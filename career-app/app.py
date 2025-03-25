import os
import sys
print(f"Python path: {sys.path}")
print(f"Current directory: {os.getcwd()}")

from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_mail import Mail, Message
from flask_migrate import Migrate
from datetime import datetime
from collections import defaultdict
import requests
import random
import copy
from collections import defaultdict
import json
from PIL import Image  # Added for image resizing
# After the existing imports and before the Flask app initialization
from questions import (
    APTITUDE_QUESTIONS, ADAPTIVE_TEST_SETTINGS, PERSONALITY_QUESTIONS,
    SCORING_KEY, TRAIT_WEIGHTS, TRAIT_DEFINITIONS, CAREER_MAPPING,
    SKILL_GAP_QUESTIONS, LEARNING_RESOURCES
)

# Import ProfileForm from forms.py
from forms import ProfileForm, LoginForm, RegisterForm, ContactForm
from flask_caching import Cache
app = Flask(__name__)
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 3600
cache = Cache(app)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()
print(f"Loaded ONET_USER: {os.getenv('ONET_USER')}")
print(f"Loaded ONET_PWD: {os.getenv('ONET_PWD')}")


# Initialize Flask app
app.config['SECRET_KEY'] = '033dc7a2f8382c4dd7bd18a473e24db20b088146eb846900'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///career_analytics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'abc@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password-here'
app.config['MAIL_DEFAULT_SENDER'] = 'abc@gmail.com'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit uploads to 16MB

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Initialize extensions
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

csrf = CSRFProtect(app)
app.config['WTF_CSRF_HEADERS'] = ['X-CSRF-Token']
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)

# Custom Jinja filter
def datetimeformat(value, format='%Y'):
    if value == 'now':
        return datetime.now().strftime(format)
    return value
app.jinja_env.filters['datetimeformat'] = datetimeformat

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=True)
    mobile_number = db.Column(db.String(15), nullable=True)
    pin_code = db.Column(db.String(10), nullable=True)
    dob = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tests = db.relationship('TestResult', backref='user', lazy=True)
    theme = db.Column(db.String(20), default='dark')
    animations_enabled = db.Column(db.Boolean, default=True)
    profile_image = db.Column(db.String(150), nullable=True, default='images/default_profile.jpg')
    bio = db.Column(db.Text, nullable=True)  # Added bio field to User model
    badges = db.relationship('Badge', backref='user', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)

class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    test_type = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    time_spent = db.Column(db.Integer, nullable=True)
    details = db.Column(db.Text, nullable=True)  # Store JSON string of detailed results
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

class University(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    country = db.Column(db.String(100), nullable=False)

class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    icon = db.Column(db.String(50), nullable=False)  # Font Awesome icon class
    date_earned = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # e.g., 'test_result', 'badge_earned'
    is_read = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Placeholder for ONetAPI (since apis.py wasn't provided)
class ONetAPI:
    def get_career_details(self, soc_code):
        # Mock implementation
        return {
            'title': 'Software Developer' if soc_code == '15-1132.00' else 'Business Manager',
            'wages': {'median': 105000},
            'outlook': {'growth_rate': 22}
        }

def get_onet_api():
    return ONetAPI()

# CAREER_MAPPING (as defined in your original code)
CAREER_MAPPING = {
    "Software Developer": {
        "aptitude": {"Mathematics": 70, "Logical Reasoning": 80, "Verbal Ability": 60},
        "personality": {"Openness": 60, "Conscientiousness": 70, "Extraversion": 50, "Agreeableness": 50, "Neuroticism": 40},
        "skills": {"Software Development": 70},
        "interests": ["Software Development"],
        "description": "Designs and builds software applications.",
        "resources": [
            {"name": "Learn Python", "link": "https://www.codecademy.com/learn/learn-python-3"},
            {"name": "Git Tutorial", "link": "https://www.atlassian.com/git/tutorials"}
        ]
    },
    "Data Scientist": {
        "aptitude": {"Mathematics": 80, "Logical Reasoning": 75, "Verbal Ability": 60},
        "personality": {"Openness": 70, "Conscientiousness": 65, "Extraversion": 40, "Agreeableness": 50, "Neuroticism": 40},
        "skills": {"Data Science": 75},
        "interests": ["Data Science"],
        "description": "Analyzes data to derive actionable insights.",
        "resources": [
            {"name": "Machine Learning by Andrew Ng", "link": "https://www.coursera.org/learn/machine-learning"},
            {"name": "SQL for Data Science", "link": "https://www.coursera.org/learn/sql-for-data-science"}
        ]
    },
    "Graphic Designer": {
        "aptitude": {"Mathematics": 50, "Logical Reasoning": 60, "Verbal Ability": 70},
        "personality": {"Openness": 80, "Conscientiousness": 60, "Extraversion": 50, "Agreeableness": 60, "Neuroticism": 40},
        "skills": {"Graphic Design": 70},
        "interests": ["Graphic Design"],
        "description": "Creates visual designs for branding and media.",
        "resources": [
            {"name": "Photoshop Tutorials", "link": "https://www.adobe.com/products/photoshop/tutorials.html"},
            {"name": "UI/UX Design", "link": "https://www.coursera.org/specializations/ui-ux-design"}
        ]
    },
    "Business Manager": {
        "aptitude": {"Mathematics": 60, "Logical Reasoning": 70, "Verbal Ability": 80},
        "personality": {"Openness": 50, "Conscientiousness": 80, "Extraversion": 70, "Agreeableness": 70, "Neuroticism": 30},
        "skills": {"Business Management": 70},
        "interests": ["Business Management"],
        "description": "Leads teams and manages business operations.",
        "resources": [
            {"name": "Leadership Skills", "link": "https://www.udemy.com/topic/leadership/"},
            {"name": "Strategic Management", "link": "https://www.coursera.org/learn/strategic-management"}
        ]
    },
    "Research Scientist": {
        "aptitude": {"Mathematics": 85, "Logical Reasoning": 80, "Verbal Ability": 65},
        "personality": {"Openness": 75, "Conscientiousness": 70, "Extraversion": 40, "Agreeableness": 50, "Neuroticism": 35},
        "skills": {"Data Science": 60},
        "interests": ["Scientific"],
        "description": "Conducts research in scientific fields.",
        "resources": [
            {"name": "Research Methods", "link": "https://www.coursera.org/learn/research-methods"},
            {"name": "Statistics with Python", "link": "https://www.coursera.org/learn/statistics-with-python"}
        ]
    }
}

# Fetch additional aptitude questions from OpenTDB
def fetch_opentdb_questions(category_id, amount=5):
    url = f'https://opentdb.com/api.php?amount={amount}&category={category_id}&type=multiple'
    response = requests.get(url)
    data = response.json()
    if data['response_code'] == 0:
        questions = []
        for q in data['results']:
            options = q['incorrect_answers'] + [q['correct_answer']]
            random.shuffle(options)
            correct_idx = options.index(q['correct_answer'])
            questions.append({
                "id": f"OTDB-{random.randint(1000, 9999)}",
                "text": q['question'],
                "options": options,
                "correct": correct_idx,
                "time_limit": 60
            })
        return questions
    return []

def populate_universities():
    sample_universities = [
        {"name": "Massachusetts Institute of Technology (MIT)", "country": "United States"},
        {"name": "Harvard University", "country": "United States"},
        # Add more as needed
    ]
    with app.app_context():
        for uni in sample_universities:
            if not University.query.filter_by(name=uni['name']).first():
                new_uni = University(name=uni['name'], country=uni['country'])
                db.session.add(new_uni)
        db.session.commit()
        print(f"Added {len(sample_universities)} universities to the database.")

with app.app_context():
    db.create_all()
    populate_universities()
    
# Generate dynamic test questions
# Replace the existing generate_questions function
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
        # Start with initial difficulty from settings
        current_difficulty = ADAPTIVE_TEST_SETTINGS['initial_difficulty']
        questions = []
        available_questions = copy.deepcopy(APTITUDE_QUESTIONS)
        
        # Select 10 questions, adapting difficulty based on simulated performance
        for i in range(10):
            category = random.choice(list(available_questions.keys()))
            difficulty_questions = available_questions[category][current_difficulty]
            if not difficulty_questions:
                # Fallback to another difficulty if empty
                for diff in ['easy', 'moderate', 'hard']:
                    if available_questions[category][diff]:
                        difficulty_questions = available_questions[category][diff]
                        current_difficulty = diff
                        break
            if difficulty_questions:
                question = random.choice(difficulty_questions)
                question['time_limit'] = question.get('time_limit', 60)  # Default 60 seconds
                questions.append(question)
                questions.append(question)
                # Remove used question to avoid repetition
                available_questions[category][current_difficulty].remove(question)
                
                # Simulate performance adjustment (actual adjustment happens in /submit_aptitude)
                if i >= 2:  # After a few questions, adjust difficulty
                    prev_correct = session.get('aptitude_correct', 0)
                    prev_total = session.get('aptitude_total', 0)
                    if prev_total > 0 and (prev_correct / prev_total) >= 0.75:
                        current_difficulty = 'hard' if current_difficulty == 'moderate' else 'moderate'
                    elif prev_total > 0 and (prev_correct / prev_total) <= 0.25:
                        current_difficulty = 'easy' if current_difficulty == 'moderate' else 'moderate'
        
        random.shuffle(questions)
        session['aptitude_questions'] = questions  # Store for validation
        return questions[:10]
    elif test_type == 'personality':
        traits = {'O': [], 'C': [], 'E': [], 'A': [], 'N': []}
        for q in PERSONALITY_QUESTIONS:
            if q['trait'] in traits:
                traits[q['trait']].append(q)
        
        selected_questions = []
        for trait in traits:
            trait_qs = traits[trait]
            selected_questions.extend(random.sample(trait_qs, min(2, len(trait_qs))))
        
        for question in selected_questions:
            question['time_limit'] = question.get('time_limit', 60)
        random.shuffle(selected_questions)
        session['personality_questions'] = selected_questions  # Store for validation
        return selected_questions
    elif test_type == 'skill_gap':
        field = session.get('selected_field', 'Software Development')
        available_questions = copy.deepcopy(SKILL_GAP_QUESTIONS.get(field, []))
        if not available_questions:
            return []
        questions = random.sample(available_questions, min(10, len(available_questions)))
        # Assign time_limit to each question
        for question in questions:
            question['time_limit'] = question.get('time_limit', 60)  # Default 60 seconds
        session['skill_gap_questions'] = questions  # Store for validation
        return questions
    return []

# Routes
@app.route('/')
def index():
    if not current_user.is_authenticated and not session.get('_flashes'):
        flash('Kindly log in to unlock comprehensive access to all features.', 'info')
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all() if current_user.is_authenticated else []
    return render_template('index.html', active_page='index', notifications=notifications)

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
    recent_tests = TestResult.query.filter_by(user_id=current_user.id).order_by(TestResult.completed_at.desc()).limit(5).all()
    badges = Badge.query.filter_by(user_id=current_user.id).order_by(Badge.date_earned.desc()).limit(5).all()
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
    
    if recent_tests:
        test_data = {
            'labels': [test.completed_at.strftime('%Y-%m-%d %H:%M') for test in recent_tests[::-1]],
            'scores': [test.score / 9 * 100 if test.test_type == 'sample' else test.score for test in recent_tests[::-1]],
            'types': [test.test_type for test in recent_tests[::-1]]
        }
        # Ensure details is handled safely
        for test in recent_tests:
            test.details_dict = json.loads(test.details) if test.details else {}
        max_score = 9 if recent_tests[0].test_type == 'sample' else 8
    else:
        test_data = {'labels': [], 'scores': [], 'types': []}
        max_score = 8  # Default max score when no tests exist
    
    recommendation = "Take more tests for personalized advice!" if len(recent_tests) < 3 else "You're doing great! Consider exploring advanced career options."
    return render_template('dashboard.html', user=current_user, recent_tests=recent_tests, badges=badges, notifications=notifications, test_data=test_data, recommendation=recommendation, max_score=max_score, active_page='dashboard')

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

@app.route('/test', methods=['GET', 'POST'])
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
        if not current_user.is_authenticated:
            flash('Please log in to access the Aptitude Test.', 'warning')
            return redirect(url_for('login', next=request.url))
        questions = session.get('aptitude_questions')
        if not questions or request.method == 'GET':
            questions = generate_questions('aptitude')
            session['aptitude_questions'] = questions
            session['aptitude_correct'] = 0
            session['aptitude_total'] = 0
            session['aptitude_category_scores'] = defaultdict(int)
            session['aptitude_category_counts'] = defaultdict(int)
        current_question_index = int(request.args.get('q', 0))
        if current_question_index >= len(questions):
            return redirect(url_for('results'))
        question = questions[current_question_index]
        category = next((cat for cat, levels in APTITUDE_QUESTIONS.items() if any(question['id'] in [q['id'] for q in level] for level in levels.values())), "Unknown")
        if request.method == 'POST' and request.form:
            answer = request.form.get(question['id'])
            if answer is not None:
                session['aptitude_total'] += 1
                session['aptitude_category_counts'][category] += 1
                if int(answer) == question['correct']:
                    session['aptitude_correct'] += 1
                    session['aptitude_category_scores'][category] += 1
                # Move to next question or finish
                next_index = current_question_index + 1
                if next_index >= len(questions):
                    score = (session['aptitude_correct'] / session['aptitude_total']) * 100 if session['aptitude_total'] > 0 else 0
                    detailed_scores = {cat: (session['aptitude_category_scores'][cat] / session['aptitude_category_counts'][cat]) * 100 for cat in session['aptitude_category_scores'] if session['aptitude_category_counts'][cat] > 0}
                    result = TestResult(
                        user_id=current_user.id,
                        test_type='aptitude',
                        score=score,
                        time_spent=request.form.get('time_spent', 0),
                        details=json.dumps(detailed_scores)
                    )
                    db.session.add(result)
                    if not Badge.query.filter_by(user_id=current_user.id, name="First Test Completed").first():
                        badge = Badge(user_id=current_user.id, name="First Test Completed", description="Completed your first test!", icon="fas fa-trophy")
                        db.session.add(badge)
                    if score >= 80:
                        if not Badge.query.filter_by(user_id=current_user.id, name="High Scorer").first():
                            badge = Badge(user_id=current_user.id, name="High Scorer", description="Scored 80% or higher on a test!", icon="fas fa-star")
                            db.session.add(badge)
                    notification = Notification(
                        user_id=current_user.id,
                        message=f"You completed the Aptitude Test with a score of {score:.1f}%!",
                        type="test_result"
                    )
                    db.session.add(notification)
                    db.session.commit()
                    session.pop('aptitude_questions', None)
                    session.pop('aptitude_correct', None)
                    session.pop('aptitude_total', None)
                    session.pop('aptitude_category_scores', None)
                    session.pop('aptitude_category_counts', None)
                    flash(f'Aptitude Test completed! Score: {score:.1f}%', 'success')
                    return redirect(url_for('results'))
                return redirect(url_for('test', type='aptitude', q=next_index))
            else:
                flash('Please select an answer before submitting.', 'danger')
        notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
        return render_template('assessments/aptitude.html',
                              questions=[question],
                              instructions=instructions,
                              current_category=category,
                              total_questions=len(questions),
                              completed_questions=current_question_index,
                              current_question_index=current_question_index,
                              initial_time=question['time_limit'],
                              completed_questions=current_question_index,
                              active_page='test',
                              test_type='aptitude',
                              notifications=notifications)

    elif test_type == 'personality':
        if not current_user.is_authenticated:
            flash('Please log in to access the Personality Test.', 'warning')
            return redirect(url_for('login', next=request.url))
        questions = session.get('personality_questions')
        if not questions or request.method == 'GET':
            questions = generate_questions('personality')
            session['personality_questions'] = questions
        if request.method == 'POST':
            if request.form:
                answers = {}
                for q in questions:
                    answer = request.form.get(q['id'])
                    if answer is not None:
                        answers[q['id']] = int(answer)
                    else:
                        flash('Please answer all questions before submitting.', 'danger')
                        notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
                        return render_template('assessments/personality.html',
                                              questions=questions,
                                              instructions=instructions,
                                              current_question_index=0,
                                              question=questions[0],
                                              active_page='test',
                                              test_type='personality',
                                              notifications=notifications)
                trait_scores = defaultdict(float)
                for q in questions:
                    score = SCORING_KEY[q['trait']][answers[q['id']]]
                    trait_scores[q['trait']] += score
                for trait in trait_scores:
                    trait_scores[trait] /= len([q for q in questions if q['trait'] == trait]) * max(SCORING_KEY[trait].values())
                    trait_scores[trait] *= 100
                detailed_scores = dict(trait_scores)
                score = sum(trait_scores.values()) / len(trait_scores) if trait_scores else 0
                result = TestResult(
                    user_id=current_user.id,
                    test_type='personality',
                    score=score,
                    time_spent=request.form.get('time_spent', 0),
                    details=json.dumps(detailed_scores)
                )
                db.session.add(result)
                if not Badge.query.filter_by(user_id=current_user.id, name="First Test Completed").first():
                    badge = Badge(user_id=current_user.id, name="First Test Completed", description="Completed your first test!", icon="fas fa-trophy")
                    db.session.add(badge)
                if score >= 80:
                    if not Badge.query.filter_by(user_id=current_user.id, name="High Scorer").first():
                        badge = Badge(user_id=current_user.id, name="High Scorer", description="Scored 80% or higher on a test!", icon="fas fa-star")
                        db.session.add(badge)
                notification = Notification(
                    user_id=current_user.id,
                    message=f"You completed the Personality Test with an overall score of {score:.1f}%!",
                    type="test_result"
                )
                db.session.add(notification)
                db.session.commit()
                session.pop('personality_questions', None)
                flash(f'Personality Test completed! Overall score: {score:.1f}%', 'success')
                return redirect(url_for('results'))
        current_question_index = int(request.args.get('q', 0))
        if current_question_index < 0 or current_question_index >= len(questions):
            current_question_index = 0
        question = questions[current_question_index]
        notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
        return render_template('assessments/personality.html',
                              questions=questions,
                              instructions=instructions,
                              current_question_index=current_question_index,
                              question=question,
                              active_page='test',
                              test_type='personality',
                              notifications=notifications)

    elif test_type == 'skill_gap':
        if not current_user.is_authenticated:
            flash('Please log in to access the Skill Gap Assessment.', 'warning')
        return redirect(url_for('login', next=request.url))
    selected_field = request.args.get('field', session.get('selected_field', 'Software Development'))
    session['selected_field'] = selected_field
    questions = session.get('skill_gap_questions')
    if not questions or request.method == 'GET':
        questions = generate_questions('skill_gap')
        session['skill_gap_questions'] = questions
        session['skill_gap_correct'] = 0
        session['skill_gap_total'] = 0
        if not questions:
            flash('No questions available for the selected field.', 'warning')
            return redirect(url_for('interest_test'))
        current_question_index = int(request.args.get('q', 0))
        if current_question_index >= len(questions):
            return redirect(url_for('results'))
        question = questions[current_question_index]
        if request.method == 'POST' and request.form:
            answer = request.form.get(question['id'])
            if answer is not None:
                session['skill_gap_total'] += 1
                if int(answer) == question['correct']:
                    session['skill_gap_correct'] += 1
                next_index = current_question_index + 1
                if next_index >= len(questions):
                    skill_score = (session['skill_gap_correct'] / session['skill_gap_total']) * 100 if session['skill_gap_total'] > 0 else 0
                    detailed_scores = {selected_field: skill_score}
                    result = TestResult(
                        user_id=current_user.id,
                        test_type='skill_gap',
                        score=skill_score,
                        time_spent=request.form.get('time_spent', 0),
                        details=json.dumps(detailed_scores)
                    )
                    db.session.add(result)
                    if not Badge.query.filter_by(user_id=current_user.id, name="First Test Completed").first():
                        badge = Badge(user_id=current_user.id, name="First Test Completed", description="Completed your first test!", icon="fas fa-trophy")
                        db.session.add(badge)
                    if skill_score >= 80:
                        if not Badge.query.filter_by(user_id=current_user.id, name="High Scorer").first():
                            badge = Badge(user_id=current_user.id, name="High Scorer", description="Scored 80% or higher on a test!", icon="fas fa-star")
                            db.session.add(badge)
                    notification = Notification(
                        user_id=current_user.id,
                        message=f"You completed the Skill Gap Test for {selected_field} with a score of {skill_score:.1f}%!",
                        type="test_result"
                    )
                    db.session.add(notification)
                    db.session.commit()
                    session.pop('skill_gap_questions', None)
                    session.pop('skill_gap_correct', None)
                    session.pop('skill_gap_total', None)
                    flash(f'Skill Gap Test completed! Score: {skill_score:.1f}%', 'success')
                    return redirect(url_for('career_match'))
                return redirect(url_for('test', type='skill_gap', q=next_index, field=selected_field))
            else:
                flash('Please select an answer before submitting.', 'danger')
        notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
        return render_template('assessments/interest_test.html',
                              selected_field=selected_field,
                              questions=[question],
                              instructions=instructions,
                              total_questions=len(questions),
                              current_question_index=current_question_index,
                              initial_time=question['time_limit'],
                              completed_questions=current_question_index,
                              active_page='test',
                              test_type='skill_gap',
                              notifications=notifications)

    else:
        flash(f'Invalid test type selected: {test_type if test_type else "None"}. Please choose a valid test type.', 'danger')
        return redirect(url_for('index'))

@app.route('/career_assessment', methods=['GET'])
def career_assessment():
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all() if current_user.is_authenticated else []
    return render_template('career_assessment.html',active_page='career_assessment', notifications=notifications)

@app.route('/interest_test', methods=['GET', 'POST'])
@login_required
def interest_test():
    selected_field = request.args.get('field', session.get('selected_field', None))
    if selected_field:
        session['selected_field'] = selected_field
    questions = generate_questions('skill_gap') if selected_field else []
    
    current_question_index = int(request.args.get('q', 0))
    total_questions = len(questions)
    completed_questions = min(current_question_index, total_questions)  # Cap at total_questions
    
    if questions and current_question_index >= len(questions):
        return redirect(url_for('results'))
    
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
    return render_template('assessments/interest_test.html',
                          selected_field=selected_field,
                          questions=questions,
                          total_questions=total_questions,
                          completed_questions=completed_questions,
                          current_question_index=current_question_index,
                          initial_time=questions[0]['time_limit'] if questions else 60,
                          active_page='interest_test',
                          notifications=notifications)
    
@app.route('/submit_assessment', methods=['POST'])
@login_required
def submit_assessment():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    test_type = data.get('type')
    responses = data.get('responses')
    duration = data.get('duration')

    if test_type != 'personality' or not responses or not isinstance(responses, list):
        return jsonify({'error': 'Invalid test type or responses'}), 400

    # Map question IDs to traits from PERSONALITY_QUESTIONS
    question_traits = {str(q['id']): (q['trait'], q['direction']) for q in PERSONALITY_QUESTIONS}
    questions = PERSONALITY_QUESTIONS  # Reference the global question set for completeness check

    # Initialize scores for Big Five traits
    scores = {
        'Openness': 0, 'Conscientiousness': 0, 'Extraversion': 0, 'Agreeableness': 0, 'Neuroticism': 0
    }
    question_counts = {trait: 0 for trait in scores}

    # Process responses
    responded_questions = set()
    for response in responses:
        question_id = str(response.get('questionId'))  # Ensure string comparison
        value = response.get('answer')
        if question_id not in question_traits or value is None:
            print(f"Invalid or missing response for question ID: {question_id}")
            continue
        try:
            value = int(value)
            if value < 0 or value > 4:  # Likert scale is 0-4
                print(f"Invalid answer value {value} for question {question_id}")
                continue
            trait, direction = question_traits[question_id]
            responded_questions.add(question_id)
            question_counts[trait] += 1  # Increment count for this trait
            scores[trait] += (4 - value) if not direction else value  # Reverse scoring if needed
        except ValueError:
            print(f"Non-integer answer provided for question {question_id}: {value}")
            continue

    # Check if all questions were answered
    if len(responded_questions) != len(questions):
        unanswered = len(questions) - len(responded_questions)
        print(f"Warning: {unanswered} questions were not answered.")

    # Calculate percentage scores for each trait
    for trait in scores:
        if question_counts[trait] > 0:
            max_score = question_counts[trait] * 4  # Max possible score (0-4 per question)
            scores[trait] = (scores[trait] / max_score) * 100  # Convert to percentage
        else:
            scores[trait] = 0  # Default to 0 if no questions for this trait

    # Determine dominant trait
    dominant_trait = max(scores, key=scores.get)
    
    # Save result to database
    result = TestResult(
        user_id=current_user.id,
        test_type='personality',
        score=int(scores[dominant_trait]),
        time_spent=duration,
        details=json.dumps(scores)
    )
    db.session.add(result)

    # Award "First Test" Badge if not already earned
    if not Badge.query.filter_by(user_id=current_user.id, name="First Test Completed").first():
        badge = Badge(
            user_id=current_user.id,
            name="First Test Completed",
            description="Completed your first test!",
            icon="fas fa-trophy"
        )
        db.session.add(badge)

    # Award "High Scorer" Badge if score is high
    if scores[dominant_trait] >= 80:
        if not Badge.query.filter_by(user_id=current_user.id, name="High Scorer").first():
            badge = Badge(
                user_id=current_user.id,
                name="High Scorer",
                description="Scored 80% or higher on a test!",
                icon="fas fa-star"
            )
            db.session.add(badge)

    # Add Notification
    notification = Notification(
        user_id=current_user.id,
        message=f"You completed the Personality Test! Dominant trait: {dominant_trait} ({scores[dominant_trait]:.1f}%)",
        type="test_result"
    )
    db.session.add(notification)
    
    # Commit all changes to the database
    db.session.commit()

    # Prepare trait names for results page
    trait_names = {
        'Openness': 'Openness to Experience',
        'Conscientiousness': 'Conscientiousness',
        'Extraversion': 'Extraversion',
        ' Agreeableness': ' Agreeableness',
        'Neuroticism': 'Neuroticism'
    }

    # Return redirect URL as JSON
    return jsonify({
        'redirect': url_for('personality_results',
                           scores=json.dumps(scores),  # Pass as JSON string
                           dominant_trait=dominant_trait,
                           trait_names=json.dumps(trait_names))  # Pass as JSON string
    })
    
@app.route('/submit_aptitude', methods=['POST'])
@login_required
def submit_aptitude():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    responses = data.get('responses', [])
    time_spent = data.get('time_spent', 0)
    current_question_index = data.get('current_question_index', 0)
    questions = session.get('aptitude_questions', [])
    
    if not questions or current_question_index >= len(questions):
        return jsonify({'error': 'Invalid question index or no questions in session'}), 400
    
    # Process current response
    correct = session.get('aptitude_correct', 0)
    total = session.get('aptitude_total', 0)
    category_scores = session.get('aptitude_category_scores', defaultdict(int))
    category_counts = session.get('aptitude_category_counts', defaultdict(int))
    
    current_response = responses[-1] if responses else None
    if current_response:
        question_id = str(current_response.get('questionId'))
        answer = current_response.get('answer')
        question = next((q for q in questions if q['id'] == question_id), None)
        if question and answer is not None:
            category = next((cat for cat, levels in APTITUDE_QUESTIONS.items() if any(question['id'] in [q['id'] for q in level] for level in levels.values())), "Unknown")
            category_counts[category] += 1
            total += 1
            if int(answer) == question['correct']:
                correct += 1
                category_scores[category] += 1
    
    session['aptitude_correct'] = correct
    session['aptitude_total'] = total
    session['aptitude_category_scores'] = dict(category_scores)
    session['aptitude_category_counts'] = dict(category_counts)
    
    # Adjust difficulty for next question
    performance = correct / total if total > 0 else 0
    current_difficulty = 'easy'
    if total >= 3:  # Adjust after a few questions
        if performance >= 0.75 and current_question_index < len(questions) - 1:
            current_difficulty = 'hard'
        elif performance >= 0.5:
            current_difficulty = 'moderate'
        else:
            current_difficulty = 'easy'
    
    # If last question, save results
    if current_question_index == len(questions) - 1:
        score = (correct / total) * 100 if total > 0 else 0
        detailed_scores = {cat: (category_scores[cat] / category_counts[cat]) * 100 for cat in category_scores if category_counts[cat] > 0}
        result = TestResult(
            user_id=current_user.id,
            test_type='aptitude',
            score=score,
            time_spent=time_spent,
            details=json.dumps(detailed_scores)
        )
        db.session.add(result)
        if not Badge.query.filter_by(user_id=current_user.id, name="First Test Completed").first():
            badge = Badge(user_id=current_user.id, name="First Test Completed", description="Completed your first test!", icon="fas fa-trophy")
            db.session.add(badge)
        if score >= 80:
            if not Badge.query.filter_by(user_id=current_user.id, name="High Scorer").first():
                badge = Badge(user_id=current_user.id, name="High Scorer", description="Scored 80% or higher on a test!", icon="fas fa-star")
                db.session.add(badge)
        notification = Notification(
            user_id=current_user.id,
            message=f"You completed the Aptitude Test with a score of {score:.1f}%!",
            type="test_result"
        )
        db.session.add(notification)
        db.session.commit()
        session.pop('aptitude_questions', None)
        session.pop('aptitude_correct', None)
        session.pop('aptitude_total', None)
        session.pop('aptitude_category_scores', None)
        session.pop('aptitude_category_counts', None)
        return jsonify({'redirect': url_for('results')})
    
    # Get next question based on adjusted difficulty
    next_index = current_question_index + 1
    available_questions = copy.deepcopy(APTITUDE_QUESTIONS)
    for q in questions[:next_index]:
        for cat in available_questions:
            for diff in available_questions[cat]:
                available_questions[cat][diff] = [aq for aq in available_questions[cat][diff] if aq['id'] != q['id']]
    
    category = random.choice(list(available_questions.keys()))
    next_questions = available_questions[category][current_difficulty]
    if not next_questions:
        for diff in ['easy', 'moderate', 'hard']:
            if available_questions[category][diff]:
                next_questions = available_questions[category][diff]
                break
    next_question = random.choice(next_questions) if next_questions else questions[next_index]
    
    questions[next_index] = next_question
    session['aptitude_questions'] = questions
    
    return jsonify({
        'question': next_question,
        'current_question_index': next_index,
        'total_questions': len(questions)
    })
    
@app.route('/submit_skill_gap', methods=['POST'])
@login_required
def submit_skill_gap():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    responses = data.get('responses', [])
    time_spent = data.get('time_spent', 0)
    current_question_index = data.get('current_question_index', 0)
    questions = session.get('skill_gap_questions', [])
    
    if not questions or current_question_index >= len(questions):
        return jsonify({'error': 'Invalid question index or no questions in session'}), 400
    
    # Process current response
    correct = session.get('skill_gap_correct', 0)
    total = session.get('skill_gap_total', 0)
    current_response = responses[-1] if responses else None
    if current_response:
        question_id = str(current_response.get('questionId'))
        answer = current_response.get('answer')
        question = next((q for q in questions if q['id'] == question_id), None)
        if question and answer is not None:
            total += 1
            if int(answer) == question['correct']:
                correct += 1
    
    session['skill_gap_correct'] = correct
    session['skill_gap_total'] = total
    
    # If last question, save results and map to careers
    if current_question_index == len(questions) - 1:
        skill_score = (correct / total) * 100 if total > 0 else 0
        selected_field = session.get('selected_field', 'Software Development')
        detailed_scores = {selected_field: skill_score}
        result = TestResult(
            user_id=current_user.id,
            test_type='skill_gap',
            score=skill_score,
            time_spent=time_spent,
            details=json.dumps(detailed_scores)
        )
        db.session.add(result)
        if not Badge.query.filter_by(user_id=current_user.id, name="First Test Completed").first():
            badge = Badge(user_id=current_user.id, name="First Test Completed", description="Completed your first test!", icon="fas fa-trophy")
            db.session.add(badge)
        if skill_score >= 80:
            if not Badge.query.filter_by(user_id=current_user.id, name="High Scorer").first():
                badge = Badge(user_id=current_user.id, name="High Scorer", description="Scored 80% or higher on a test!", icon="fas fa-star")
                db.session.add(badge)
        notification = Notification(
            user_id=current_user.id,
            message=f"You completed the Skill Gap Test for {selected_field} with a score of {skill_score:.1f}%!",
            type="test_result"
        )
        db.session.add(notification)
        db.session.commit()
        session.pop('skill_gap_questions', None)
        session.pop('skill_gap_correct', None)
        session.pop('skill_gap_total', None)
        return jsonify({'redirect': url_for('career_match')})
    
    # Return next question
    next_index = current_question_index + 1
    next_question = questions[next_index]
    return jsonify({
        'question': next_question,
        'current_question_index': next_index,
        'total_questions': len(questions)
    })
    
@app.route('/submit_interests', methods=['POST'])
@login_required
def submit_interests():
    field = request.form.get('field')
    if not field or field not in SKILL_GAP_QUESTIONS:
        flash('Invalid field selected.', 'danger')
        return redirect(url_for('interest_test'))

    questions = SKILL_GAP_QUESTIONS[field]
    print(f"Processing questions for field {field}: {questions}")  # Debug print
    correct = 0
    total = len(questions)
    for question in questions:
        answer = request.form.get(str(question['id']))
        if answer is not None and int(answer) == question['correct']:
            correct += 1
    
    skill_score = (correct / total) * 100
    detailed_scores = {field: skill_score}

    result = TestResult(
        user_id=current_user.id,
        test_type='skill_gap',
        score=skill_score,
        details=json.dumps(detailed_scores)
    )
    db.session.add(result)
    # Award "First Test" Badge if not already earned
    if not Badge.query.filter_by(user_id=current_user.id, name="First Test Completed").first():
        badge = Badge(
            user_id=current_user.id,
            name="First Test Completed",
            description="Completed your first test!",
            icon="fas fa-trophy"
        )
        db.session.add(badge)
    # Award "High Scorer" Badge if score is high
    if skill_score >= 80:
        if not Badge.query.filter_by(user_id=current_user.id, name="High Scorer").first():
            badge = Badge(
                user_id=current_user.id,
                name="High Scorer",
                description="Scored 80% or higher on a test!",
                icon="fas fa-star"
            )
            db.session.add(badge)
    # Add Notification
    notification = Notification(
        user_id=current_user.id,
        message=f"You completed the Skill Gap Test for {field} with a score of {skill_score:.1f}%!",
        type="test_result"
    )
    db.session.add(notification)
    db.session.commit()

    return redirect(url_for('career_match'))

@app.route('/personality_results')
@login_required
def personality_results():
    scores_json = request.args.get('scores')
    dominant_trait = request.args.get('dominant_trait')
    trait_names_json = request.args.get('trait_names')
    
    if not scores_json or not dominant_trait or not trait_names_json:
        flash('Invalid results data.', 'danger')
        return redirect(url_for('dashboard'))
    
    scores = json.loads(scores_json)
    trait_names = json.loads(trait_names_json)
    
    return render_template(
        'personality_results.html',
        scores=scores,
        dominant_trait=dominant_trait,
        trait_names=trait_names,
        active_page='personality_results'
    )

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

@app.route('/career_match', methods=['GET', 'POST'])
@login_required
def career_match():
    results = TestResult.query.filter_by(user_id=current_user.id).all()
    has_aptitude = any(r.test_type == 'aptitude' for r in results)
    has_personality = any(r.test_type == 'personality' for r in results)
    has_skill_gap = any(r.test_type == 'skill_gap' for r in results)
    
    if request.method == 'POST' and 'take_skill_gap' in request.form:
        if request.form['take_skill_gap'] == 'yes':
            return redirect(url_for('interest_test'))
    
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
            for career, weights in CAREER_MAPPING.items():
                score = sum(aptitude_scores.get(cat, 0) * weight / 100 
                           for cat, weight in weights['aptitude'].items())
                career_scores[career] += score * 0.4
        elif result.test_type == 'personality':
            personality_scores = details
            for career, weights in CAREER_MAPPING.items():
                score = sum(personality_scores.get(trait.strip(), 0) * weight / 100 
                           for trait, weight in weights['personality'].items())
                career_scores[career] += score * 0.3
        elif result.test_type == 'skill_gap':
            skill_scores = details
            for career, weights in CAREER_MAPPING.items():
                for skill, weight in weights['skills'].items():
                    if skill in skill_scores:
                        career_scores[career] += (skill_scores[skill] * weight / 100) * 0.3

    career_matches = []
    for career, data in CAREER_MAPPING.items():
        soc_code = data.get('soc_code', '15-1252.00')  # Default to Software Developer SOC if missing
        career_data = onet_api.get_career_details(soc_code)
        career_matches.append({
            'career': career,
            'match_score': career_scores.get(career, 0),
            'description': data['description'],
            'resources': data['resources'],
            'requirements': {
                'aptitude': data['aptitude'],
                'personality': data['personality'],
                'skills': list(data['skills'].keys()),
                'education': career_data.get('education', {}).get('typical', 'Not specified'),
                'experience': career_data.get('experience', {}).get('typical', 'Not specified')
            },
            'salary': career_data.get('wages', {}).get('median', 0) or 0,
            'scope': career_data.get('job_outlook', {}).get('growth_rate', 0) or 0
        })
    career_matches.sort(key=lambda x: x['match_score'], reverse=True)
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
    return render_template(
        'career_match.html',
        career_matches=career_matches[:5],
        has_aptitude=has_aptitude,
        has_personality=has_personality,
        has_skill_gap=has_skill_gap,
        active_page='career_match',
        notifications=notifications
    )
    
@app.route('/progress_tracking')
@login_required
def progress_tracking():
    test_history = TestResult.query.filter_by(user_id=current_user.id).order_by(TestResult.completed_at.asc()).all()
    total_tests = len(test_history)
    if total_tests == 0:
        flash('No tests taken yet. Take a test to track your progress!', 'info')
        return redirect(url_for('test'))
    
    test_types = ['sample', 'aptitude', 'personality']
    avg_scores = {}
    for test_type in test_types:
        tests = [test for test in test_history if test.test_type == test_type]
        if tests:
            max_score = 9 if test_type == 'sample' else (5 if test_type == 'personality' else 10)
            avg_scores[test_type] = sum(test.score for test in tests) / len(tests) / max_score * 100
        else:
            avg_scores[test_type] = 0

    progress_data = {
        'labels': [test.completed_at.strftime('%Y-%m-%d') for test in test_history],
        'scores': [(test.score / (9 if test.test_type == 'sample' else (5 if test.test_type == 'personality' else 10)) * 100) for test in test_history],
        'types': [test.test_type for test in test_history]
    }

    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
    return render_template('progress_tracking.html', user=current_user, test_history=test_history, 
                          avg_scores=avg_scores, progress_data=progress_data, active_page='progress_tracking', notifications=notifications)

@app.route('/profile')
@login_required
def profile():
    test_history = TestResult.query.filter_by(user_id=current_user.id).order_by(TestResult.completed_at.desc()).all()
    badges = Badge.query.filter_by(user_id=current_user.id).order_by(Badge.date_earned.desc()).all()
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
    return render_template('profile.html', user=current_user, test_history=test_history, badges=badges, active_page='profile', notifications=notifications)

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

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        msg = Message(subject=f"Contact Form Submission from {name}",
                      recipients=['abc@gmail.com'],
                      body=f"Name: {name}\nEmail: {email}\nMessage: {message}")
        try:
            mail.send(msg)
            flash('Your message has been sent successfully!', 'success')
            return redirect(url_for('contact'))
        except Exception as e:
            print(f"Error sending email: {e}")
            flash('Failed to send message. Please try again later.', 'danger')
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all() if current_user.is_authenticated else []
    return render_template('contact.html',form=form, active_page='contact', notifications=notifications)

@app.route('/faq')
def faq():
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all() if current_user.is_authenticated else []
    return render_template('faq.html', active_page='faq', notifications=notifications)

@app.route('/roadmap')
@login_required
def roadmap():
    test_history = TestResult.query.filter_by(user_id=current_user.id).order_by(TestResult.completed_at.asc()).all()
    total_tests = len(test_history)
    milestones_completed = min(total_tests // 2, 4)
    avg_score = sum(test.score for test in test_history) / max(total_tests, 1) if total_tests > 0 else 0
    if avg_score > 7:
        destination = "Senior Tech Lead"
    elif avg_score > 5:
        destination = "Tech Lead"
    else:
        destination = "Junior Developer"
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
    return render_template('roadmap.html', 
                         milestones_completed=milestones_completed, 
                         destination=destination, 
                         animations_enabled=current_user.animations_enabled,
                         active_page='roadmap',
                         notifications=notifications)

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
    app.run(debug=True, host='0.0.0.0', port=5001)