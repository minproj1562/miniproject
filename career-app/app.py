import os
import math
import json
import datetime
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, abort, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

# Local imports
from questions import APTITUDE_QUESTIONS, PERSONALITY_QUESTIONS, CAREER_MAPPING, SCORING_KEY, TRAIT_WEIGHTS, TRAIT_DEFINITIONS

from apis import APIService, ONetAPI, PlagiarismChecker
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['LINKEDIN_API_KEY'] = os.getenv('LINKEDIN_KEY')
app.config['ONET_CREDENTIALS'] = (os.getenv('ONET_USER'), os.getenv('ONET_PWD'))
app.config['COPYLEAKS_KEY'] = os.getenv('COPYLEAKS_KEY')

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})  # or 'RedisCache'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    mobile_number = db.Column(db.String(15))
    pin_code = db.Column(db.String(6))
    dob = db.Column(db.String(10))
    assessments = db.Column(db.JSON, default={})
    api_data = db.Column(db.JSON, default={})
    last_updated = db.Column(db.DateTime)
    assessments_completed = db.Column(db.Integer, default=0)

@app.before_request
def validate_inputs():
    """Validate JSON inputs for routes that accept JSON."""
    if request.content_type == 'application/json':
        try:
            request.get_json()
        except Exception:
            abort(400, description="Invalid JSON format")

@app.route('/')
def home():
    return render_template('index.html')  # or whichever template is your home page

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    aptitude_progress = user.assessments.get('aptitude_progress', 0) if user.assessments else 0
    personality_progress = user.assessments.get('personality_progress', 0) if user.assessments else 0
    return render_template('dashboard.html', 
                           aptitude_progress=aptitude_progress,
                           personality_progress=personality_progress)

@app.route('/aptitude-test')
def aptitude_test():
    return render_template('aptitude.html', questions=APTITUDE_QUESTIONS)

@app.route('/personality-test')
def personality_test():
    return render_template('personality.html', questions=PERSONALITY_QUESTIONS)

@app.route('/submit-assessment', methods=['POST'])
def submit_assessment():
    data = request.get_json()
    if 'user_id' not in session:
        abort(401)
    user = User.query.get(session['user_id'])
    
    if data['type'] == 'personality':
        scores = calculate_personality(data['responses'])
    else:
        scores = calculate_aptitude(data['responses'])
    
    if not user.assessments:
        user.assessments = {}
    user.assessments[f"{data['type']}_scores"] = scores
    user.assessments[f"{data['type']}_progress"] = 100
    db.session.commit()
    
    return jsonify({'redirect': url_for('results')})

def calculate_personality(responses):
    """Calculate personality scores using validated psychometric methods"""
    trait_scores = {t: 0 for t in ["O", "C", "E", "A", "N"]}
    
    for q_id, response in responses.items():
        try:
            question = next(q for q in PERSONALITY_QUESTIONS if q["id"] == int(q_id))
            trait = question["trait"]
            
            if trait == "V":  # Skip validation items
                continue
                
            # Reverse score if needed
            adjusted_score = response if question["direction"] else (4 - response)
            trait_scores[trait] += adjusted_score * TRAIT_WEIGHTS[trait]
            
        except (StopIteration, ValueError):
            app.logger.error(f"Invalid response ID: {q_id}")
            continue

    return trait_scores

def interpret_scores(raw_scores):
    """Convert raw scores to standardized interpretations"""
    interpretations = {}
    
    for trait, score in raw_scores.items():
        # Convert to T-score (M=50, SD=10)
        t_score = 50 + ((score - SCORING_KEY[trait]["mean"]) / SCORING_KEY[trait]["sd"]) * 10
        t_score = max(0, min(100, t_score))  # Clamp between 0-100
        
        # Find interpretation
        for low, high, label in SCORING_KEY[trait]["norms"]:
            if low <= t_score <= high:
                interpretations[trait] = {
                    "score": round(t_score, 1),
                    "label": label,
                    "definition": TRAIT_DEFINITIONS[trait]
                }
                break
                
    return interpretations

@app.route('/submit-assessment', methods=['POST'])
def submit_assessment():
    data = request.get_json()
    user = User.query.get(session['user_id'])
    
    if data['type'] == 'personality':
        raw_scores = calculate_personality(data['responses'])
        interpretations = interpret_scores(raw_scores)
        
        user.assessments['personality'] = {
            'raw_scores': raw_scores,
            'interpretations': interpretations,
            'completed_at': datetime.datetime.utcnow()
        }
        
    db.session.commit()
    return jsonify(interpretations)
def get_question(question_id):
    for domain, levels in APTITUDE_QUESTIONS.items():
        for difficulty_level, question_list in levels.items():
            for question in question_list:
                if question["id"] == question_id:
                    return {
                        "id": question["id"],
                        "discrimination": question["irt_params"]["discrimination"],
                        "difficulty": question["irt_params"]["difficulty"],
                        "time_limit": question["time_limit"]
                    }
    return None

def calculate_aptitude(responses):
    ability = 0
    for response in responses:
        question = get_question(response['id'])
        if not question:
            continue
        p = 1 / (1 + math.exp(-question['discrimination'] * (ability - question['difficulty'])))
        epsilon = 1e-10
        p = min(max(p, epsilon), 1 - epsilon)
        # Using a simple log-odds approach for demonstration
        ability += math.log(p / (1 - p))
    return ability

@app.route('/results')
def results():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    aptitude = user.assessments.get('aptitude_scores') if user.assessments else None
    personality = user.assessments.get('personality_scores') if user.assessments else None
    return render_template('results.html',
                           aptitude=aptitude,
                           personality=personality,
                           careers=CAREER_MAPPING)

@app.route('/api/careers/<soc_code>')
def career_details(soc_code):
    return jsonify(ONetAPI().get_career_details(soc_code))

@app.route('/api/job-market/<title>')
def job_market(title):
    return jsonify(APIService.get_linkedin_jobs(title))

@app.route('/api/verify-answers', methods=['POST'])
def verify_answers():
    responses = request.json.get('answers')
    scores = [PlagiarismChecker.verify_content(r) for r in responses]
    return jsonify({"originality_scores": scores})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('Please fill in all fields', 'danger')
            return redirect(url_for('login'))
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            mobile_number=request.form.get('mobile_number'),
            pin_code=request.form.get('pin_code'),
            dob=request.form.get('dob')
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception:
            flash('Username or email already exists!', 'danger')
            db.session.rollback()
    return render_template('auth/register.html')

@app.route('/interview-prep')
def interview_prep():
    return render_template('careers/interview.html')

@app.route('/career-test')
def career_test():
    return render_template('careers/career_assessment.html')

@app.route('/online-jobs')
def online_jobs():
    return render_template('careers/online.html')

@app.route('/software-engineer')
def software_engineer():
    return render_template('careers/software_engg.html')

@app.route('/introvert-careers')
def introvert_careers():
    return render_template('careers/introvert.html')

@app.route('/degree')
def degree():
    return render_template('degree.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/protected-api', methods=['POST'])
@jwt_required()
def protected_endpoint():
    return jsonify({"message": "Protected endpoint accessed"})

@cache.memoize(timeout=3600)
def get_career_data(soc_code):
    return ONetAPI().get_career_details(soc_code)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
