import os
import math
import json
import datetime
import re
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, abort, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from functools import wraps

# Local imports (assuming these are defined in separate modules)
try:
    from questions import APTITUDE_QUESTIONS, PERSONALITY_QUESTIONS, CAREER_MAPPING, SCORING_KEY, TRAIT_WEIGHTS, TRAIT_DEFINITIONS, match_careers
    from apis import APIService, ONetAPI, PlagiarismChecker
    from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
except ImportError as e:
    print(f"Import error: {e}")
    APTITUDE_QUESTIONS = {}
    PERSONALITY_QUESTIONS = []
    CAREER_MAPPING = {}
    SCORING_KEY = {}
    TRAIT_WEIGHTS = {}
    TRAIT_DEFINITIONS = {}
    match_careers = lambda x, y: []
    class APIService: pass
    class ONetAPI: pass
    class PlagiarismChecker: pass
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'users.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure random secret key

# Configure Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['LINKEDIN_API_KEY'] = os.getenv('LINKEDIN_KEY')
app.config['ONET_CREDENTIALS'] = (os.getenv('ONET_USER'), os.getenv('ONET_PWD'))
app.config['COPYLEAKS_KEY'] = os.getenv('COPYLEAKS_KEY')

# Initialize extensions
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    mobile_number = db.Column(db.String(15))
    pin_code = db.Column(db.String(6))
    dob = db.Column(db.String(10))
    assessments = db.Column(db.JSON, default={})
    career_matches = db.Column(db.JSON, default={})
    last_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# Create database tables within app context
with app.app_context():
    try:
        db.create_all()
        print("Database tables created successfully.")
    except Exception as e:
        print(f"Error creating database tables: {e}")

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Before request hook to validate JSON inputs
@app.before_request
def validate_inputs():
    if request.content_type == 'application/json':
        try:
            request.get_json()
        except Exception:
            abort(400, description="Invalid JSON format")

# --- Routes ---

## Home Route
@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        flash(f"Error rendering home page: {e}", 'danger')
        return render_template('500.html'), 500

## Dashboard Route
@app.route('/dashboard')
@login_required
def dashboard():
    try:
        user = User.query.get(session['user_id'])
        aptitude_progress = user.assessments.get('aptitude', {}).get('progress', 0)
        personality_progress = user.assessments.get('personality', {}).get('progress', 0)

        # Mock data for dashboard (replace with actual database queries or calculations)
        stats = {
            'total_tests': 0,  # Replace with actual count
            'avg_sample_score': 0,  # Replace with average
            'avg_aptitude_score': aptitude_progress,
            'total_time_spent': 0  # Replace with sum of time spent
        }
        test_results = []  # Replace with actual test history
        sample_dates = []  # Replace with actual dates
        sample_scores = []  # Replace with actual scores
        aptitude_dates = []  # Replace with actual dates
        aptitude_scores = []  # Replace with actual scores
        date_range = request.args.get('date_range', 'all')

        return render_template('dashboard.html',
                              user=user,
                              stats=stats,
                              test_results=test_results,
                              sample_dates=sample_dates,
                              sample_scores=sample_scores,
                              aptitude_dates=aptitude_dates,
                              aptitude_scores=aptitude_scores,
                              date_range=date_range)
    except Exception as e:
        flash(f"Error rendering dashboard: {e}", 'danger')
        return render_template('500.html'), 500
## Aptitude Test Route
@app.route('/career-test/aptitude')
@login_required
def career_test_aptitude():
    try:
        user = User.query.get(session['user_id'])
        total_questions = sum(len(q_list) for category_data in APTITUDE_QUESTIONS.values() for q_list in category_data.values())
        answered_questions = user.assessments.get('aptitude', {}).get('answered_questions', [])
        completed_questions = len(answered_questions)
        return render_template('assessments/aptitude.html.jinja2',
                               questions=APTITUDE_QUESTIONS,
                               current_category='Mathematics',
                               initial_time=1800,  # 30 minutes
                               total_questions=total_questions,
                               completed_questions=completed_questions)
    except Exception as e:
        flash(f"Error rendering aptitude test: {e}", 'danger')
        return render_template('500.html'), 500

## Personality Test Route
@app.route('/personality')
@login_required
def career_test_personality():
    try:
        q = request.args.get('q', 0, type=int)
        total = len(PERSONALITY_QUESTIONS)
        q = max(0, min(q, total - 1))  # Clamp q between 0 and total-1
        question_obj = PERSONALITY_QUESTIONS[q]
        return render_template('assessments/personality.html.jinja2',
                               questions=PERSONALITY_QUESTIONS,
                               question=question_obj,
                               current_question_index=q)
    except Exception as e:
        flash(f"Error rendering personality test: {e}", 'danger')
        return render_template('500.html'), 500

## Save Answer (AJAX)
@app.route('/save-answer', methods=['POST'])
@login_required
@csrf.exempt  # Exempt AJAX POST from CSRF if needed (optional)
def save_answer():
    try:
        data = request.get_json()
        user = User.query.get(session['user_id'])
        question_id = data.get('question_id')
        if not question_id:
            return jsonify({'error': 'No question_id provided'}), 400
        answered = user.assessments.get('aptitude', {}).get('answered_questions', [])
        if question_id not in answered:
            answered.append(question_id)
            user.assessments.setdefault('aptitude', {})['answered_questions'] = answered
            db.session.commit()
        return jsonify({'message': 'Answer saved', 'answered_count': len(answered)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

## Submit Assessment
@app.route('/submit-assessment', methods=['POST'])
@limiter.limit("5/minute")
@login_required
@csrf.exempt  # Exempt AJAX POST from CSRF if needed (optional)
def submit_assessment():
    try:
        data = request.get_json()
        user = User.query.get(session['user_id'])
        test_type = data.get('type')
        if test_type not in ['aptitude', 'personality']:
            return jsonify({'error': 'Invalid test type'}), 400
        responses = data.get('responses', [])
        if test_type == 'aptitude':
            ability = calculate_aptitude(responses)
            user.assessments.setdefault('aptitude', {})['scores'] = {"Mathematics": ability, "Logical Reasoning": ability, "Verbal Ability": ability}
            user.assessments['aptitude']['progress'] = 100
        else:
            user.assessments.setdefault('personality', {})['scores'] = {"O": 70, "C": 75, "E": 60, "A": 68, "N": 35}
            user.assessments['personality']['progress'] = 100
        user.last_updated = datetime.datetime.utcnow()
        db.session.commit()
        return jsonify({'success': True, 'redirect': url_for('career_test_results')})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

## Authentication Routes
## Authentication Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and bcrypt.check_password_hash(user.password, password):
                session['user_id'] = user.id
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            flash('Invalid username or password', 'danger')
        return render_template('auth/login.html')
    except Exception as e:
        flash(f"Error during login: {e}", 'danger')
        return render_template('500.html'), 500

@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            mobile_number = request.form.get('mobile_number', '')
            pin_code = request.form.get('pin_code', '')
            dob = request.form.get('dob', '')

            if password != confirm_password:
                flash('Passwords do not match!', 'danger')
                return redirect(url_for('register'))
            if mobile_number and not re.match(r'^\d{10}$', mobile_number):
                flash("Mobile number must be 10 digits.", 'danger')
                return redirect(url_for('register'))
            if pin_code and not re.match(r'^\d{6}$', pin_code):
                flash("Pin code must be 6 digits.", 'danger')
                return redirect(url_for('register'))
            if User.query.filter_by(username=username).first():
                flash("Username already exists!", 'danger')
                return redirect(url_for('register'))
            if User.query.filter_by(email=email).first():
                flash("Email already registered!", 'danger')
                return redirect(url_for('register'))

            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, email=email, password=hashed_password,
                            mobile_number=mobile_number, pin_code=pin_code, dob=dob)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        return render_template('auth/register.html')
    except Exception as e:
        db.session.rollback()
        flash(f"Error during registration: {e}", 'danger')
        return render_template('500.html'), 500

@app.route('/logout')
def logout():
    try:
        session.clear()
        flash('You have been logged out.', 'success')
        return redirect(url_for('home'))
    except Exception as e:
        flash(f"Error during logout: {e}", 'danger')
        return render_template('500.html'), 500

## API Routes
@app.route('/api/careers/<soc_code>')
@cache.cached(timeout=3600)
def career_details(soc_code):
    try:
        return jsonify(ONetAPI().get_career_details(soc_code))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/verify-answers', methods=['POST'])
def verify_answers():
    try:
        responses = request.json.get('answers')
        scores = [PlagiarismChecker.verify_content(r) for r in responses]
        return jsonify({"originality_scores": scores})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

## Career Test Routes
@app.route('/career-test')
def career_test():
    try:
        return render_template('assessments/career_assessment.html')
    except Exception as e:
        flash(f"Error rendering career test: {e}", 'danger')
        return render_template('500.html'), 500

@app.route('/career-test/results')
@login_required
def career_test_results():
    try:
        user = User.query.get(session['user_id'])
        if not user.assessments.get('aptitude', {}).get('scores') or not user.assessments.get('personality', {}).get('scores'):
            flash('Complete both tests to view results', 'warning')
            return redirect(url_for('career_test'))

        aptitude = user.assessments['aptitude']['scores']
        personality = user.assessments['personality']['scores']
        aptitude_interpretation = interpret_scores(aptitude)
        personality_interpretation = interpret_scores(personality)

        # Mock aptitude and personality sections/values (replace with actual data)
        aptitude_sections = list(aptitude.keys())
        aptitude_values = list(aptitude.values())
        personality_traits = list(personality.keys())
        personality_scores = [50 + ((score - 50) / 10) * 10 for score in personality.values()]  # Example T-score calculation

        career_matches = []
        for career, details in CAREER_MAPPING.items():
            apt_match = all(aptitude.get(skill, 0) >= threshold for skill, threshold in details['requirements']['aptitude'].items())
            pers_match = all(personality.get(trait, 50) >= threshold if trait != 'N' else personality.get(trait, 50) <= threshold
                             for trait, threshold in details['requirements']['personality'].items())
            if apt_match and pers_match:
                gaps = calculate_skill_gaps_for_career(aptitude, personality, details)
                career_matches.append({
                    'name': career,
                    'details': details,
                    'match_score': calculate_match_score(aptitude, personality, details),
                    'skill_gaps': gaps
                })
        career_matches.sort(key=lambda x: x['match_score'], reverse=True)

        return render_template('results.html.jinja2',
                              career_matches=career_matches,
                              aptitude=aptitude,
                              personality=personality,
                              aptitude_sections=aptitude_sections,
                              aptitude_values=aptitude_values,
                              personality_traits=personality_traits,
                              personality_scores=personality_scores)
    except Exception as e:
        flash(f"Error rendering career test results: {e}", 'danger')
        return render_template('500.html'), 500

## Additional Routes
@app.route('/student')
@login_required
def student():
    try:
        return render_template('student.html')
    except Exception as e:
        flash(f"Error rendering student portal: {e}", 'danger')
        return render_template('500.html'), 500

@app.route('/profile')
@login_required
def profile():
    try:
        user = User.query.get(session['user_id'])
        return render_template('profile.html', user=user)
    except Exception as e:
        flash(f"Error rendering profile: {e}", 'danger')
        return render_template('500.html'), 500

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    try:
        user = User.query.get(session['user_id'])
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            mobile_number = request.form['mobile_number']
            pin_code = request.form['pin_code']
            dob = request.form['dob']
            current_password = request.form['current_password']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']

            # Validate current password
            if not bcrypt.check_password_hash(user.password, current_password):
                flash("Current password is incorrect!", "danger")
                return redirect(url_for('settings'))

            # Validate username and email uniqueness
            if username != user.username and User.query.filter_by(username=username).first():
                flash("Username already taken!", "danger")
                return redirect(url_for('settings'))
            if email != user.email and User.query.filter_by(email=email).first():
                flash("Email already registered!", "danger")
                return redirect(url_for('settings'))

            # Update user details
            user.username = username
            user.email = email
            user.mobile_number = mobile_number
            user.pin_code = pin_code
            user.dob = dob

            # Handle password update
            if new_password and confirm_password:
                if new_password != confirm_password:
                    flash("New passwords do not match!", "danger")
                    return redirect(url_for('settings'))
                if len(new_password) < 6:
                    flash("New password must be at least 6 characters!", "danger")
                    return redirect(url_for('settings'))
                user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')

            db.session.commit()
            flash("Settings updated successfully!", "success")
            return redirect(url_for('settings'))
        return render_template('settings.html', user=user)
    except Exception as e:
        db.session.rollback()
        flash(f"Error updating settings: {e}", 'danger')
        return render_template('500.html'), 500

@app.route('/degree')
def degree():
    try:
        # Mock degree data (replace with database query later)
        degrees = [
            {'title': 'Bachelor of Science in Computer Science', 'institution': 'University of Technology', 'duration': '4 years'},
            {'title': 'Master of Business Administration', 'institution': 'Global Business School', 'duration': '2 years'},
            {'title': 'Bachelor of Arts in Psychology', 'institution': 'Riverside University', 'duration': '3 years'},
            {'title': 'Master of Science in Data Science', 'institution': 'Tech Institute', 'duration': '1.5 years'}
        ]
        return render_template('degree.html', degrees=degrees)
    except Exception as e:
        flash(f"Error rendering degree page: {e}", 'danger')
        return render_template('500.html'), 500

@app.route('/online-jobs')
def online_jobs():
    try:
        return render_template('careers/online.html')
    except Exception as e:
        flash(f"Error rendering online jobs: {e}", 'danger')
        return render_template('500.html'), 500

@app.route('/software-engineer')
def software_engineer():
    try:
        return render_template('careers/software_engg.html')
    except Exception as e:
        flash(f"Error rendering software engineer page: {e}", 'danger')
        return render_template('500.html'), 500

@app.route('/introvert-careers')
def introvert_careers():
    try:
        return render_template('careers/introvert.html')
    except Exception as e:
        flash(f"Error rendering introvert careers: {e}", 'danger')
        return render_template('500.html'), 500

@app.route('/test')
def test():
    try:
        return render_template('test.html')
    except Exception as e:
        flash(f"Error rendering test page: {e}", 'danger')
        return render_template('500.html'), 500

## Protected API Route
@app.route('/protected-api', methods=['POST'])
@jwt_required()
def protected_endpoint():
    try:
        return jsonify({"message": "Protected endpoint accessed"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

## Helper Functions
def interpret_scores(raw_scores):
    try:
        interpretations = {}
        for trait, score in raw_scores.items():
            t_score = 50 + ((score - SCORING_KEY.get(trait, {"mean": 50})["mean"]) / SCORING_KEY.get(trait, {"sd": 10})["sd"]) * 10
            t_score = max(0, min(100, t_score))
            for low, high, label in SCORING_KEY.get(trait, {"norms": [(0, 100, "Unknown")]})["norms"]:
                if low <= t_score <= high:
                    interpretations[trait] = {"score": round(t_score, 1), "label": label, "definition": TRAIT_DEFINITIONS.get(trait, "No definition")}
                    break
        return interpretations
    except Exception as e:
        print(f"Error in interpret_scores: {e}")
        return {}

def get_question(question_id):
    try:
        for domain, levels in APTITUDE_QUESTIONS.items():
            for difficulty_level, question_list in levels.items():
                for question in question_list:
                    if question["id"] == question_id:
                        return {"id": question["id"], "discrimination": question["irt_params"]["discrimination"],
                                "difficulty": question["irt_params"]["difficulty"], "time_limit": question["time_limit"]}
        return None
    except Exception as e:
        print(f"Error in get_question: {e}")
        return None

def calculate_aptitude(responses):
    try:
        ability = 0
        for response in responses:
            question = get_question(response['id'])
            if not question:
                continue
            p = 1 / (1 + math.exp(-question['discrimination'] * (ability - question['difficulty'])))
            epsilon = 1e-10
            p = min(max(p, epsilon), 1 - epsilon)
            ability += math.log(p / (1 - p))
        return ability
    except Exception as e:
        print(f"Error in calculate_aptitude: {e}")
        return 0

def calculate_match_score(aptitude, personality, career_details):
    try:
        total_points = 0
        earned_points = 0
        for skill, threshold in career_details.get('requirements', {}).get('aptitude', {}).items():
            total_points += 100
            earned_points += min(aptitude.get(skill, 0), threshold)
        for trait, threshold in career_details.get('requirements', {}).get('personality', {}).items():
            total_points += 100
            if trait == 'N':
                earned_points += max(0, 100 - abs(personality.get(trait, 50) - threshold) * 2)
            else:
                earned_points += max(0, 100 - abs(personality.get(trait, 50) - threshold) * 2)
        return (earned_points / total_points) * 100 if total_points > 0 else 0
    except Exception as e:
        print(f"Error in calculate_match_score: {e}")
        return 0

def calculate_skill_gaps_for_career(aptitude, personality, career_details):
    try:
        gaps = {
            'aptitude': {skill: max(0, threshold - aptitude.get(skill, 0)) for skill, threshold in career_details.get('requirements', {}).get('aptitude', {}).items()},
            'personality': {trait: (max(0, threshold - personality.get(trait, 50)) if trait != 'N' else max(0, personality.get(trait, 50) - threshold))
                            for trait, threshold in career_details.get('requirements', {}).get('personality', {}).items()}
        }
        return gaps
    except Exception as e:
        print(f"Error in calculate_skill_gaps_for_career: {e}")
        return {'aptitude': {}, 'personality': {}}

## Error Handlers
@app.errorhandler(404)
def not_found(error):
    try:
        return render_template('404.html'), 404
    except Exception as e:
        return "404 - Page Not Found", 404

@app.errorhandler(500)
def internal_error(error):
    try:
        return render_template('500.html'), 500
    except Exception as e:
        return "500 - Internal Server Error", 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)