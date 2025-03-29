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
from datetime import datetime, timezone
import numpy as np

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
    completed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    icon = db.Column(db.String(50), nullable=False)
    date_earned = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

# In calculate_match function (app.py)
def calculate_match(user_scores, career):
    # 1. Trait Alignment (Personality)
    trait_score = cosine_similarity(
        [list(user_scores['personality'].values())],
        [list(career['personality'].values())]
    )[0][0]

    # 2. Competency Match (Aptitude)
    apt_score = sum(
        min(user, career['aptitude'][cat]) 
        for cat, user in user_scores['aptitude'].items()
    ) / sum(career['aptitude'].values())
    
    # 3. Skill Proximity (Skill Gap)
    skill_score = 1 - abs(
        user_scores['skill_gap']['score'] - 
        career['skills']['required']
    ) / 100 if 'skill_gap' in user_scores else 0
    
    # Adaptive weights
    weights = [0.4, 0.4, 0.2] if 'skill_gap' in user_scores else [0.6, 0.4, 0.0]
    return round((
        trait_score * weights[0] +
        apt_score * weights[1] +
        skill_score * weights[2]
    ) * 100, 2)

@app.before_request
def init_session():
    if 'used_aptitude' not in session:
        session['used_aptitude'] = []
    if 'aptitude_history' not in session:
        session['aptitude_history'] = defaultdict(list)
        
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
@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return value.strftime(format)


# Generate dynamic test questions with no repeats in a session
def generate_questions(test_type):
    if test_type == 'sample':
        return [
            {"id": "q1", "question": "How do you prioritize tasks when faced with tight deadlines?", "options": ["Focus on the most urgent first", "Delegate to others", "Work on multiple tasks simultaneously", "Ask for an extension"]},
            {"id": "q2", "question": "What do you do if you notice a coworker slacking off?", "options": ["Report them to the supervisor", "Offer to help them", "Ignore it and focus on my work", "Confront them directly"]},
            {"id": "q3", "question": "How often do you take initiative on projects without being asked?", "options": ["Always", "Often", "Sometimes", "Rarely"]},
            {"id": "q4", "question": "What’s your approach to handling a mistake you made at work?", "options": ["Admit it and fix it immediately", "Fix it quietly without telling anyone", "Blame external factors", "Wait for someone to notice"]},
            {"id": "q5", "question": "How do you balance work and personal life?", "options": ["Set strict boundaries", "Work late when needed", "Integrate work into personal time", "Prioritize personal life over work"]},
            {"id": "q6", "question": "How do you respond to constructive criticism from a manager?", "options": ["Accept it and improve", "Defend my actions", "Feel discouraged but try to adapt", "Ignore it unless it’s repeated"]},
            {"id": "q7", "question": "What motivates you to meet a challenging deadline?", "options": ["Personal satisfaction", "Team success", "Avoiding consequences", "Recognition from others"]},
            {"id": "q8", "question": "How do you handle a situation where you disagree with a team decision?", "options": ["Voice my opinion and push back", "Go along but document my concerns", "Support it fully despite disagreement", "Stay silent and follow through"]},
            {"id": "q9", "question": "What’s your approach to learning new skills required for your job?", "options": ["Proactively seek training", "Learn on the job as needed", "Wait for company-provided training", "Rely on colleagues to teach me"]},
            {"id": "q10", "question": "How do you ensure your work maintains high quality under pressure?", "options": ["Double-check everything", "Stick to a proven process", "Focus on speed over perfection", "Ask for feedback before submission"]}
        ]
    elif test_type == 'aptitude':
        available_questions = copy.deepcopy(APTITUDE_QUESTIONS)
        used_questions = session.get('used_aptitude', [])
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
                difficulty_questions = [q for q in 
                    available_questions[category]['easy'] +
                    available_questions[category]['moderate'] +
                    available_questions[category]['hard'] 
                    if q['id'] not in used_questions
                ]
                continue
            question = random.choice(difficulty_questions)
            question['time_limit'] = question.get('time_limit', 60)
            questions.append(question)
            if question['id'] not in used_questions:  # Prevent duplicates
                used_questions.append(question['id'])
        
        session['aptitude_questions'] = questions
        session['used_aptitude_questions'] = used_questions
        session['aptitude_correct'] = 0
        session['aptitude_total'] = 0
        session['aptitude_category_scores'] = defaultdict(int)
        session['aptitude_category_counts'] = defaultdict(int)
        for category in APTITUDE_QUESTIONS.keys():
            if category not in session['aptitude_category_counts']:
                session['aptitude_category_counts'][category] = 0
            if category not in session['aptitude_category_scores']:
                session['aptitude_category_scores'][category] = 0
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

@app.route('/student')
@login_required
def student():
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
    return render_template('student.html', user=current_user, active_page='student', notifications=notifications)

@app.route('/degree', methods=['GET'])
@login_required
def degree():
    onet_api = get_onet_api()
    print(f"ONET_USER: {os.getenv('ONET_USER')}")
    print(f"ONET_PWD: {os.getenv('ONET_PWD')}")

    degrees = [
        {"title": "Bachelor of Science in Computer Science", "university": "University of Technology", "duration": "4 years", "description": "Focuses on programming and systems.", "degree_level": "Bachelor", "field_of_study": "Computer Science", "soc_code": "15-1132.00"},
        {"title": "Master of Business Administration", "university": "Global Business School", "duration": "2 years", "description": "Prepares for leadership roles.", "degree_level": "Master", "field_of_study": "Business", "soc_code": "11-1021.00"},
        {"title": "Bachelor of Arts in Psychology", "university": "Riverside University", "duration": "3 years", "description": "Explores human behavior.", "degree_level": "Bachelor", "field_of_study": "Psychology", "soc_code": "19-3031.00"},
        {"title": "Master of Science in Data Science", "university": "Tech Institute", "duration": "1.5 years", "description": "Analyzes big data.", "degree_level": "Master", "field_of_study": "Data Science", "soc_code": "15-2051.00"}
    ]

    mock_career_data = {
        "Bachelor of Science in Computer Science": {'job_title': 'Software Developer', 'salary': 105000, 'job_growth': 22},
        "Master of Business Administration": {'job_title': 'Business Manager', 'salary': 120000, 'job_growth': 8},
        "Bachelor of Arts in Psychology": {'job_title': 'Clinical Psychologist', 'salary': 82000, 'job_growth': 14},
        "Master of Science in Data Science": {'job_title': 'Data Scientist', 'salary': 115000, 'job_growth': 31}
    }

    degree_level = request.args.get('degree_level', '').strip()
    field_of_study = request.args.get('field_of_study', '').strip()
    duration = request.args.get('duration', '').strip()
    keyword = request.args.get('keyword', '').strip().lower()
    sort_by = request.args.get('sort_by', '').strip()

    filtered_degrees = degrees
    if degree_level: filtered_degrees = [d for d in filtered_degrees if d['degree_level'] == degree_level]
    if field_of_study: filtered_degrees = [d for d in filtered_degrees if d['field_of_study'] == field_of_study]
    if duration: filtered_degrees = [d for d in filtered_degrees if d['duration'] == duration]
    if keyword: filtered_degrees = [d for d in filtered_degrees if keyword in d['university'].lower() or keyword in d['title'].lower()]
    if sort_by == 'title': filtered_degrees.sort(key=lambda x: x['title'])
    elif sort_by == 'duration': filtered_degrees.sort(key=lambda x: float(x['duration'].split()[0]))
    elif sort_by == 'university': filtered_degrees.sort(key=lambda x: x['university'])

    for degree in filtered_degrees:
        try:
            career_data = onet_api.get_career_details(degree['soc_code'])
            degree['career_data'] = {
                'job_title': career_data.get('title', 'N/A'),
                'salary': career_data.get('wages', {}).get('median', 'N/A'),
                'job_growth': career_data.get('outlook', {}).get('growth_rate', 'N/A')
            }
        except Exception as e:
            print(f"Error fetching career data for {degree['title']}: {e}")
            degree['career_data'] = mock_career_data.get(degree['title'], {
                'job_title': 'N/A',
                'salary': 'N/A',
                'job_growth': 'N/A'
            })
            flash(f"Failed to fetch career data for {degree['title']}. Using mock data.", 'warning')

    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
    return render_template('degree.html', user=current_user, degrees=filtered_degrees, active_page='degree', notifications=notifications)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next', url_for('dashboard'))
            flash('Logged in successfully!', 'success')
            return redirect(next_page)
        else:
            flash('Invalid username or password.', 'danger')
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all() if current_user.is_authenticated else []
    return render_template('auth/login.html', form=form, active_page='login', notifications=notifications)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        captcha = form.captcha.data
        if captcha != '5':
            flash('Verification failed. Please enter the correct answer (2 + 3 = 5).', 'danger')
        elif User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
        elif email and User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password, email=email)
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
    
    # Generate test labels and scores for the chart
    test_labels = [test.completed_at.strftime('%Y-%m-%d') for test in tests]
    test_scores = [test.score for test in tests]
    
    return render_template('dashboard.html', 
                          user=current_user, 
                          tests=tests, 
                          badges=badges, 
                          notifications=notifications,
                          available_tests=available_tests, 
                          can_proceed=can_proceed,
                          test_labels=test_labels,
                          test_scores=test_scores,
                          active_page='dashboard')

@app.route('/test', methods=['GET', 'POST'])
@login_required
def test():
    test_type = request.args.get('type')
    instructions = {
        "time_limit": "You have 10 minutes to complete this test.",
        "honesty": "Please answer all questions honestly and without external assistance.",
        "scientific_accuracy": "This test is designed to assess your skills with validated questions."
    }
    
    if test_type == 'sample':
        questions = generate_questions('sample')
        if request.method == 'POST':
            if request.form:
                answers = {}
                for q in questions:
                    answer = request.form.get(q['id'])
                    if answer is not None:
                        answers[q['id']] = int(answer)
                    else:
                        flash('Please answer all questions before submitting.', 'danger')
                        notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all() if current_user.is_authenticated else []
                        return render_template('sample_test.html', questions=questions, instructions=instructions, active_page='test', test_type='sample', notifications=notifications)
                score = sum(3 - answers[q['id']] for q in questions)
                max_score = len(questions) * 3
                if current_user.is_authenticated:
                    result = TestResult(
                        user_id=current_user.id,
                        test_type='sample',
                        score=score
                    )
                    db.session.add(result)
                    if not Badge.query.filter_by(user_id=current_user.id, name="First Test Completed").first():
                        badge = Badge(user_id=current_user.id, name="First Test Completed", description="Completed your first test!", icon="fas fa-trophy")
                        db.session.add(badge)
                    if score >= 0.8 * max_score:
                        if not Badge.query.filter_by(user_id=current_user.id, name="High Scorer").first():
                            badge = Badge(user_id=current_user.id, name="High Scorer", description="Scored 80% or higher on a test!", icon="fas fa-star")
                            db.session.add(badge)
                    notification = Notification(
                        user_id=current_user.id,
                        message=f"You completed the Sample Test with a score of {score}/{max_score}!",
                        type="test_result"
                    )
                    db.session.add(notification)
                    db.session.commit()
                flash(f'Your work ethics score: {score} out of {max_score}', 'success')
                return redirect(url_for('index'))
        notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all() if current_user.is_authenticated else []
        return render_template('sample_test.html', questions=questions, instructions=instructions, active_page='test', test_type='sample', notifications=notifications)


    elif test_type == 'aptitude':
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

@app.route('/career_assessment', methods=['GET'])
def career_assessment():
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all() if current_user.is_authenticated else []
    return render_template('career_assessment.html',active_page='career_assessment', notifications=notifications)

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
    session.setdefault('skill_gap_total', 0)
    session.setdefault('skill_gap_correct', 0)
    
    current_response = responses[-1]
    question_id = current_response['questionId']
    answer = int(current_response['answer'])
    question = next((q for q in questions if q['id'] == question_id), None)
    if not question:
        return jsonify({'error': 'Question not found'}), 400
    
    session['skill_gap_total'] += 1
    if answer == question['correct']:
        session['skill_gap_correct'] += 1
    
    # Mark session as modified
    session.modified = True
    
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
    result = TestResult.query.filter_by(
        user_id=current_user.id, 
        test_type='skill_gap'
    ).order_by(TestResult.completed_at.desc()).first()
    
    if not result:
        flash('No skill gap results found', 'warning')
        return redirect(url_for('dashboard'))
    
    details = json.loads(result.details)
    field = list(details.keys())[0]
    score = result.score
    
    recommendations = get_recommendations(field, score)
    
    return render_template('skill_gap_results.html',
        field=field,
        score=score,
        recommendations=recommendations,
        has_aptitude=TestResult.query.filter_by(
            user_id=current_user.id,
            test_type='aptitude'
        ).count() > 0,
        has_personality=TestResult.query.filter_by(
            user_id=current_user.id,
            test_type='personality'
        ).count() > 0
    )
# Three-tiered matching algorithm


@app.route('/submit_career_assessment', methods=['POST'])
@login_required
def submit_career_assessment():
    if not request.form.get('csrf_token'):
        return "CSRF token missing", 400
    
    # Collect responses from the form
    responses = {
        'q1': request.form.get('q1'),
        'q2': request.form.get('q2'),
        'q3': request.form.get('q3'),
        'q4': request.form.get('q4'),
        'q5': request.form.get('q5'),
        'q6': request.form.get('q6'),
        'q7': request.form.get('q7'),
        'q8': request.form.get('q8'),
        'q9': request.form.get('q9'),
        'q10': request.form.get('q10')
    }

    # Check if all questions are answered
    if None in responses.values():
        flash('Please answer all questions before submitting.', 'danger')
        return redirect(url_for('career_assessment'))

    # Calculate interest scores based on responses
    interest_scores = defaultdict(int)
    fields = ['Software Development', 'Data Science', 'Graphic Design', 'Business Management', 'Scientific']
    for field in fields:
        for q in ['q1', 'q2', 'q3', 'q4', 'q5']:
            if responses[q] == field:
                interest_scores[field] += 20  # 20 points per match (max 100)

    # Calculate a simple score (e.g., number of specific career interests)
    score = sum(1 for v in responses.values() if v in fields)

    # Save result to database
    result = TestResult(
        user_id=current_user.id,
        test_type='career_interest',
        score=score,
        details=json.dumps({**responses, 'interest_scores': dict(interest_scores)}),
        time_spent=0  # Add timing logic if desired
    )
    db.session.add(result)
    
    # Award badges and notifications
    if not Badge.query.filter_by(user_id=current_user.id, name="First Test Completed").first():
        badge = Badge(
            user_id=current_user.id,
            name="First Test Completed",
            description="Completed your first test!",
            icon="fas fa-trophy"
        )
        db.session.add(badge)
    
    top_field = max(interest_scores, key=interest_scores.get, default="None")
    notification = Notification(
        user_id=current_user.id,
        message=f"You completed the Career Assessment! Top interest: {top_field} ({interest_scores[top_field]}%)",
        type="test_result"
    )
    db.session.add(notification)
    db.session.commit()

    return redirect(url_for('interest_results', result_id=result.id))

@app.route('/career_match')
@login_required
def career_match():
    user_scores = {}
    tests = TestResult.query.filter_by(user_id=current_user.id).all()
    
    # Collect scores
    for test in tests:
        if test.test_type == 'personality':
            user_scores['personality'] = json.loads(test.details)
        elif test.test_type == 'aptitude':
            user_scores['aptitude'] = json.loads(test.details)
        elif test.test_type == 'skill_gap':
            user_scores['skill_gap'] = {
                'field': list(json.loads(test.details).keys()[0]),
                'score': test.score
            }
    
    # Calculate matches
    matches = []
    for career, data in CAREER_MAPPING.items():
        score = calculate_match(user_scores, data)
        matches.append({
            'name': career,
            'score': score,
            'details': data,
            'resources': get_recommendations(
                data['interests'][0], 
                user_scores.get('skill_gap', {}).get('score', 0)
            )
        })
    
    matches.sort(key=lambda x: x['score'], reverse=True)
    
    # Determine completion status
    completed = {
        'aptitude': 'aptitude' in user_scores,
        'personality': 'personality' in user_scores,
        'skill_gap': 'skill_gap' in user_scores
    }
    
    return render_template('career_match.html',
        matches=matches[:5],
        completed=completed,
        has_skill_gap='skill_gap' in user_scores
    )

def generate_career_matches(test_results, include_skill_gap):
    career_scores = defaultdict(float)
    weights = CAREER_MAPPING
    
    # Basic scoring (aptitude + personality)
    if test_results['aptitude'] and test_results['personality']:
        apt_scores = json.loads(test_results['aptitude'].details)
        pers_scores = json.loads(test_results['personality'].details)
        
        for career, data in weights.items():
            apt_score = sum(apt_scores.get(cat, 0) * weight/100 
                          for cat, weight in data['aptitude'].items())
            pers_score = sum(pers_scores.get(trait, 0) * weight/100 
                           for trait, weight in data['personality'].items())
            career_scores[career] = (apt_score * 0.6) + (pers_score * 0.4)
    
    # Enhanced scoring with skill gap
    if include_skill_gap and test_results['skill_gap']:
        skill_scores = json.loads(test_results['skill_gap'].details)
        field = list(skill_scores.keys())[0]
        
        for career, data in weights.items():
            if field.lower() in career.lower():
                skill_weight = sum(skill_scores[field] * weight/100 
                                 for skill, weight in data['skills'].items())
                career_scores[career] = career_scores.get(career, 0) * 0.7 + skill_weight * 0.3
    
    # Get top 5 careers and render results
    top_careers = sorted(career_scores.items(), key=lambda x: x[1], reverse=True)[:5]
    return render_template('career_results.html', careers=top_careers)

def render_full_analysis(test_results):
    # Combine all test data for detailed analysis
    analysis_data = {
        'aptitude': json.loads(test_results['aptitude'].details),
        'personality': json.loads(test_results['personality'].details),
        'skill_gap': json.loads(test_results['skill_gap'].details)
    }
    return render_template('full_analysis.html', analysis=analysis_data)

WEIGHTS = {
    'base': {'aptitude': 0.4, 'personality': 0.4, 'skill_gap': 0.2},
    'partial': {'aptitude': 0.6, 'personality': 0.4},
    'skill_only': {'skill_gap': 1.0}
}

def calculate_match(user_scores, career):
    """Calculate career fit using adaptive weighting"""
    scores = {}
    weights = WEIGHTS['base']  # Default weights
    
    # Determine weighting scheme based on available data
    if not user_scores.get('personality') and not user_scores.get('aptitude'):
        weights = WEIGHTS['skill_only']
    elif not user_scores.get('skill_gap'):
        weights = WEIGHTS['partial']
    
    total = 0
    max_possible = 0
    
    # Personality component
    if 'personality' in user_scores and 'personality' in weights:
        for trait, score in user_scores['personality'].items():
            career_trait = career['personality'].get(trait, 50)
            trait_match = 1 - abs(score - career_trait)/100
            total += weights['personality'] * trait_match
            max_possible += weights['personality']
    
    # Aptitude component  
    if 'aptitude' in user_scores and 'aptitude' in weights:
        for category, score in user_scores['aptitude'].items():
            career_apt = career['aptitude'].get(category, 50)
            apt_match = score/100 * (career_apt/100)
            total += weights['aptitude'] * apt_match
            max_possible += weights['aptitude']
    
    # Skill gap component
    if 'skill_gap' in user_scores and 'skill_gap' in weights:
        skill_match = user_scores['skill_gap']['score']/100
        total += weights['skill_gap'] * skill_match
        max_possible += weights['skill_gap']
    
    return (total / max_possible) * 100 if max_possible > 0 else 0

def get_recommendations(field, score):
    """Get personalized learning recommendations"""
    levels = ['basic', 'intermediate', 'advanced']
    level = np.digitize(score, [40, 70]) 
    return LEARNING_RESOURCES.get(field, {}).get(levels[level], [])

@app.route('/interest_results/<int:result_id>')
@login_required
def interest_results(result_id):
    result = TestResult.query.get_or_404(result_id)
    if result.user_id != current_user.id:
        flash('You do not have permission to view this result.', 'danger')
        return redirect(url_for('dashboard'))
    
    details = json.loads(result.details)
    interest_scores = details.get('interest_scores', {})
    categories = [(field, score) for field, score in interest_scores.items()]
    categories.sort(key=lambda x: x[1], reverse=True)
    
    recommendations = []
    soc_codes = {
        "Software Development": "15-1132.00",
        "Data Science": "15-2051.00",
        "Graphic Design": "27-1024.00",
        "Business Management": "11-1021.00",
        "Scientific": "19-1042.00"
    }
    for career, score in categories[:3]:  # Top 3 careers
        recommendations.append({
            'career': career,
            'link': f"https://www.onetonline.org/link/summary/{soc_codes.get(career, '15-1132.00')}"
        })
    
    return render_template(
        'interest_results.html',
        categories=categories,
        recommendations=recommendations
    )
   
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

@app.route('/resources')
@login_required
def resources():
    # Determine the user's career path
    career_path = session.get('selected_field', 'Software Development')
    if career_path not in CAREER_MAPPING:
        career_path = 'Software Development'
    
    # Fetch resources for the career path
    resources = LEARNING_RESOURCES.get(career_path, [])
    
    # Fetch notifications
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
    
    return render_template('resources.html',
                          user=current_user,
                          career_path=career_path,
                          resources=resources,
                          active_page='resources',
                          notifications=notifications)
    
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

@app.route('/progress_tracking')
@login_required
def progress_tracking():
    # Fetch test history
    test_history = TestResult.query.filter_by(user_id=current_user.id).order_by(TestResult.completed_at.asc()).all()
    total_tests = len(test_history)
    if total_tests == 0:
        flash('No tests taken yet. Take a test to track your progress!', 'info')
        return redirect(url_for('test'))

    # Calculate average scores for each test type
    test_types = ['sample', 'aptitude', 'personality']
    avg_scores = {}
    for test_type in test_types:
        tests = [test for test in test_history if test.test_type == test_type]
        if tests:
            max_score = 9 if test_type == 'sample' else (5 if test_type == 'personality' else 10)
            avg_scores[test_type] = sum(test.score for test in tests) / len(tests) / max_score * 100
        else:
            avg_scores[test_type] = 0

    # Prepare progress data for chart
    progress_data = {
        'labels': [test.completed_at.strftime('%Y-%m-%d') for test in test_history],
        'scores': [(test.score / (9 if test.test_type == 'sample' else (5 if test.test_type == 'personality' else 10)) * 100) for test in test_history],
        'types': [test.test_type for test in test_history]
    }

    # Define tasks based on roadmap milestones
    career_path = session.get('selected_field', 'Software Development')
    if career_path not in CAREER_MAPPING:
        career_path = 'Software Development'

    tasks = [
        {
            "name": "Complete Initial Assessment",
            "id": "assessment",
            "completed": any(result.test_type == 'aptitude' for result in test_history)
        },
        {
            "name": "Enroll in Relevant Courses",
            "id": "courses",
            "completed": False  # Replace with real course enrollment data if available
        },
        {
            "name": "Practice Career-Specific Skills",
            "id": "skills",
            "completed": any(result.test_type == 'skill_gap' and career_path in json.loads(result.details) for result in test_history)
        },
        {
            "name": "Build a Portfolio",
            "id": "portfolio",
            "completed": False  # Replace with real portfolio/project data if available
        },
        {
            "name": "Apply for Opportunities",
            "id": "opportunities",
            "completed": False  # Replace with real job application data if available
        }
    ]

    # Calculate task-based progress
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task["completed"])
    progress_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

    # Fetch notifications
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()

    return render_template('progress_tracking.html',
                          user=current_user,
                          test_history=test_history,
                          avg_scores=avg_scores,
                          progress_data=progress_data,
                          tasks=tasks,
                          progress_percentage=progress_percentage,
                          total_tests=total_tests,
                          active_page='progress_tracking',
                          notifications=notifications)

@app.route('/roadmap')
@login_required
def roadmap():
    # Fetch test history for the user, ordered by completion date
    test_history = TestResult.query.filter_by(user_id=current_user.id).order_by(TestResult.completed_at.asc()).all()
    total_tests = len(test_history)

    # Determine the user's career path from the session, default to 'Software Development'
    career_path = session.get('selected_field', 'Software Development')
    if career_path not in CAREER_MAPPING:
        career_path = 'Software Development'

    # Define career goals and milestones for different career paths
    career_roadmaps = {
        "Software Development": {
            "career_goal": "Senior Software Engineer",
            "milestones": [
                {
                    "title": "Completed Aptitude Test",
                    "description": "Assessed core skills",
                    "details": "Evaluated logical reasoning, problem-solving, and basic technical knowledge.",
                    "date": next((t.completed_at for t in test_history if t.test_type == 'aptitude'), None),
                    "type": "test",
                    "completed": any(t.test_type == 'aptitude' for t in test_history),
                    "progress": 100 if any(t.test_type == 'aptitude' for t in test_history) else 0
                },
                {
                    "title": "Skill Gap Assessment",
                    "description": "Evaluated coding skills",
                    "details": "Assessed proficiency in Python, JavaScript, and software development fundamentals.",
                    "date": next((t.completed_at for t in test_history if t.test_type == 'skill_gap' and 'Software Development' in json.loads(t.details)), None),
                    "type": "test",
                    "completed": any(t.test_type == 'skill_gap' and 'Software Development' in json.loads(t.details) for t in test_history),
                    "progress": 100 if any(t.test_type == 'skill_gap' and 'Software Development' in json.loads(t.details) for t in test_history) else 0
                },
                {
                    "title": "First Project",
                    "description": "Built a basic application",
                    "details": "Developed a to-do list app using HTML, CSS, and JavaScript.",
                    "date": datetime(2025, 3, 10),  # Simulated date; replace with real data if available
                    "type": "project",
                    "completed": False,  # Replace with real data (e.g., check if project exists in a Project model)
                    "progress": 50  # Simulated partial progress; replace with real data
                },
                {
                    "title": "Portfolio Creation",
                    "description": "Showcased projects",
                    "details": "Created a portfolio website with 3 projects, hosted on GitHub Pages.",
                    "date": datetime(2025, 3, 15),  # Simulated date; replace with real data
                    "type": "project",
                    "completed": False,  # Replace with real data
                    "progress": 30  # Simulated partial progress; replace with real data
                },
                {
                    "title": "Job Application",
                    "description": "Applied to entry-level roles",
                    "details": "Submitted applications to 5 software development positions.",
                    "date": datetime(2025, 3, 20),  # Simulated date; replace with real data
                    "type": "job",
                    "completed": False,  # Replace with real data
                    "progress": 20  # Simulated partial progress; replace with real data
                }
            ]
        },
        "Data Science": {
            "career_goal": "Lead Data Scientist",
            "milestones": [
                {
                    "title": "Completed Aptitude Test",
                    "description": "Assessed analytical skills",
                    "details": "Evaluated mathematical reasoning, statistics, and problem-solving abilities.",
                    "date": next((t.completed_at for t in test_history if t.test_type == 'aptitude'), None),
                    "type": "test",
                    "completed": any(t.test_type == 'aptitude' for t in test_history),
                    "progress": 100 if any(t.test_type == 'aptitude' for t in test_history) else 0
                },
                {
                    "title": "Skill Gap Assessment",
                    "description": "Evaluated data skills",
                    "details": "Assessed proficiency in Python, R, and data analysis techniques.",
                    "date": next((t.completed_at for t in test_history if t.test_type == 'skill_gap' and 'Data Science' in json.loads(t.details)), None),
                    "type": "test",
                    "completed": any(t.test_type == 'skill_gap' and 'Data Science' in json.loads(t.details) for t in test_history),
                    "progress": 100 if any(t.test_type == 'skill_gap' and 'Data Science' in json.loads(t.details) for t in test_history) else 0
                },
                {
                    "title": "Statistics Mastery",
                    "description": "Completed stats course",
                    "details": "Finished an online course on advanced statistics and probability.",
                    "date": datetime(2025, 3, 12),  # Simulated date; replace with real data
                    "type": "course",
                    "completed": False,  # Replace with real data (e.g., check if course is completed in a CourseEnrollment model)
                    "progress": 70  # Simulated partial progress; replace with real data
                },
                {
                    "title": "Data Project",
                    "description": "Analyzed a dataset",
                    "details": "Performed exploratory data analysis on a public dataset using Pandas and Matplotlib.",
                    "date": datetime(2025, 3, 18),  # Simulated date; replace with real data
                    "type": "project",
                    "completed": False,  # Replace with real data
                    "progress": 40  # Simulated partial progress; replace with real data
                },
                {
                    "title": "Research Publication",
                    "description": "Published findings",
                    "details": "Published a research paper on machine learning applications in a journal.",
                    "date": datetime(2025, 3, 25),  # Simulated date; replace with real data
                    "type": "publication",
                    "completed": False,  # Replace with real data
                    "progress": 10  # Simulated partial progress; replace with real data
                }
            ]
        }
    }

    # Get roadmap data for the user's career path, default to Software Development if not found
    roadmap_data = career_roadmaps.get(career_path, career_roadmaps["Software Development"])
    milestones = roadmap_data["milestones"]

    # Fetch unread notifications for the user, limited to the 5 most recent
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()

    # Get the current date as an offset-naive datetime to match the offset-naive dates in milestones
    # We use datetime.now(timezone.utc) to get the current time in UTC, then remove the timezone info
    current_date = datetime.now(timezone.utc).replace(tzinfo=None)

    # Render the roadmap template with the necessary data
    return render_template('roadmap.html',
                          user=current_user,
                          career_goal=roadmap_data["career_goal"],
                          milestones=milestones,
                          career_path=career_path,
                          current_date=current_date,  # Pass the offset-naive datetime
                          animations_enabled=current_user.animations_enabled,
                          active_page='roadmap',
                          notifications=notifications)

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