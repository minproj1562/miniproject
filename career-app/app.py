import os
import sys
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect, generate_csrf
from werkzeug.utils import secure_filename
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
import logging

# Import question data
from questions import (
    APTITUDE_QUESTIONS, PERSONALITY_QUESTIONS, SCORING_KEY,
    CAREER_MAPPING, SKILL_GAP_QUESTIONS, LEARNING_RESOURCES, ADAPTIVE_TEST_SETTINGS
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
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def cosine_similarity(a, b):
    a = np.array(a, dtype=float).flatten()  # Ensure 1D and numeric
    b = np.array(b, dtype=float).flatten()
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=True)
    animations_enabled = db.Column(db.Boolean, default=True, nullable=False)
    # New fields for settings
    theme = db.Column(db.String(10), default='light', nullable=False)  # For theme preference
    notify_test_reminders = db.Column(db.Boolean, default=True, nullable=False)  # Notification preferences
    notify_badge_earned = db.Column(db.Boolean, default=True, nullable=False)
    notify_progress_updates = db.Column(db.Boolean, default=True, nullable=False)
    email_notifications = db.Column(db.Boolean, default=True, nullable=False)  # Email preferences
    email_newsletters = db.Column(db.Boolean, default=False, nullable=False)
    profile_visibility = db.Column(db.String(10), default='public', nullable=False)  # Profile visibility
    preferred_test_categories = db.Column(db.JSON, default=lambda: [], nullable=False)  # Preferred test categories
    # Existing relationships
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

def get_recommendations(field, score):
    """Get personalized learning recommendations"""
    levels = ['basic', 'intermediate', 'advanced']
    level = np.digitize(score, [40, 70]) 
    return LEARNING_RESOURCES.get(field, {}).get(levels[level], [])
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

    def get_skills_for_occupation(self, soc_code):
        # Mock skills data
        return [
            {'name': 'Programming'},
            {'name': 'Problem Solving'},
            {'name': 'Teamwork'},
            {'name': 'Communication'},
            {'name': 'Critical Thinking'}
        ]

    def get_education_for_occupation(self, soc_code):
        # Mock education data
        return {
            'typical_level': 'Bachelor’s Degree'
        }
        
def get_onet_api():
    """Return instances of ONetAPI and EdxAPI."""
    return ONetAPI(), EdxAPI()

class EdxAPI:
    def search_courses(self, subject=None, limit=5):
        # Mock course data for EdxAPI
        courses = [
            {"title": "Introduction to Computer Science", "university": "MITx", "duration": "Self-paced", "description": "Learn the basics of computer science.", "degree_level": "Beginner", "field_of_study": "Computer Science", "country": "USA"},
            {"title": "Data Science Fundamentals", "university": "HarvardX", "duration": "Self-paced", "description": "Introduction to data science concepts.", "degree_level": "Intermediate", "field_of_study": "Data Science", "country": "USA"},
            {"title": "Business Analytics", "university": "ColumbiaX", "duration": "Self-paced", "description": "Learn business analytics techniques.", "degree_level": "Intermediate", "field_of_study": "Business", "country": "USA"},
            {"title": "Graphic Design Basics", "university": "CalArts", "duration": "Self-paced", "description": "Introduction to graphic design principles.", "degree_level": "Beginner", "field_of_study": "Graphic Design", "country": "USA"},
            {"title": "Psychology 101", "university": "Yale", "duration": "Self-paced", "description": "Explore the basics of psychology.", "degree_level": "Beginner", "field_of_study": "Psychology", "country": "USA"}
        ]
        if subject:
            courses = [course for course in courses if course['field_of_study'] == subject]
        return courses[:limit]
    
def get_indian_courses(field_of_study=None, degree_level=None, limit=5):
    """
    Fetch mock course data for India.
    
    Args:
        field_of_study (str, optional): The field of study to filter courses.
        degree_level (str, optional): The degree level to filter courses.
        limit (int): The maximum number of courses to return.
        
    Returns:
        list: A list of mock courses.
    """
    indian_courses = [
        {"title": "Bachelor of Technology in Computer Science", "university": "IIT Delhi", "duration": "4 years", "description": "Comprehensive program in computer science and engineering.", "degree_level": "Bachelor", "field_of_study": "Computer Science", "country": "India"},
        {"title": "Master of Business Administration", "university": "IIM Ahmedabad", "duration": "2 years", "description": "Premier MBA program for business leaders.", "degree_level": "Master", "field_of_study": "Business", "country": "India"},
        {"title": "Bachelor of Science in Data Science", "university": "Christ University, Bangalore", "duration": "3 years", "description": "Focuses on data analysis and machine learning.", "degree_level": "Bachelor", "field_of_study": "Data Science", "country": "India"},
        {"title": "Master of Arts in Psychology", "university": "University of Mumbai", "duration": "2 years", "description": "Advanced study of human behavior and mental processes.", "degree_level": "Master", "field_of_study": "Psychology", "country": "India"},
        {"title": "Bachelor of Design in Graphic Design", "university": "NID Ahmedabad", "duration": "4 years", "description": "Specialization in visual communication and design.", "degree_level": "Bachelor", "field_of_study": "Graphic Design", "country": "India"}
    ]
    
    filtered_courses = indian_courses
    if field_of_study:
        filtered_courses = [course for course in filtered_courses if course['field_of_study'] == field_of_study]
    if degree_level:
        filtered_courses = [course for course in filtered_courses if course['degree_level'] == degree_level]
    return filtered_courses[:limit]

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
    # Use initial difficulty from ADAPTIVE_TEST_SETTINGS
        current_difficulty = ADAPTIVE_TEST_SETTINGS['initial_difficulty']  # 'easy'
    
    # Ensure we have enough questions
        total_available = sum(
            sum(len(questions) for difficulty, questions in category.items())
            for category in available_questions.values()
        )
        if total_available < 10:
            raise ValueError(f"Not enough questions available. Required: 10, Available: {total_available}")

    # Generate 10 questions
        for _ in range(10):
        # Choose a category randomly
            category = random.choice(list(available_questions.keys()))
        # Filter questions by current difficulty and exclude used questions
            difficulty_questions = [
               q for q in available_questions[category][current_difficulty]
               if q['id'] not in used_questions
            ]
        # If no questions at current difficulty, try other difficulties
            if not difficulty_questions:
                for diff in ['easy', 'moderate', 'hard']:
                    if diff != current_difficulty:
                        difficulty_questions = [
                            q for q in available_questions[category][diff]
                            if q['id'] not in used_questions
                        ]
                        if difficulty_questions:
                            current_difficulty = diff
                            break
        # If still no questions, use any available question from the category
            if not difficulty_questions:
                difficulty_questions = [
                    q for q in (
                        available_questions[category]['easy'] +
                        available_questions[category]['moderate'] +
                        available_questions[category]['hard']
                    )
                    if q['id'] not in used_questions
                ]
                if not difficulty_questions:
                # If no questions are available in this category, remove it and try again
                    del available_questions[category]
                    if not available_questions:
                        raise ValueError("Ran out of questions to select.")
                    continue
        # Select a question
            question = random.choice(difficulty_questions)
            question['time_limit'] = question.get('time_limit', 60)
            questions.append(question)
            used_questions.append(question['id'])

        session['aptitude_questions'] = questions
        session['used_aptitude'] = used_questions
        session['aptitude_correct'] = 0
        session['aptitude_total'] = 0
        session['aptitude_category_scores'] = defaultdict(int)
        session['aptitude_category_counts'] = defaultdict(int)
        for category in APTITUDE_QUESTIONS.keys():
           session['aptitude_category_counts'][category] = 0
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
    onet_api, edx_api = get_onet_api()

    # Get filter parameters
    degree_level = request.args.get('degree_level', '').strip()
    field_of_study = request.args.get('field_of_study', '').strip()
    duration = request.args.get('duration', '').strip()
    country = request.args.get('country', '').strip()
    university = request.args.get('university', '').strip()
    keyword = request.args.get('keyword', '').strip().lower()
    sort_by = request.args.get('sort_by', '').strip()

    # Fetch international courses from Edx API
    edx_courses = edx_api.search_courses(subject=field_of_study if field_of_study else None, limit=5)

    # Fetch Indian courses (mock data)
    indian_courses = get_indian_courses(field_of_study=field_of_study, degree_level=degree_level, limit=5)

    # Combine all courses
    degrees = edx_courses + indian_courses

    # Add SOC codes for O*NET lookup (mock mapping for now)
    soc_mapping = {
        "Computer Science": "15-1132.00",
        "Business": "11-1021.00",
        "Psychology": "19-3031.00",
        "Data Science": "15-2051.00",
        "Graphic Design": "27-1024.00"
    }
    for degree in degrees:
        degree['soc_code'] = soc_mapping.get(degree['field_of_study'], "15-1132.00")

    # Apply filters
    filtered_degrees = degrees
    if degree_level:
        filtered_degrees = [d for d in filtered_degrees if d['degree_level'] == degree_level]
    if field_of_study:
        filtered_degrees = [d for d in filtered_degrees if d['field_of_study'] == field_of_study]
    if duration:
        filtered_degrees = [d for d in filtered_degrees if d.get('duration') == duration]
    if country:
        filtered_degrees = [d for d in filtered_degrees if d.get('country') == country]
    if university:
        filtered_degrees = [d for d in filtered_degrees if d['university'] == university]
    if keyword:
        filtered_degrees = [d for d in filtered_degrees if keyword in d['university'].lower() or keyword in d['title'].lower()]
    if sort_by == 'title':
        filtered_degrees.sort(key=lambda x: x['title'])
    elif sort_by == 'duration':
        filtered_degrees.sort(key=lambda x: float(x['duration'].split()[0]) if x['duration'] != 'Self-paced' else float('inf'))
    elif sort_by == 'university':
        filtered_degrees.sort(key=lambda x: x['university'])

    # Fetch career data from O*NET
    for degree in filtered_degrees:
        try:
            career_data = onet_api.get_career_details(degree['soc_code'])
            degree['career_data'] = {
                'job_title': career_data.get('title', 'N/A'),
                'salary': career_data.get('wages', {}).get('median', 'N/A'),
                'job_growth': career_data.get('outlook', {}).get('growth_rate', 'N/A')
            }
            # Fetch skills and education
            degree['skills'] = [skill.get('name', 'N/A') for skill in onet_api.get_skills_for_occupation(degree['soc_code'])[:5]]
            degree['education'] = onet_api.get_education_for_occupation(degree['soc_code'])
        except Exception as e:
            print(f"Error fetching career data for {degree['title']}: {e}")
            degree['career_data'] = {
                'job_title': 'N/A',
                'salary': 'N/A',
                'job_growth': 'N/A'
            }
            degree['skills'] = []
            degree['education'] = {}
            flash(f"Failed to fetch career data for {degree['title']}.", 'warning')

    # Get unique countries and universities for dropdowns
    countries = sorted(set(d['country'] for d in degrees if d.get('country')))
    universities = sorted(set(d['university'] for d in degrees))
    degree_levels = sorted(set(d['degree_level'] for d in degrees))
    fields_of_study = sorted(set(d['field_of_study'] for d in degrees))
    durations = sorted(set(d['duration'] for d in degrees if d.get('duration')))

    # Render the template with filtered degrees and dropdown options
    return render_template(
        'degree.html',
        degrees=filtered_degrees,
        countries=countries,
        universities=universities,
        degree_levels=degree_levels,
        fields_of_study=fields_of_study,
        durations=durations,
        selected_degree_level=degree_level,
        selected_field_of_study=field_of_study,
        selected_duration=duration,
        selected_country=country,
        selected_university=university,
        keyword=keyword,
        sort_by=sort_by
    )

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
    
    # Use session's completed_tests if available, otherwise build from test history
    completed_tests = session.get('completed_tests', [t.test_type for t in tests])
    test_results = session.get('test_results', {})
    
    # Build test_results from TestResult if not in session
    for test in tests:
        if test.test_type not in test_results:
            test_results[test.test_type] = {'score': test.score}
    session['test_results'] = test_results

    # Generate test labels and scores for the chart
    test_labels = [test.completed_at.strftime('%Y-%m-%d') for test in tests]
    test_scores = [test.score for test in tests]
    
    # Calculate average score and recommendation
    recent_tests = [t for t in tests if t.test_type in ['aptitude', 'personality', 'skill_gap']]
    max_score = 10  # Adjust based on your scoring system
    recommendation = "Take more tests to improve your skills!" if len(recent_tests) < 3 else "Great job! Consider exploring career matches."

    return render_template('dashboard.html', 
                          user=current_user, 
                          tests=tests, 
                          recent_tests=recent_tests,
                          badges=badges, 
                          notifications=notifications,
                          completed_tests=completed_tests,
                          test_results=test_results,
                          test_labels=test_labels,
                          test_scores=test_scores,
                          max_score=max_score,
                          recommendation=recommendation,
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

    # Enforce test sequence
    completed_tests = session.get('completed_tests', [])
    if test_type == 'personality' and 'aptitude' not in completed_tests:
        flash('Please complete the Aptitude Test before taking the Personality Test.', 'warning')
        return redirect(url_for('dashboard'))
    if test_type == 'skill_gap' and ('aptitude' not in completed_tests or 'personality' not in completed_tests):
        flash('Please complete both the Aptitude and Personality Tests before taking the Skill Gap Test.', 'warning')
        return redirect(url_for('dashboard'))

    if not test_type:
        flash('Please select a test type (e.g., aptitude, personality, skill_gap).', 'warning')
        return redirect(url_for('dashboard'))

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
        # Clear previous session data to start fresh
        session.pop('aptitude_questions', None)
        session.pop('aptitude_responses', None)
        session.pop('ability_estimate', None)
        session.pop('used_aptitude', None)  # Correct key
        session.pop('aptitude_correct', None)
        session.pop('aptitude_total', None)
        session.pop('aptitude_category_scores', None)
        session.pop('aptitude_category_counts', None)

        # Generate questions
        questions = generate_questions('aptitude')
        if not questions:
            flash('No aptitude questions available at this time.', 'danger')
            return redirect(url_for('dashboard'))

        # Initialize session data
        session['aptitude_responses'] = []
        session['ability_estimate'] = 0.0

        current_question_index = int(request.args.get('q', 0))
        if current_question_index >= len(questions):
            return redirect(url_for('aptitude_results'))

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
            return redirect(url_for('skill_gap_results'))
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

    flash(f'Invalid test type: {test_type}. Please choose aptitude, personality, or skill_gap.', 'danger')
    return redirect(url_for('dashboard'))

@app.route('/career_assessment', methods=['GET'])
def career_assessment():
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all() if current_user.is_authenticated else []
    return render_template('career_assessment.html',active_page='career_assessment', notifications=notifications)

@app.route('/submit_aptitude', methods=['POST'])
@login_required
@csrf.exempt  # Temporarily exempt to test if CSRF is the issue
def submit_aptitude():
    data = request.get_json()
    logger.debug(f"Received data: {data}")
    if not data or 'responses' not in data:
        return jsonify({'error': 'No data provided'}), 400

    responses = data['responses']
    time_spent = data.get('time_spent', 0)
    current_question_index = data.get('current_question_index', 0)

    # Load session data
    questions = session.get('aptitude_questions', [])
    user_responses = session.get('aptitude_responses', [])
    ability_estimate = session.get('ability_estimate', 0.0)
    used_questions = session.get('used_aptitude', [])

    if not questions or current_question_index >= len(questions):
        return jsonify({'error': 'No more questions available'}), 400

    # Process the current response
    current_response = responses[-1]
    question_id = current_response['questionId']
    
    # Validate the answer
    if 'answer' not in current_response or current_response['answer'] is None:
        return jsonify({'error': 'Answer is missing or invalid'}), 400
    
    try:
        user_answer = int(current_response['answer'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Answer must be a valid integer'}), 400

    current_question = next((q for q in questions if q['id'] == question_id), None)
    if not current_question:
        return jsonify({'error': 'Question not found'}), 400

    # Check if the answer is correct
    correct_answer = current_question['correct']
    is_correct = user_answer == correct_answer

    # Update category-based scoring
    category = next(
        (cat for cat, levels in APTITUDE_QUESTIONS.items() if any(
            current_question['id'] in [q['id'] for q in level] for level in levels.values()
        )), "Unknown"
    )
    session['aptitude_total'] = session.get('aptitude_total', 0) + 1
    session['aptitude_correct'] = session.get('aptitude_correct', 0) + (1 if is_correct else 0)
    session['aptitude_category_counts'][category] = session['aptitude_category_counts'].get(category, 0) + 1
    if is_correct:
        session['aptitude_category_scores'][category] = session['aptitude_category_scores'].get(category, 0) + 1
    session.modified = True
    # Bayesian ability estimation
    scaling_factors = ADAPTIVE_TEST_SETTINGS['scaling_factors']
    irt_params = current_question['irt_params']
    difficulty = irt_params['difficulty']
    discrimination = irt_params['discrimination']
    expected_prob = 1 / (1 + np.exp(-discrimination * (ability_estimate - difficulty)))
    if is_correct:
        ability_estimate += scaling_factors['correct_answer'] * (1 - expected_prob)
    else:
        ability_estimate += scaling_factors['wrong_answer'] * expected_prob
    time_limit = current_question['time_limit']
    if time_spent > time_limit:
        excess_time = time_spent - time_limit
        time_penalty = (excess_time / time_limit) * scaling_factors['time_penalty']
        ability_estimate += time_penalty

    # Store the response
    user_responses.append({
        'question_id': question_id,
        'answer': user_answer,
        'correct': is_correct,
        'time_spent': time_spent
    })
    session['aptitude_responses'] = user_responses
    session['ability_estimate'] = ability_estimate

    # Check if the test is complete
    if current_question_index + 1 >= len(questions):
        # Calculate final scores
        overall_score = (session['aptitude_correct'] / session['aptitude_total']) * 100
        detailed_scores = {
            cat: (session['aptitude_category_scores'].get(cat, 0) / session['aptitude_category_counts'][cat]) * 100
            for cat in session['aptitude_category_counts'] if session['aptitude_category_counts'][cat] > 0
        }

        # Save test result
        result = TestResult(
            user_id=current_user.id,
            test_type='aptitude',
            score=overall_score,
            time_spent=sum(r['time_spent'] for r in user_responses),
            details=json.dumps(detailed_scores)  # Ensure detailed_scores is a dict
        )
        db.session.add(result)

        # Award badges
        if not Badge.query.filter_by(user_id=current_user.id, name="First Test Completed").first():
            badge = Badge(
                user_id=current_user.id,
                name="First Test Completed",
                description="Completed your first test!",
                icon="fas fa-trophy"
            )
            db.session.add(badge)
        if overall_score >= 80:
            if not Badge.query.filter_by(user_id=current_user.id, name="High Scorer").first():
                badge = Badge(
                    user_id=current_user.id,
                    name="High Scorer",
                    description="Scored 80% or higher!",
                    icon="fas fa-star"
                )
                db.session.add(badge)

        # Send notification
        notification = Notification(
            user_id=current_user.id,
            message=f"Aptitude Test completed! Score: {overall_score:.1f}%",
            type="test_result"
        )
        db.session.add(notification)
        db.session.commit()

        # Update completed tests
        completed_tests = session.get('completed_tests', [])
        if 'aptitude' not in completed_tests:
            completed_tests.append('aptitude')
            session['completed_tests'] = completed_tests

        # Store test results for display in dashboard
        test_results = session.get('test_results', {})
        test_results['aptitude'] = {
            'score': overall_score,
            'correct': session['aptitude_correct'],
            'total': session['aptitude_total'],
            'time_spent': sum(r['time_spent'] for r in user_responses),
            'detailed_scores': detailed_scores,
            'responses': user_responses,
            'questions': questions
        }
        session['test_results'] = test_results

        return jsonify({'redirect': url_for('aptitude_results')})

    # Select the next question based on ability estimate and category performance
    category_performance = {
        cat: (session['aptitude_category_scores'].get(cat, 0) / session['aptitude_category_counts'][cat]) * 100
        for cat in session['aptitude_category_counts'] if session['aptitude_category_counts'][cat] > 0
    }

    # Determine the next difficulty based on performance in the current category
    thresholds = ADAPTIVE_TEST_SETTINGS['proficiency_levels'].get(category, {"thresholds": [40, 70]})
    performance = category_performance.get(category, 0)
    if performance < thresholds['thresholds'][0]:
        next_difficulty = 'easy'
    elif performance < thresholds['thresholds'][1]:
        next_difficulty = 'moderate'
    else:
        next_difficulty = 'hard'

    # Select the next question
    remaining_questions = [
        q for q in questions[current_question_index + 1:]
        if q['id'] not in [r['question_id'] for r in user_responses]
    ]
    if not remaining_questions:
        available_questions = copy.deepcopy(APTITUDE_QUESTIONS)
        next_questions = []
        for cat in available_questions:
            next_questions.extend([
                q for q in available_questions[cat][next_difficulty]
                if q['id'] not in used_questions
            ])
        if not next_questions:
            for diff in ['easy', 'moderate', 'hard']:
                if diff != next_difficulty:
                    for cat in available_questions:
                        next_questions.extend([
                            q for q in available_questions[cat][diff]
                            if q['id'] not in used_questions
                        ])
                    if next_questions:
                        break
        if not next_questions:
            for cat in available_questions:
                next_questions.extend([
                    q for q in (
                        available_questions[cat]['easy'] +
                        available_questions[cat]['moderate'] +
                        available_questions[cat]['hard']
                    )
                    if q['id'] not in used_questions
                ])
        if not next_questions:
            return jsonify({'error': 'No more questions available'}), 400
        next_question = random.choice(next_questions)
        questions[current_question_index + 1] = next_question
        used_questions.append(next_question['id'])
    else:
        next_question = remaining_questions[0]

    # Add category to the next question
    next_question['category'] = next(
        (cat for cat, levels in APTITUDE_QUESTIONS.items() if any(
            next_question['id'] in [q['id'] for q in level] for level in levels.values()
        )), "Unknown"
    )

    # Update session with modified questions and used questions
    session['aptitude_questions'] = questions
    session['used_aptitude'] = used_questions

    return jsonify({
        'question': next_question,
        'current_question_index': current_question_index + 1
    })

def select_next_question(ability_estimate, questions, next_index):
    # Filter remaining questions
    remaining_questions = questions[next_index:]
    if not remaining_questions:
        return None

    # Find the question with the closest difficulty to the user's ability estimate
    best_match = None
    smallest_diff = float('inf')

    for question in remaining_questions:
        difficulty = question['irt_params']['difficulty']
        diff = abs(difficulty - ability_estimate)
        if diff < smallest_diff:
            smallest_diff = diff
            best_match = question

    return best_match

def calculate_aptitude_scores(responses, questions):
    scores = {}
    for category in APTITUDE_QUESTIONS.keys():
        category_questions = [q for q in questions if q['category'] == category]
        category_responses = [r for r in responses if r['question_id'] in [q['id'] for q in category_questions]]
        correct_count = sum(1 for r in category_responses if r['correct'])
        total = len(category_questions)
        scores[category] = (correct_count / total) * 100 if total > 0 else 0
    return scores

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
    
    scores = {
        'Openness': 0, 'Conscientiousness': 0, 'Extraversion': 0,
        ' Agreeableness': 0, 'Neuroticism': 0
    }
    counts = {trait: 0 for trait in scores}
    trait_mapping = {
        'O': 'Openness',
        'C': 'Conscientiousness',
        'E': 'Extraversion',
        'A': ' Agreeableness',
        'N': 'Neuroticism'
    }

    for response in responses:
        question = next((q for q in questions if q['id'] == response['questionId']), None)
        if not question:
            logger.warning(f"Question ID {response['questionId']} not found in session questions")
            continue
        try:
            value = int(response['answer'])
            if value < 0 or value > 4:
                logger.warning(f"Invalid answer value {value} for question {question['id']}")
                continue
            trait = question['trait']
            if trait not in trait_mapping:
                logger.error(f"Invalid trait {trait} for question {question['id']}")
                continue
            trait_name = trait_mapping[trait]
            # Adjust score based on question-specific direction
            if question['direction'] == 'positive':
                score = value  # 0 to 4
            else:  # 'negative'
                score = 4 - value  # Reverse: 4 to 0
            scores[trait_name] += score
            counts[trait_name] += 1
        except (ValueError, KeyError) as e:
            logger.error(f"Error processing response {response}: {e}")
            continue
    
    # Normalize scores to a percentage
    for trait in scores:
        if counts[trait] > 0:
            max_possible = counts[trait] * 4  # Each question scored from 0 to 4
            scores[trait] = (scores[trait] / max_possible) * 100
        else:
            scores[trait] = 0
            logger.warning(f"No responses recorded for trait {trait}")
    
    dominant_trait = max(scores, key=scores.get)
    result = TestResult(
        user_id=current_user.id,
        test_type='personality',
        score=scores[dominant_trait],
        time_spent=duration,
        details=json.dumps(scores)
    )
    db.session.add(result)
    
    # Award badges
    if not Badge.query.filter_by(user_id=current_user.id, name="First Test Completed").first():
        badge = Badge(user_id=current_user.id, name="First Test Completed", description="Completed your first test!", icon="fas fa-trophy")
        db.session.add(badge)
    if scores[dominant_trait] >= 80:
        if not Badge.query.filter_by(user_id=current_user.id, name="High Scorer").first():
            badge = Badge(user_id=current_user.id, name="High Scorer", description="Scored 80% or higher!", icon="fas fa-star")
            db.session.add(badge)
    
    # Add notification
    notification = Notification(user_id=current_user.id, message=f"Personality Test completed! Dominant trait: {dominant_trait} ({scores[dominant_trait]:.1f}%)", type="test_result")
    db.session.add(notification)
    db.session.commit()
    
    # Update session
    completed_tests = session.get('completed_tests', [])
    if 'personality' not in completed_tests:
        completed_tests.append('personality')
        session['completed_tests'] = completed_tests

    test_results = session.get('test_results', {})
    test_results['personality'] = {'score': scores[dominant_trait], 'details': scores}
    session['test_results'] = test_results
    
    session.pop('personality_questions', None)
    return jsonify({'redirect': url_for('personality_results')})

@app.route('/submit_skill_gap', methods=['POST'])
@login_required
def submit_skill_gap():
    data = request.get_json()
    if not data or 'responses' not in data:
        return jsonify({'error': 'No data provided'}), 400

    # Initialize session variables if not present
    session.setdefault('skill_gap_total', 0)
    session.setdefault('skill_gap_correct', 0)

    responses = data['responses']
    time_spent = data.get('time_spent', 0)
    current_question_index = data.get('current_question_index')
    questions = session.get('skill_gap_questions', [])

    if not questions or current_question_index >= len(questions):
        return jsonify({'error': 'Invalid session data'}), 400

    current_response = responses[-1]
    question_id = current_response['questionId']
    
    # Validate and convert the answer
    # In submit_skill_gap route
    try:
        answer = int(current_response['answer'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid answer format. Answer must be an integer.'}), 400

    question = next((q for q in questions if q['id'] == question_id), None)
    if not question:
        return jsonify({'error': 'Question not found'}), 400

    # Update session counters
    session['skill_gap_total'] += 1
    if answer == question['correct']:
        session['skill_gap_correct'] += 1

    # Mark session as modified
    session.modified = True

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

        # Update completed tests
        completed_tests = session.get('completed_tests', [])
        if 'skill_gap' not in completed_tests:
            completed_tests.append('skill_gap')
            session['completed_tests'] = completed_tests

        # Store test results for display in dashboard
        test_results = session.get('test_results', {})
        test_results['skill_gap'] = {
            'score': score,
            'correct': session['skill_gap_correct'],
            'total': session['skill_gap_total'],
            'time_spent': time_spent,
            'detailed_scores': detailed_scores
        }
        session['test_results'] = test_results

        session.pop('skill_gap_questions', None)
        session.pop('skill_gap_correct', None)
        session.pop('skill_gap_total', None)
        session.modified = True  # Mark session as modified after clearing

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
    
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
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
                          ).count() > 0,
                          active_page='results',
                          notifications=notifications)
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

@app.route('/aptitude_results')
@login_required
def aptitude_results():
    test_results = session.get('test_results', {})
    score_data = test_results.get('aptitude', None)
    has_personality = 'personality' in session.get('completed_tests', [])
    has_aptitude = 'aptitude' in session.get('completed_tests', [])

    if not score_data:
        flash('No aptitude test results found. Please complete the test first.', 'warning')
        return redirect(url_for('dashboard'))

    # Ensure responses and questions are included in score_data
    score_data['test_type'] = 'aptitude'
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()

    return render_template(
        'results.html',
        score_data=score_data,
        has_personality=has_personality,
        has_aptitude=has_aptitude,
        active_page='results',
        notifications=notifications
    )

@app.route('/personality_results')
@login_required
def personality_results():
    latest_test = TestResult.query.filter_by(user_id=current_user.id, test_type='personality').order_by(TestResult.completed_at.desc()).first()
    if not latest_test:
        flash('No personality test results found.', 'warning')
        return redirect(url_for('dashboard'))

    scores = json.loads(latest_test.details)
    dominant_trait = max(scores, key=scores.get)
    trait_names = {
        'Openness': 'Openness to Experience',
        'Conscientiousness': 'Conscientiousness',
        'Extraversion': 'Extraversion',
        'Agreeableness': 'Agreeableness',
        'Neuroticism': 'Neuroticism'
    }
    has_aptitude = TestResult.query.filter_by(user_id=current_user.id, test_type='aptitude').count() > 0
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
    
    return render_template('personality_results.html',
                          scores=scores,
                          dominant_trait=dominant_trait,
                          trait_names=trait_names,
                          has_aptitude=has_aptitude,
                          active_page='results',
                          notifications=notifications)
    
def calculate_match(user_scores, career):
    components = {}
    base_weights = {'personality': 0.4, 'aptitude': 0.4, 'skill_gap': 0.2}

    try:
        # Personality component
        if 'personality' in user_scores and user_scores['personality']:
            career_personality = {k.strip(): float(v) for k, v in career['personality'].items()}
            user_personality = {k: float(v) for k, v in user_scores['personality'].items()}
            traits = ['Openness', 'Conscientiousness', 'Extraversion', ' Agreeableness', 'Neuroticism']
            user_vals = [user_personality.get(trait, 0) for trait in traits]
            career_vals = [career_personality.get(trait, 0) for trait in traits]
            trait_score = cosine_similarity(user_vals, career_vals)
            components['personality'] = trait_score if not np.isnan(trait_score) else 0.0

        # Aptitude component
        if 'aptitude' in user_scores and user_scores['aptitude']:
            career_aptitude = {k: float(v) for k, v in career['aptitude'].items()}
            user_aptitude = {k: float(v) for k, v in user_scores['aptitude'].items()}
            total_career_aptitude = sum(career_aptitude.values())
            if total_career_aptitude > 0:
                apt_score = sum(
                    min(user_aptitude.get(cat, 0), career_aptitude.get(cat, 0))
                    for cat in career_aptitude
                ) / total_career_aptitude
                components['aptitude'] = apt_score
            else:
                components['aptitude'] = 0.0

        # Skill gap component
        if 'skill_gap' in user_scores and 'score' in user_scores['skill_gap']:
            user_skill_score = float(user_scores['skill_gap']['score'])
            career_required = float(career['skills'].get('required', 0))
            skill_score = 1 - abs(user_skill_score - career_required) / 100
            components['skill_gap'] = skill_score

        if not components:
            return 0.0

        available_weights = {k: base_weights[k] for k in components}
        total_weight = sum(available_weights.values())
        if total_weight == 0:
            return 0.0

        weighted_sum = sum(components[k] * (available_weights[k] / total_weight) for k in components)
        return round(weighted_sum * 100, 2)
    except Exception as e:
        logger.error(f"Error in calculate_match: {str(e)}")
        return 0.0

@app.route('/career_match', methods=['GET'])
@login_required
def career_match():
    try:
        # Fetch user's test results
        personality_result = TestResult.query.filter_by(user_id=current_user.id, test_type='personality').order_by(TestResult.completed_at.desc()).first()
        aptitude_result = TestResult.query.filter_by(user_id=current_user.id, test_type='aptitude').order_by(TestResult.completed_at.desc()).first()
        skill_gap_result = TestResult.query.filter_by(user_id=current_user.id, test_type='skill_gap').order_by(TestResult.completed_at.desc()).first()
        
        user_scores = {}
        if personality_result:
            try:
                user_scores['personality'] = json.loads(personality_result.details)
            except json.JSONDecodeError:
                logger.error(f"Invalid personality details JSON for user {current_user.id}")
                user_scores['personality'] = {}
        if aptitude_result:
            try:
                user_scores['aptitude'] = json.loads(aptitude_result.details)
            except json.JSONDecodeError:
                logger.error(f"Invalid aptitude details JSON for user {current_user.id}")
                user_scores['aptitude'] = {}
        if skill_gap_result:
            try:
                user_scores['skill_gap'] = json.loads(skill_gap_result.details)
                if 'score' not in user_scores['skill_gap']:
                    user_scores['skill_gap']['score'] = skill_gap_result.score
            except json.JSONDecodeError:
                logger.error(f"Invalid skill_gap details JSON for user {current_user.id}")
                user_scores['skill_gap'] = {'score': skill_gap_result.score}

        # Calculate career matches
        matches = []
        onet_api, _ = get_onet_api()
        soc_codes = {
            "Software Developer": "15-1132.00",
            "Data Scientist": "15-2051.00",
            "Graphic Designer": "27-1024.00",
            "Business Manager": "11-1021.00",
            "Research Scientist": "19-1042.00"
        }

        for career_name, career_data in CAREER_MAPPING.items():
            try:
                match_score = calculate_match(user_scores, career_data)
                soc_code = soc_codes.get(career_name, "15-1132.00")
                career_details = onet_api.get_career_details(soc_code)
                skills = onet_api.get_skills_for_occupation(soc_code)
                education = onet_api.get_education_for_occupation(soc_code)

                matches.append({
                    'name': career_name,
                    'score': match_score,
                    'description': career_data.get('description', 'No description available'),
                    'resources': career_data.get('resources', []),
                    'onet_details': {
                        'title': career_details['title'],
                        'median_wage': career_details['wages']['median'],
                        'growth_rate': career_details['outlook']['growth_rate'],
                        'skills': [skill['name'] for skill in skills],
                        'education': education['typical_level']
                    }
                })
            except Exception as e:
                logger.error(f"Error calculating match for {career_name}: {str(e)}")
                continue
        
        # Sort matches by score in descending order
        matches.sort(key=lambda x: x['score'], reverse=True)

        # Fetch notifications
        notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()

        return render_template(
            'career_match.html',
            matches=matches,
            active_page='career_match',
            notifications=notifications
        )
    except Exception as e:
        logger.error(f"Error in career_match route: {str(e)}")
        flash('An error occurred while calculating career matches. Please try again later.', 'error')
        return redirect(url_for('dashboard'))

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
   
@app.route('/full_analysis')
@login_required
def full_analysis():
    # Fetch all test results for the user
    tests = TestResult.query.filter_by(user_id=current_user.id).all()
    
    # Organize test results by type
    test_results = {
        'aptitude': None,
        'personality': None,
        'skill_gap': None
    }
    
    for test in tests:
        if test.test_type == 'aptitude':
            test_results['aptitude'] = {
                'score': test.score,
                'details': json.loads(test.details),
                'completed_at': test.completed_at
            }
        elif test.test_type == 'personality':
            test_results['personality'] = {
                'score': test.score,
                'details': json.loads(test.details),
                'completed_at': test.completed_at
            }
        elif test.test_type == 'skill_gap':
            test_results['skill_gap'] = {
                'score': test.score,
                'details': json.loads(test.details),
                'completed_at': test.completed_at
            }
    
    # Check if all required tests are completed
    if not all(test_results.values()):
        flash('Please complete all tests (Aptitude, Personality, and Skill Gap) to view the full analysis.', 'warning')
        return redirect(url_for('dashboard'))
    
    # Compute dominant personality trait
    if test_results['personality']:
        personality_details = test_results['personality']['details']
        dominant_trait = max(personality_details, key=personality_details.get)
        test_results['personality']['dominant_trait'] = dominant_trait
    
    # Calculate career matches
    user_scores = {
        'aptitude': test_results['aptitude']['details'],
        'personality': test_results['personality']['details'],
        'skill_gap': {
            'field': list(test_results['skill_gap']['details'].keys())[0],
            'score': test_results['skill_gap']['score']
        }
    }
    
    matches = []
    onet_api, _ = get_onet_api()  # Unpack and ignore EdxAPI
    soc_codes = {
        "Software Developer": "15-1132.00",
        "Data Scientist": "15-2051.00",
        "Graphic Designer": "27-1024.00",
        "Business Manager": "11-1021.00",
        "Research Scientist": "19-1042.00"
    }
    
    for career, data in CAREER_MAPPING.items():
        score = calculate_match(user_scores, data)
        # Fetch additional career details from O*NET
        soc_code = soc_codes.get(career, "15-1132.00")  # Default to Software Developer SOC code
        career_details = onet_api.get_career_details(soc_code)
        skills = onet_api.get_skills_for_occupation(soc_code)
        education = onet_api.get_education_for_occupation(soc_code)
        
        # Fetch resources using get_recommendations
        primary_interest = data['interests'][0] if data['interests'] else "Software Development"
        resources = get_recommendations(primary_interest, user_scores['skill_gap']['score'])
        formatted_resources = [
            {"name": res["name"], "link": res["url"]} for res in resources
        ]
        
        matches.append({
            'name': career,
            'score': score,
            'details': data,
            'resources': formatted_resources,
            'onet_details': {
                'title': career_details['title'],
                'median_wage': career_details['wages']['median'],
                'growth_rate': career_details['outlook']['growth_rate'],
                'skills': [skill.get('name', 'N/A') for skill in skills[:5]],  # Top 5 skills
                'education': education.get('typical_level', 'N/A')
            }
        })
    
    matches.sort(key=lambda x: x['score'], reverse=True)
    
    # Prepare analysis data for the template
    analysis_data = {
        'aptitude': test_results['aptitude'],
        'personality': test_results['personality'],
        'skill_gap': test_results['skill_gap']
    }
    
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
    return render_template('full_analysis.html',
                          analysis=analysis_data,
                          matches=matches[:3],  # Top 3 career matches
                          active_page='full_analysis',
                          notifications=notifications)
    
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

@app.route('/career_details/<career_name>')
@login_required
def career_details(career_name):
    # Fetch career data from CAREER_MAPPING
    career_data = CAREER_MAPPING.get(career_name)
    if not career_data:
        flash('Career not found.', 'danger')
        return redirect(url_for('career_match'))
    
    # Fetch user scores for match calculation
    user_scores = {}
    tests = TestResult.query.filter_by(user_id=current_user.id).all()
    for test in tests:
        if test.test_type == 'personality':
            user_scores['personality'] = json.loads(test.details)
        elif test.test_type == 'aptitude':
            user_scores['aptitude'] = json.loads(test.details)
        elif test.test_type == 'skill_gap':
            user_scores['skill_gap'] = {
                'field': list(json.loads(test.details).keys())[0],
                'score': test.score
            }
    
    # Calculate match score
    match_score = calculate_match(user_scores, career_data)
    
    # Fetch O*NET data
    onet_api = get_onet_api()
    soc_codes = {
        "Software Developer": "15-1132.00",
        "Data Scientist": "15-2051.00",
        "Graphic Designer": "27-1024.00",
        "Business Manager": "11-1021.00",
        "Research Scientist": "19-1042.00"
    }
    soc_code = soc_codes.get(career_name, "15-1132.00")
    career_details = onet_api.get_career_details(soc_code)
    skills = onet_api.get_skills_for_occupation(soc_code)
    education = onet_api.get_education_for_occupation(soc_code)
    
    onet_data = {
        'title': career_details['title'],
        'median_wage': career_details['wages']['median'],
        'growth_rate': career_details['outlook']['growth_rate'],
        'skills': [skill.get('name', 'N/A') for skill in skills],
        'education': education.get('typical_level', 'N/A')
    }
    
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
    return render_template('career_details.html',
                          career_name=career_name,
                          match_score=match_score,
                          career_data=career_data,
                          onet_data=onet_data,
                          active_page='career_details',
                          notifications=notifications)
    
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
        
        # Theme Preferences
        if 'theme' in request.form:
            theme = request.form['theme']
            if theme in ['light', 'dark']:
                current_user.theme = theme
                db.session.commit()
                flash('Theme updated successfully!', 'success')
            else:
                flash('Invalid theme selection.', 'danger')
        
        # Notification Preferences
        elif 'notify_test_reminders' in request.form:
            current_user.notify_test_reminders = 'notify_test_reminders' in request.form
            current_user.notify_badge_earned = 'notify_badge_earned' in request.form
            current_user.notify_progress_updates = 'notify_progress_updates' in request.form
            db.session.commit()
            flash('Notification preferences updated successfully!', 'success')
        
        # Email Preferences
        elif 'email_notifications' in request.form:
            current_user.email_notifications = 'email_notifications' in request.form
            current_user.email_newsletters = 'email_newsletters' in request.form
            db.session.commit()
            flash('Email preferences updated successfully!', 'success')
        
        # Profile Visibility
        elif 'profile_visibility' in request.form:
            visibility = request.form['profile_visibility']
            if visibility in ['public', 'private']:
                current_user.profile_visibility = visibility
                db.session.commit()
                flash('Profile visibility updated successfully!', 'success')
            else:
                flash('Invalid visibility selection.', 'danger')
        
        # Preferred Test Categories
        elif 'pref_aptitude' in request.form or 'pref_personality' in request.form or 'pref_skill_gap' in request.form:
            categories = []
            if 'pref_aptitude' in request.form:
                categories.append('aptitude')
            if 'pref_personality' in request.form:
                categories.append('personality')
            if 'pref_skill_gap' in request.form:
                categories.append('skill_gap')
            current_user.preferred_test_categories = categories
            db.session.commit()
            flash('Preferred test categories updated successfully!', 'success')
        
        # Change Password
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
        
        # Reset Roadmap (existing functionality)
        elif 'reset_roadmap' in request.form:
            TestResult.query.filter_by(user_id=current_user.id).delete()
            db.session.commit()
            flash('Roadmap progress reset successfully!', 'success')
        
        # Delete Account
        elif 'delete_account' in request.form:
            confirm_username = request.form.get('confirm_username')
            if confirm_username != current_user.username:
                flash('Username does not match. Account deletion aborted.', 'danger')
            else:
                # Delete all user-related data
                TestResult.query.filter_by(user_id=current_user.id).delete()
                Badge.query.filter_by(user_id=current_user.id).delete()
                Notification.query.filter_by(user_id=current_user.id).delete()
                db.session.delete(current_user)
                db.session.commit()
                logout_user()
                flash('Your account has been deleted.', 'info')
                return redirect(url_for('index'))
        
        return redirect(url_for('settings'))
    
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
    return render_template('settings.html', user=current_user, active_page='settings', notifications=notifications)

@app.route('/progress_tracking')
@login_required
def progress_tracking():
    # Fetch test history from database
    test_history = TestResult.query.filter_by(user_id=current_user.id).order_by(TestResult.completed_at.asc()).all()
    
    # Streak calculation function
    def calculate_streak(test_dates):
        if not test_dates:
            return 0
        
        current_streak = 1
        sorted_dates = sorted(test_dates, reverse=True)
        
        for i in range(1, len(sorted_dates)):
            if (sorted_dates[i-1] - sorted_dates[i]).days == 1:
                current_streak += 1
            else:
                break
        return current_streak

    # Calculate current streak
    test_dates = [test.completed_at.date() for test in test_history if test.completed_at]
    current_streak = calculate_streak(test_dates)

    # Handle empty test history
    total_tests = len(test_history)
    if total_tests == 0:
        flash('No tests taken yet. Take a test to track your progress!', 'info')
        return redirect(url_for('test'))

    # Calculate average scores
    test_types = ['sample', 'aptitude', 'personality']
    avg_scores = {}
    for test_type in test_types:
        type_tests = [test for test in test_history if test.test_type == test_type]
        max_score = 9 if test_type == 'sample' else (5 if test_type == 'personality' else 10)
        avg_scores[test_type] = (sum(test.score for test in type_tests) / (len(type_tests) * max_score)) * 100 if type_tests else 0

    # Prepare progress data (CORRECTED SECTION)
    progress_data = {
        'labels': [test.completed_at.strftime('%Y-%m-%d') for test in test_history],
        'scores': [
            (test.score / (
                9 if test.test_type == 'sample' 
                else (5 if test.test_type == 'personality' else 10)
            )) * 100 
            for test in test_history
        ],
        'types': [test.test_type for test in test_history]
    }

    # Define career tasks
    career_path = session.get('selected_field', 'Software Development')
    if career_path not in CAREER_MAPPING:
        career_path = 'Software Development'

    tasks = [
        {"name": "Complete Initial Assessment", "completed": any(t.test_type == 'aptitude' for t in test_history)},
        {"name": "Enroll in Courses", "completed": False},
        {"name": "Practice Skills", "completed": any(t.test_type == 'skill_gap' and career_path in json.loads(t.details) for t in test_history)},
        {"name": "Build Portfolio", "completed": False},
        {"name": "Apply for Jobs", "completed": False}
    ]

    # Calculate progress
    completed_tasks = sum(1 for task in tasks if task["completed"])
    progress_percentage = (completed_tasks / len(tasks)) * 100 if tasks else 0

    # Fetch notifications
    notifications = Notification.query.filter_by(
        user_id=current_user.id, 
        is_read=False
    ).order_by(Notification.date.desc()).limit(5).all()

    return render_template(
        'progress_tracking.html',
        user=current_user,
        test_history=test_history,
        avg_scores=avg_scores,
        progress_data=progress_data,
        tasks=tasks,
        progress_percentage=progress_percentage,
        current_streak=current_streak,
        total_tests=total_tests,
        active_page='progress_tracking',
        notifications=notifications
    )

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
                    "date": next((t.completed_at for t in test_history if t.test_type == 'aptitude'), None),  # Keep timezone-aware
                    "type": "test",
                    "completed": any(t.test_type == 'aptitude' for t in test_history),
                    "progress": 100 if any(t.test_type == 'aptitude' for t in test_history) else 0
                },
                {
                    "title": "Skill Gap Assessment",
                    "description": "Evaluated coding skills",
                    "details": "Assessed proficiency in Python, JavaScript, and software development fundamentals.",
                    "date": next((t.completed_at for t in test_history if t.test_type == 'skill_gap' and 'Software Development' in json.loads(t.details)), None),  # Keep timezone-aware
                    "type": "test",
                    "completed": any(t.test_type == 'skill_gap' and 'Software Development' in json.loads(t.details) for t in test_history),
                    "progress": 100 if any(t.test_type == 'skill_gap' and 'Software Development' in json.loads(t.details) for t in test_history) else 0
                },
                {
                    "title": "First Project",
                    "description": "Built a basic application",
                    "details": "Developed a to-do list app using HTML, CSS, and JavaScript.",
                    "date": datetime(2025, 3, 10, tzinfo=timezone.utc),  # Make timezone-aware
                    "type": "project",
                    "completed": False,
                    "progress": 50
                },
                {
                    "title": "Portfolio Creation",
                    "description": "Showcased projects",
                    "details": "Created a portfolio website with 3 projects, hosted on GitHub Pages.",
                    "date": datetime(2025, 3, 15, tzinfo=timezone.utc),  # Make timezone-aware
                    "type": "project",
                    "completed": False,
                    "progress": 30
                },
                {
                    "title": "Job Application",
                    "description": "Applied to entry-level roles",
                    "details": "Submitted applications to 5 software development positions.",
                    "date": datetime(2025, 3, 20, tzinfo=timezone.utc),  # Make timezone-aware
                    "type": "job",
                    "completed": False,
                    "progress": 20
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
                    "date": next((t.completed_at for t in test_history if t.test_type == 'aptitude'), None),  # Keep timezone-aware
                    "type": "test",
                    "completed": any(t.test_type == 'aptitude' for t in test_history),
                    "progress": 100 if any(t.test_type == 'aptitude' for t in test_history) else 0
                },
                {
                    "title": "Skill Gap Assessment",
                    "description": "Evaluated data skills",
                    "details": "Assessed proficiency in Python, R, and data analysis techniques.",
                    "date": next((t.completed_at for t in test_history if t.test_type == 'skill_gap' and 'Data Science' in json.loads(t.details)), None),  # Keep timezone-aware
                    "type": "test",
                    "completed": any(t.test_type == 'skill_gap' and 'Data Science' in json.loads(t.details) for t in test_history),
                    "progress": 100 if any(t.test_type == 'skill_gap' and 'Data Science' in json.loads(t.details) for t in test_history) else 0
                },
                {
                    "title": "Statistics Mastery",
                    "description": "Completed stats course",
                    "details": "Finished an online course on advanced statistics and probability.",
                    "date": datetime(2025, 3, 12, tzinfo=timezone.utc),  # Make timezone-aware
                    "type": "course",
                    "completed": False,
                    "progress": 70
                },
                {
                    "title": "Data Project",
                    "description": "Analyzed a dataset",
                    "details": "Performed exploratory data analysis on a public dataset using Pandas and Matplotlib.",
                    "date": datetime(2025, 3, 18, tzinfo=timezone.utc),  # Make timezone-aware
                    "type": "project",
                    "completed": False,
                    "progress": 40
                },
                {
                    "title": "Research Publication",
                    "description": "Published findings",
                    "details": "Published a research paper on machine learning applications in a journal.",
                    "date": datetime(2025, 3, 25, tzinfo=timezone.utc),  # Make timezone-aware
                    "type": "publication",
                    "completed": False,
                    "progress": 10
                }
            ]
        }
    }

    # Get roadmap data for the user's career path, default to Software Development if not found
    roadmap_data = career_roadmaps.get(career_path, career_roadmaps["Software Development"])
    milestones = roadmap_data["milestones"]

    # Fetch unread notifications for the user, limited to the 5 most recent
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()

    # Get the current date as a timezone-aware datetime
    current_date = datetime.now(timezone.utc)

    # Render the roadmap template with the necessary data
    return render_template('roadmap.html',
                          user=current_user,
                          career_goal=roadmap_data["career_goal"],
                          milestones=milestones,
                          career_path=career_path,
                          current_date=current_date,
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