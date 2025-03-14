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
from questions import match_careers
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


user_aptitude_scores = {"Mathematics": 80, "Logical Reasoning": 72, "Verbal Ability": 68}
user_personality_scores = {"O": 70, "C": 75, "E": 60, "A": 68, "N": 35}
matched = match_careers(user_aptitude_scores, user_personality_scores)
print("Matched Careers:", matched)


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

# Use new Flask-Limiter usage: don't pass app into the constructor.
limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)

cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

# ----------------- MODELS ----------------- #
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    assessments = db.Column(db.JSON, default={
        'aptitude': {'scores': {}, 'progress': 0, 'answered_questions': []},
        'personality': {'scores': {}, 'progress': 0, 'answered_questions': []}
    })
    career_matches = db.Column(db.JSON, default=[])
    last_updated = db.Column(db.DateTime)

# ----------------- HOOKS ----------------- #
@app.before_request
def validate_inputs():
    if request.content_type == 'application/json':
        try:
            request.get_json()
        except Exception:
            abort(400, description="Invalid JSON format")

# ----------------- ROUTES ----------------- #
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    aptitude_progress = user.assessments['aptitude'].get('progress', 0)
    personality_progress = user.assessments['personality'].get('progress', 0)
    return render_template('results.html.jinja2',
                           aptitude_progress=aptitude_progress,
                           personality_progress=personality_progress)

# ------------------ APTITUDE TEST ------------------ #
@app.route('/career-test/aptitude')
@login_required
def career_test_aptitude():
    user = User.query.get(session['user_id'])
    total_questions = sum(
        len(q_list)
        for category_data in APTITUDE_QUESTIONS.values()
        for q_list in category_data.values()
    )
    answered_questions = user.assessments['aptitude'].get('answered_questions', [])
    completed_questions = len(answered_questions)
    return render_template(
        'assessments/aptitude.html.jinja2',
        questions=APTITUDE_QUESTIONS,
        current_category='Mathematics',
        initial_time=1800,  # 30 minutes
        total_questions=total_questions,
        completed_questions=completed_questions
    )

# ------------------ PERSONALITY TEST ------------------ #
@app.route('/career-test/personality')
@login_required
def career_test_personality():
    # Use query parameter "q" to determine which personality question to display
    q = request.args.get('q', 0, type=int)
    total = len(PERSONALITY_QUESTIONS)
    if q < 0:
        q = 0
    if q >= total:
        q = total - 1
    question_obj = PERSONALITY_QUESTIONS[q]
    return render_template(
        'assessments/personality.html.jinja2',
        questions=PERSONALITY_QUESTIONS,
        question=question_obj,
        current_question_index=q
    )

# ------------------ SAVE ANSWER (AJAX) ------------------ #
@app.route('/save-answer', methods=['POST'])
@login_required
def save_answer():
    data = request.get_json()
    user = User.query.get(session['user_id'])
    question_id = data.get('question_id')
    if not question_id:
        return jsonify({'error': 'No question_id provided'}), 400
    answered = user.assessments['aptitude'].get('answered_questions', [])
    if question_id not in answered:
        answered.append(question_id)
        user.assessments['aptitude']['answered_questions'] = answered
        db.session.commit()
    return jsonify({'message': 'Answer saved', 'answered_count': len(answered)})

# ------------------ SUBMIT ASSESSMENT ------------------ #
@app.route('/submit-assessment', methods=['POST'])
@limiter.limit("5/minute")
@login_required
def submit_assessment():
    data = request.get_json()
    user = User.query.get(session['user_id'])
    test_type = data.get('type')
    if test_type not in ['aptitude', 'personality']:
        return jsonify({'error': 'Invalid test type'}), 400
    responses = data.get('responses', [])
    if test_type == 'aptitude':
        # Placeholder: add your aptitude scoring logic here
        user.assessments['aptitude']['progress'] = 100
    else:
        # Placeholder: add your personality scoring logic here
        user.assessments['personality']['progress'] = 100
    db.session.commit()
    return jsonify({'success': True, 'redirect': url_for('career_test_results')})

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
# ------------------ AUTH & OTHER ROUTES ------------------ #
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
        new_user = User(username=username, email=email, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception:
            flash('Username or email already exists!', 'danger')
            db.session.rollback()
    return render_template('auth/register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))
@app.route('/api/careers/<soc_code>')
def career_details(soc_code):
    return jsonify(ONetAPI().get_career_details(soc_code))
@app.route('/api/verify-answers', methods=['POST'])
def verify_answers():
    responses = request.json.get('answers')
    scores = [PlagiarismChecker.verify_content(r) for r in responses]
    return jsonify({"originality_scores": scores})
@app.route('/career-test')
def career_test():
    return render_template('assessments/career_assessment.html')

@app.route('/career-test/results')
@login_required
def career_test_results():
    user = User.query.get(session['user_id'])
    if not user.assessments.get('aptitude', {}).get('scores') or not user.assessments.get('personality', {}).get('scores'):
        flash('Complete both tests to view results', 'warning')
        return redirect(url_for('career_test'))
    
    aptitude = user.assessments['aptitude']['scores']
    personality = user.assessments['personality']['scores']
    aptitude_interpretation = interpret_scores(aptitude)
    personality_interpretation = interpret_scores(personality)

    # Get career matches
    career_matches = []
    skill_gaps = {}
    for career, details in CAREER_MAPPING.items():
        apt_match = all(
        aptitude.get(skill, 0) >= threshold
        for skill, threshold in details['requirements']['aptitude'].items()
    )
    pers_match = all(
        personality.get(trait, 50) >= threshold if trait != 'N'
        else personality.get(trait, 50) <= threshold
        for trait, threshold in details['requirements']['personality'].items()
    )
    if apt_match and pers_match:
        gaps = calculate_skill_gaps_for_career(aptitude, personality, details)
        career_matches.append({
            'name': career,
            'details': details,
            'match_score': calculate_match_score(aptitude, personality, details),
            'skill_gaps': gaps
        })

    # Sort by match score descending
    career_matches.sort(key=lambda x: x['match_score'], reverse=True)
    return render_template('assessments/results.html.jinja2',
                       career_matches=career_matches,
                       aptitude=aptitude,
                       personality=personality,
                       aptitude_interpretation=aptitude_interpretation,
                       personality_interpretation=personality_interpretation)


def calculate_match_score(aptitude, personality, career_details):
    """Calculate percentage match for a career"""
    total_points = 0
    earned_points = 0
    
    # Calculate aptitude match
    for skill, threshold in career_details['requirements']['aptitude'].items():
        total_points += 100
        earned_points += min(aptitude.get(skill, 0), threshold)
        # Calculate personality match
    for trait, threshold in career_details['requirements']['personality'].items():
        total_points += 100
        if trait == 'N':
            # Lower neuroticism is better
            earned_points += max(0, 100 - abs(personality.get(trait, 50) - threshold) * 2)
        else:
            earned_points += max(0, 100 - abs(personality.get(trait, 50) - threshold) * 2)
    return (earned_points / total_points) * 100 if total_points > 0 else 0
def calculate_skill_gaps_for_career(aptitude, personality, career_details):
    gaps = {
        'aptitude': {
            skill: max(0, threshold - aptitude.get(skill, 0))
            for skill, threshold in career_details['requirements']['aptitude'].items()
        },
        'personality': {
            trait: (max(0, threshold - personality.get(trait, 50))
                    if trait != 'N'
                    else max(0, personality.get(trait, 50) - threshold))
            for trait, threshold in career_details['requirements']['personality'].items()
        }
    }
    return gaps

@app.route('/degree')
def degree():
    return render_template('degree.html')
@app.route('/online-jobs')
def online_jobs():
    return render_template('careers/online.html')

@app.route('/software-engineer')
def software_engineer():
    return render_template('careers/software_engg.html')

@app.route('/introvert-careers')
def introvert_careers():
    return render_template('careers/introvert.html')

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
