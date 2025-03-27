import os
import sys
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_mail import Mail, Message
from flask_migrate import Migrate
from datetime import datetime
from collections import defaultdict
import requests
import random
import copy
import json
from PIL import Image
from datetime import datetime

# Import question data
from questions import (
    APTITUDE_QUESTIONS, PERSONALITY_QUESTIONS, SCORING_KEY,
    CAREER_MAPPING, SKILL_GAP_QUESTIONS, LEARNING_RESOURCES
)
from forms import ProfileForm, LoginForm, RegisterForm, ContactForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '033dc7a2f8382c4dd7bd18a473e24db20b088146eb846900'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///career_analytics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'abc@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password-here'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
app.config['WTF_CSRF_HEADERS'] = ['X-CSRF-Token']
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=True)
    tests = db.relationship('TestResult', backref='user', lazy=True)
    badges = db.relationship('Badge', backref='user', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)

class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    test_type = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Float, nullable=False)
    time_spent = db.Column(db.Integer, nullable=True)
    details = db.Column(db.Text, nullable=True)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    icon = db.Column(db.String(50), nullable=False)
    date_earned = db.Column(db.DateTime, default=datetime.utcnow)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

class ONetAPI:
    def get_career_details(self, soc_code):
        return {
            'title': 'Software Developer' if soc_code == '15-1132.00' else 'Business Manager',
            'wages': {'median': 105000},
            'outlook': {'growth_rate': 22}
        }

def get_onet_api():
    return ONetAPI()

# Custom Jinja2 filter for datetime formatting
def datetimeformat(value, format='%Y'):
    if value == 'now':
        return datetime.utcnow().strftime(format)
    return value

app.jinja_env.filters['datetimeformat'] = datetimeformat

# Generate dynamic test questions with no repeats in a session
def generate_questions(test_type):
    if test_type == 'aptitude':
        available_questions = copy.deepcopy(APTITUDE_QUESTIONS)
        used_questions = session.get('used_aptitude_questions', set())
        questions = []
        current_difficulty = 'moderate'
        
        for _ in range(10):
            category = random.choice(list(available_questions.keys()))
            difficulty_questions = [q for q in available_questions[category][current_difficulty] 
                                 if q['id'] not in used_questions]
            if not difficulty_questions:
                for diff in ['easy', 'moderate', 'hard']:
                    difficulty_questions = [q for q in available_questions[category][diff] 
                                         if q['id'] not in used_questions]
                    if difficulty_questions:
                        current_difficulty = diff
                        break
            if not difficulty_questions:
                continue
            question = random.choice(difficulty_questions)
            question['time_limit'] = question.get('time_limit', 60)
            questions.append(question)
            used_questions.add(question['id'])
        
        session['aptitude_questions'] = questions
        session['used_aptitude_questions'] = used_questions
        session['aptitude_correct'] = 0
        session['aptitude_total'] = 0
        session['aptitude_category_scores'] = defaultdict(int)
        session['aptitude_category_counts'] = defaultdict(int)
        return questions[:10]
    
    elif test_type == 'personality':
        questions = random.sample(PERSONALITY_QUESTIONS, min(10, len(PERSONALITY_QUESTIONS)))
        for q in questions:
            q['time_limit'] = q.get('time_limit', 60)
        session['personality_questions'] = questions
        return questions
    
    elif test_type == 'skill_gap':
        field = session.get('selected_field', 'Software Development')
        available_questions = copy.deepcopy(SKILL_GAP_QUESTIONS.get(field, []))
        questions = random.sample(available_questions, min(10, len(available_questions)))
        for q in questions:
            q['time_limit'] = q.get('time_limit', 60)
        session['skill_gap_questions'] = questions
        session['skill_gap_correct'] = 0
        session['skill_gap_total'] = 0
        return questions
    
    return []

# Routes
@app.route('/')
def index():
    if not current_user.is_authenticated and not session.get('_flashes'):
        flash('Kindly log in to unlock comprehensive access to all features.', 'info')
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all() if current_user.is_authenticated else []
    return render_template('index.html', active_page='index', notifications=notifications, current_year=datetime.utcnow().year)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Logged in successfully!', 'success')
            return redirect(request.args.get('next', url_for('dashboard')))
        flash('Invalid username or password.', 'danger')
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all() if current_user.is_authenticated else []
    return render_template('auth/login.html', form=form, active_page='login', notifications=notifications)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists.', 'danger')
        elif User.query.filter_by(email=form.email.data).first():
            flash('Email already registered.', 'danger')
        else:
            hashed_password = generate_password_hash(form.password.data)
            new_user = User(username=form.username.data, password=hashed_password, email=form.email.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all() if current_user.is_authenticated else []
    return render_template('auth/register.html', form=form, active_page='register', notifications=notifications)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    tests = TestResult.query.filter_by(user_id=current_user.id).order_by(TestResult.completed_at.desc()).all()
    badges = Badge.query.filter_by(user_id=current_user.id).order_by(Badge.date_earned.desc()).limit(5).all()
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
    
    completed_tests = set(t.test_type for t in tests)
    available_tests = {
        'aptitude': 'Aptitude Test' not in completed_tests,
        'personality': 'Personality Test' not in completed_tests,
        'skill_gap': 'Skill Gap Test' not in completed_tests
    }
    can_proceed = 'aptitude' in completed_tests and 'personality' in completed_tests
    
    for test in tests:
        test.details_dict = json.loads(test.details) if test.details else {}
    
    return render_template('dashboard.html', user=current_user, tests=tests, badges=badges, notifications=notifications,
                          available_tests=available_tests, can_proceed=can_proceed, active_page='dashboard')

@app.route('/test', methods=['GET', 'POST'])
@login_required
def test():
    test_type = request.args.get('type')
    instructions = {
        "time_limit": "You have 10 minutes to complete this test.",
        "honesty": "Please answer all questions honestly and without external assistance.",
        "scientific_accuracy": "This test is designed to assess your skills with validated questions."
    }

    if test_type == 'aptitude':
        questions = session.get('aptitude_questions')
        if not questions or request.method == 'GET':
            questions = generate_questions('aptitude')
        current_question_index = int(request.args.get('q', 0))
        if current_question_index >= len(questions):
            return redirect(url_for('dashboard'))
        question = questions[current_question_index]
        category = next((cat for cat, levels in APTITUDE_QUESTIONS.items() if any(question['id'] in [q['id'] for q in level] for level in levels.values())), "Unknown")
        notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
        return render_template('assessments/aptitude.html',
                              questions=[question],
                              instructions=instructions,
                              current_category=category,
                              total_questions=len(questions),
                              completed_questions=current_question_index,
                              current_question_index=current_question_index,
                              initial_time=question['time_limit'],
                              active_page='test',
                              test_type='aptitude',
                              notifications=notifications)
    
    elif test_type == 'personality':
        questions = session.get('personality_questions')
        if not questions or request.method == 'GET':
            questions = generate_questions('personality')
        notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
        return render_template('assessments/personality.html',
                              questions=questions,
                              instructions=instructions,
                              active_page='test',
                              test_type='personality',
                              notifications=notifications)
    
    elif test_type == 'skill_gap':
        selected_field = request.args.get('field', session.get('selected_field', None))
        if not selected_field:
            return redirect(url_for('interest_test'))
        session['selected_field'] = selected_field
        questions = session.get('skill_gap_questions')
        if not questions or request.method == 'GET':
            questions = generate_questions('skill_gap')
        current_question_index = int(request.args.get('q', 0))
        if current_question_index >= len(questions):
            return redirect(url_for('dashboard'))
        question = questions[current_question_index]
        notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
        return render_template('assessments/interest_test.html',
                              selected_field=selected_field,
                              questions=questions,
                              total_questions=len(questions),
                              completed_questions=current_question_index,
                              current_question_index=current_question_index,
                              initial_time=question['time_limit'],
                              active_page='test',
                              test_type='skill_gap',
                              notifications=notifications)
    
    flash('Invalid test type.', 'danger')
    return redirect(url_for('dashboard'))

@app.route('/submit_aptitude', methods=['POST'])
@login_required
def submit_aptitude():
    data = request.get_json()
    if not data or 'responses' not in data:
        return jsonify({'error': 'No data provided'}), 400
    
    responses = data['responses']
    time_spent = data.get('time_spent', 0)
    current_question_index = data['current_question_index']
    questions = session.get('aptitude_questions', [])
    
    if not questions or current_question_index >= len(questions):
        return jsonify({'error': 'Invalid session data'}), 400
    
    current_response = responses[-1]
    question_id = current_response['questionId']
    answer = int(current_response['answer'])
    question = next((q for q in questions if q['id'] == question_id), None)
    if not question:
        return jsonify({'error': 'Question not found'}), 400
    
    category = next((cat for cat, levels in APTITUDE_QUESTIONS.items() if any(question['id'] in [q['id'] for q in level] for level in levels.values())), "Unknown")
    session['aptitude_total'] += 1
    session['aptitude_category_counts'][category] += 1
    if answer == question['correct']:
        session['aptitude_correct'] += 1
        session['aptitude_category_scores'][category] += 1
    
    # Dynamic difficulty adjustment
    if session['aptitude_total'] >= 3:
        performance = session['aptitude_correct'] / session['aptitude_total']
        available_questions = copy.deepcopy(APTITUDE_QUESTIONS)
        used_questions = session.get('used_aptitude_questions', set())
        if performance >= 0.75 and current_question_index + 1 < len(questions):
            difficulty = 'hard'
            next_questions = [q for cat in available_questions for q in available_questions[cat][difficulty] if q['id'] not in used_questions]
            if next_questions:
                next_q = random.choice(next_questions)
                questions[current_question_index + 1] = next_q
                used_questions.add(next_q['id'])
        elif performance <= 0.25 and current_question_index + 1 < len(questions):
            difficulty = 'easy'
            next_questions = [q for cat in available_questions for q in available_questions[cat][difficulty] if q['id'] not in used_questions]
            if next_questions:
                next_q = random.choice(next_questions)
                questions[current_question_index + 1] = next_q
                used_questions.add(next_q['id'])
        session['used_aptitude_questions'] = used_questions
        session['aptitude_questions'] = questions
    
    if current_question_index == len(questions) - 1:
        score = (session['aptitude_correct'] / session['aptitude_total']) * 100
        detailed_scores = {cat: (session['aptitude_category_scores'][cat] / session['aptitude_category_counts'][cat]) * 100 
                         for cat in session['aptitude_category_scores'] if session['aptitude_category_counts'][cat] > 0}
        result = TestResult(user_id=current_user.id, test_type='aptitude', score=score, time_spent=time_spent, details=json.dumps(detailed_scores))
        db.session.add(result)
        
        if not Badge.query.filter_by(user_id=current_user.id, name="First Test Completed").first():
            badge = Badge(user_id=current_user.id, name="First Test Completed", description="Completed your first test!", icon="fas fa-trophy")
            db.session.add(badge)
        if score >= 80:
            if not Badge.query.filter_by(user_id=current_user.id, name="High Scorer").first():
                badge = Badge(user_id=current_user.id, name="High Scorer", description="Scored 80% or higher!", icon="fas fa-star")
                db.session.add(badge)
        
        notification = Notification(user_id=current_user.id, message=f"Aptitude Test completed! Score: {score:.1f}%", type="test_result")
        db.session.add(notification)
        db.session.commit()
        
        session.pop('aptitude_questions', None)
        session.pop('aptitude_correct', None)
        session.pop('aptitude_total', None)
        session.pop('aptitude_category_scores', None)
        session.pop('aptitude_category_counts', None)
        return jsonify({'redirect': url_for('dashboard')})
    
    next_question = questions[current_question_index + 1]
    next_question['category'] = next((cat for cat, levels in APTITUDE_QUESTIONS.items() if any(next_question['id'] in [q['id'] for q in level] for level in levels.values())), "Unknown")
    return jsonify({'question': next_question, 'current_question_index': current_question_index + 1})

@app.route('/submit_assessment', methods=['POST'])
@login_required
def submit_assessment():
    data = request.get_json()
    if not data or data.get('type') != 'personality':
        return jsonify({'error': 'Invalid data'}), 400
    
    responses = data['responses']
    duration = data['duration']
    questions = session.get('personality_questions', [])
    
    if len(responses) != len(questions):
        return jsonify({'error': 'Incomplete responses'}), 400
    
    scores = {'Openness': 0, 'Conscientiousness': 0, 'Extraversion': 0, 'Agreeableness': 0, 'Neuroticism': 0}
    counts = {trait: 0 for trait in scores}
    
    for response in responses:
        question = next((q for q in questions if q['id'] == response['questionId']), None)
        if question:
            value = int(response['answer'])
            trait = question['trait']
            scores[trait] += SCORING_KEY[trait][value]
            counts[trait] += 1
    
    for trait in scores:
        scores[trait] = (scores[trait] / (counts[trait] * 4)) * 100 if counts[trait] > 0 else 0
    
    dominant_trait = max(scores, key=scores.get)
    result = TestResult(user_id=current_user.id, test_type='personality', score=scores[dominant_trait], time_spent=duration, details=json.dumps(scores))
    db.session.add(result)
    
    if not Badge.query.filter_by(user_id=current_user.id, name="First Test Completed").first():
        badge = Badge(user_id=current_user.id, name="First Test Completed", description="Completed your first test!", icon="fas fa-trophy")
        db.session.add(badge)
    if scores[dominant_trait] >= 80:
        if not Badge.query.filter_by(user_id=current_user.id, name="High Scorer").first():
            badge = Badge(user_id=current_user.id, name="High Scorer", description="Scored 80% or higher!", icon="fas fa-star")
            db.session.add(badge)
    
    notification = Notification(user_id=current_user.id, message=f"Personality Test completed! Dominant trait: {dominant_trait} ({scores[dominant_trait]:.1f}%)", type="test_result")
    db.session.add(notification)
    db.session.commit()
    
    session.pop('personality_questions', None)
    return jsonify({'redirect': url_for('dashboard')})

@app.route('/submit_skill_gap', methods=['POST'])
@login_required
def submit_skill_gap():
    data = request.get_json()
    if not data or 'responses' not in data:
        return jsonify({'error': 'No data provided'}), 400
    
    responses = data['responses']
    time_spent = data.get('time_spent', 0)
    current_question_index = data['current_question_index']
    questions = session.get('skill_gap_questions', [])
    
    if not questions or current_question_index >= len(questions):
        return jsonify({'error': 'Invalid session data'}), 400
    
    current_response = responses[-1]
    question_id = current_response['questionId']
    answer = int(current_response['answer'])
    question = next((q for q in questions if q['id'] == question_id), None)
    if not question:
        return jsonify({'error': 'Question not found'}), 400
    
    session['skill_gap_total'] += 1
    if answer == question['correct']:
        session['skill_gap_correct'] += 1
    
    if current_question_index == len(questions) - 1:
        score = (session['skill_gap_correct'] / session['skill_gap_total']) * 100
        selected_field = session['selected_field']
        detailed_scores = {selected_field: score}
        result = TestResult(user_id=current_user.id, test_type='skill_gap', score=score, time_spent=time_spent, details=json.dumps(detailed_scores))
        db.session.add(result)
        
        if not Badge.query.filter_by(user_id=current_user.id, name="First Test Completed").first():
            badge = Badge(user_id=current_user.id, name="First Test Completed", description="Completed your first test!", icon="fas fa-trophy")
            db.session.add(badge)
        if score >= 80:
            if not Badge.query.filter_by(user_id=current_user.id, name="High Scorer").first():
                badge = Badge(user_id=current_user.id, name="High Scorer", description="Scored 80% or higher!", icon="fas fa-star")
                db.session.add(badge)
        
        notification = Notification(user_id=current_user.id, message=f"Skill Gap Test for {selected_field} completed! Score: {score:.1f}%", type="test_result")
        db.session.add(notification)
        db.session.commit()
        
        session.pop('skill_gap_questions', None)
        session.pop('skill_gap_correct', None)
        session.pop('skill_gap_total', None)
        return jsonify({'redirect': url_for('skill_gap_results')})
    
    next_question = questions[current_question_index + 1]
    return jsonify({'question': next_question, 'current_question_index': current_question_index + 1})

@app.route('/interest_test', methods=['GET'])
@login_required
def interest_test():
    selected_field = request.args.get('field', session.get('selected_field', None))
    if selected_field:
        session['selected_field'] = selected_field
        return redirect(url_for('test', type='skill_gap', field=selected_field))
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
    return render_template('assessments/interest_test.html', selected_field=None, questions=[], total_questions=0,
                          completed_questions=0, current_question_index=0, initial_time=60, active_page='interest_test',
                          notifications=notifications)

@app.route('/skill_gap_results')
@login_required
def skill_gap_results():
    latest_skill_gap = TestResult.query.filter_by(user_id=current_user.id, test_type='skill_gap').order_by(TestResult.completed_at.desc()).first()
    if not latest_skill_gap:
        flash('No skill gap test results found.', 'warning')
        return redirect(url_for('dashboard'))
    
    details = json.loads(latest_skill_gap.details)
    field = list(details.keys())[0]
    score = latest_skill_gap.score
    
    has_aptitude = TestResult.query.filter_by(user_id=current_user.id, test_type='aptitude').count() > 0
    has_personality = TestResult.query.filter_by(user_id=current_user.id, test_type='personality').count() > 0
    
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
    return render_template('skill_gap_results.html', field=field, score=score, has_aptitude=has_aptitude,
                          has_personality=has_personality, active_page='skill_gap_results', notifications=notifications)

@app.route('/career_match', methods=['GET', 'POST'])
@login_required
def career_match():
    results = TestResult.query.filter_by(user_id=current_user.id).all()
    has_aptitude = any(r.test_type == 'aptitude' for r in results)
    has_personality = any(r.test_type == 'personality' for r in results)
    has_skill_gap = any(r.test_type == 'skill_gap' for r in results)
    
    if request.method == 'POST':
        if 'take_skill_gap' in request.form and request.form['take_skill_gap'] == 'yes':
            return redirect(url_for('interest_test'))
        elif 'proceed' in request.form:
            pass  # Proceed to career matching
    
    if not (has_aptitude or has_personality or has_skill_gap):
        flash('Please complete at least one test for career matching.', 'warning')
        return redirect(url_for('dashboard'))
    
    if has_aptitude and has_personality and not has_skill_gap and request.method == 'GET':
        notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
        return render_template('prompt_skill_gap.html', active_page='career_match', notifications=notifications)
    
    career_scores = defaultdict(float)
    aptitude_scores = {}
    personality_scores = {}
    skill_scores = {}
    onet_api = get_onet_api()
    
    for result in results:
        details = json.loads(result.details) if result.details else {}
        if result.test_type == 'aptitude':
            aptitude_scores = details
            session['aptitude_score'] = result.score
        elif result.test_type == 'personality':
            personality_scores = details
            session['personality_scores'] = details
        elif result.test_type == 'skill_gap':
            skill_scores = details
            session['skill_gap_score'] = result.score
            session['skill_gap_field'] = list(details.keys())[0]
    
    for career, weights in CAREER_MAPPING.items():
        score = 0
        if has_aptitude:
            apt_score = sum(aptitude_scores.get(cat, 0) * weight / 100 for cat, weight in weights['aptitude'].items())
            score += apt_score * 0.4
        if has_personality:
            pers_score = sum(personality_scores.get(trait.strip(), 0) * weight / 100 for trait, weight in weights['personality'].items())
            score += pers_score * 0.3
        if has_skill_gap:
            skill_score = sum(skill_scores.get(skill, 0) * weight / 100 for skill, weight in weights['skills'].items())
            score += skill_score * 0.3
        
        career_data = onet_api.get_career_details(weights.get('soc_code', '15-1252.00'))
        career_scores[career] = {
            'career': career,
            'match_score': score,
            'description': weights['description'],
            'resources': weights['resources'],
            'requirements': {
                'skills': list(weights['skills'].keys()),
                'education': career_data.get('education', {}).get('typical', 'Not specified'),
                'experience': career_data.get('experience', {}).get('typical', 'Not specified')
            },
            'salary': career_data.get('wages', {}).get('median', 0),
            'scope': career_data.get('outlook', {}).get('growth_rate', 0)
        }
    
    career_matches = sorted(career_scores.values(), key=lambda x: x['match_score'], reverse=True)[:5]
    alignment_message = "Results based on "
    if has_aptitude and has_personality and has_skill_gap:
        alignment_message += "Aptitude, Personality, and Skill Gap tests."
    elif has_aptitude and has_personality:
        alignment_message += "Aptitude and Personality tests only. For more accuracy, take the Skill Gap test."
    else:
        alignment_message += "Skill Gap test only. For better accuracy, complete Aptitude and Personality tests."
    
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
    return render_template('career_match.html', career_matches=career_matches, alignment_message=alignment_message,
                          only_skill_gap_completed=has_skill_gap and not (has_aptitude or has_personality),
                          selected_field=session.get('skill_gap_field'), skill_gap_result=session.get('skill_gap_score'),
                          active_page='career_match', notifications=notifications)
    
@app.route('/career_path')
@login_required
def career_path():
    results = TestResult.query.filter_by(user_id=current_user.id).all()
    career_scores = defaultdict(float)
    for result in results:
        details = json.loads(result.details) if result.details else {}
        if result.test_type == 'skill_gap':
            for career, data in CAREER_MAPPING.items():
                for skill in data['skills']:
                    if skill in details:
                        career_scores[career] += details[skill] * 0.5
    data = {
        'labels': list(career_scores.keys()),
        'scores': [career_scores[c] for c in career_scores]
    }
    return render_template('career_path.html', data=data, active_page='career_path')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        if form.password.data:
            current_user.password = generate_password_hash(form.password.data)
        if form.profile_image.data and allowed_file(form.profile_image.data.filename):
            filename = secure_filename(f"profile_{current_user.id}.{form.profile_image.data.filename.rsplit('.', 1)[1].lower()}")
            image = Image.open(form.profile_image.data)
            image = image.resize((150, 150), Image.LANCZOS)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            current_user.profile_image = f"uploads/{filename}"
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    form.email.data = current_user.email
    tests = TestResult.query.filter_by(user_id=current_user.id).order_by(TestResult.completed_at.desc()).all()
    badges = Badge.query.filter_by(user_id=current_user.id).order_by(Badge.date_earned.desc()).all()
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
    return render_template('profile.html', user=current_user, form=form, tests=tests, badges=badges,
                          active_page='profile', notifications=notifications)
    
@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    form = ProfileForm()
    
    if form.validate_on_submit():
        # Update user details
        current_user.email = form.email.data
        if form.password.data:
            current_user.password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        current_user.mobile_number = form.mobile_number.data
        current_user.pin_code = form.pin_code.data
        if form.dob.data:
            current_user.dob = form.dob.data
        
        # Handle profile picture upload
        if form.profile_image.data:
            # Generate a unique filename based on user ID
            file_extension = form.profile_image.data.filename.rsplit('.', 1)[1].lower()
            filename = f"profile_{current_user.id}.{file_extension}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Resize and save the image
            image = Image.open(form.profile_image.data)
            image = image.resize((150, 150), Image.LANCZOS)
            image.save(filepath)
            current_user.profile_image = f"uploads/{filename}"
        
        # Update bio
        current_user.bio = form.bio.data
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    # Pre-fill the form with current user data
    if request.method == 'GET':
        form.email.data = current_user.email
        form.mobile_number.data = current_user.mobile_number
        form.pin_code.data = current_user.pin_code
        form.dob.data = current_user.dob
        form.bio.data = current_user.bio
    
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
    return render_template('profile_edit.html', form=form, user=current_user, active_page='profile', notifications=notifications)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = Message(subject=f"Contact from {form.name.data}", recipients=['abc@gmail.com'],
                      body=f"Name: {form.name.data}\nEmail: {form.email.data}\nMessage: {form.message.data}")
        try:
            mail.send(msg)
            flash('Message sent successfully!', 'success')
            return redirect(url_for('contact'))
        except Exception as e:
            flash(f'Failed to send message: {str(e)}', 'danger')
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all() if current_user.is_authenticated else []
    return render_template('contact.html', form=form, active_page='contact', notifications=notifications)

@app.route('/delete_profile_picture', methods=['POST'])
@login_required
def delete_profile_picture():
    # Delete the current profile picture file if it exists and isn’t the default
    if current_user.profile_image and current_user.profile_image != 'images/default_profile.jpg':
        try:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(current_user.profile_image))
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            flash(f'Error deleting profile picture: {str(e)}', 'danger')
    
    # Reset the profile picture to the default
    current_user.profile_image = 'images/default_profile.jpg'
    db.session.commit()
    flash('Profile picture removed successfully!', 'success')
    return redirect(url_for('profile'))

@app.route('/forgot_password')
def forgot_password():
    flash('Password reset is not yet implemented. Please contact support.', 'warning')
    return redirect(url_for('login'))

@app.route('/results')
@login_required
def results():
    latest_test = TestResult.query.filter_by(user_id=current_user.id).order_by(TestResult.completed_at.desc()).first()
    if not latest_test:
        flash('Please complete a test to view results.', 'warning')
        return redirect(url_for('test'))
    if latest_test.test_type == 'aptitude':
        score_data = {
            'score': latest_test.score,
            'correct': int(latest_test.score / 10),  # Assuming score is a percentage, adjust as needed
            'total': 10,
            'time_spent': latest_test.time_spent or 0
        }
        notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
        return render_template('results.html', score_data=score_data, active_page='results', notifications=notifications)
    elif latest_test.test_type == 'personality':
        return redirect(url_for('personality_results'))
    elif latest_test.test_type == 'skill_gap':
        return redirect(url_for('submit_interests'))
    else:
        flash('No detailed results available for this test type.', 'info')
        return redirect(url_for('dashboard'))

@app.route('/about')
def about():
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all() if current_user.is_authenticated else []
    return render_template('about.html', active_page='about', notifications=notifications)

@app.route('/faq')
def faq():
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all() if current_user.is_authenticated else []
    return render_template('faq.html', active_page='faq', notifications=notifications)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        print("Form data received:", request.form)
        if 'theme' in request.form:
            theme = request.form['theme']
            print(f"Updating theme to: {theme}")
            current_user.theme = theme
            db.session.commit()
            flash('Theme updated successfully!', 'success')
            return redirect(url_for('settings'))
        elif 'animations' in request.form:
            animations = request.form.get('animations') == 'on'
            print(f"Updating animations to: {animations}")
            current_user.animations_enabled = animations
            db.session.commit()
            flash('Animation settings updated!', 'success')
            return redirect(url_for('settings'))
        elif 'current_password' in request.form:
            current_password = request.form['current_password']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']
            if not check_password_hash(current_user.password, current_password):
                flash('Current password is incorrect.', 'danger')
            elif new_password != confirm_password:
                flash('New passwords do not match.', 'danger')
            elif len(new_password) < 8:
                flash('New password must be at least 8 characters long.', 'danger')
            else:
                current_user.password = generate_password_hash(new_password)
                db.session.commit()
                flash('Password updated successfully!', 'success')
            return redirect(url_for('settings'))
        elif 'reset_roadmap' in request.form:
            TestResult.query.filter_by(user_id=current_user.id).delete()
            db.session.commit()
            flash('Roadmap progress reset successfully!', 'success')
            return redirect(url_for('settings'))
        elif 'delete_account' in request.form:
            db.session.delete(current_user)
            db.session.commit()
            logout_user()
            flash('Your account has been deleted.', 'info')
            return redirect(url_for('index'))
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
    return render_template('settings.html', user=current_user, csrf_token=generate_csrf(), active_page='settings', notifications=notifications)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').strip()
    if not query:
        flash('Please enter a search term.', 'warning')
        return redirect(url_for('index'))
    # Search for tests and careers
    results = [
        {'title': 'Sample Test', 'type': 'test', 'url': url_for('test', type='sample')},
        {'title': 'Aptitude Test', 'type': 'test', 'url': url_for('test', type='aptitude')},
        {'title': 'Personality Test', 'type': 'test', 'url': url_for('test', type='personality')},
        {'title': 'Skill Gap Test', 'type': 'test', 'url': url_for('interest_test')},
        {'title': 'Career Assessment', 'type': 'test', 'url': url_for('career_assessment')},
        {'title': 'Software Developer', 'type': 'career', 'url': url_for('career_match')},
        {'title': 'Data Scientist', 'type': 'career', 'url': url_for('career_match')},
        {'title': 'Graphic Designer', 'type': 'career', 'url': url_for('career_match')},
        {'title': 'Business Manager', 'type': 'career', 'url': url_for('career_match')},
        {'title': 'Research Scientist', 'type': 'career', 'url': url_for('career_match')}
    ]
    # Filter results based on query
    filtered_results = [r for r in results if query.lower() in r['title'].lower()]
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all() if current_user.is_authenticated else []
    return render_template('search.html', query=query, results=filtered_results, active_page='search', notifications=notifications)

@app.route('/mark_notification_read/<int:notification_id>', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    notification.is_read = True
    db.session.commit()
    return jsonify({'success': True})

@app.errorhandler(404)
def not_found(error):
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all() if current_user.is_authenticated else []
    return render_template('404.html', active_page='404', notifications=notifications), 404

@app.errorhandler(500)
def internal_error(error):
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all() if current_user.is_authenticated else []
    return render_template('500.html', active_page='500', notifications=notifications), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5001)