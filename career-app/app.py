import os
import sys
print(f"Python path: {sys.path}")
print(f"Current directory: {os.getcwd()}")

from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail, Message
from flask_migrate import Migrate
from datetime import datetime, timedelta
import secrets
import requests
import random
import copy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError

# Load environment variables
from dotenv import load_dotenv
load_dotenv()
print(f"Loaded ONET_USER: {os.getenv('ONET_USER')}")
print(f"Loaded ONET_PWD: {os.getenv('ONET_PWD')}")

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
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

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Initialize extensions
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

csrf = CSRFProtect(app)
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

# User model
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

class PasswordReset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(100), nullable=False, unique=True)
    expires_at = db.Column(db.DateTime, nullable=False)
    user = db.relationship('User', backref='password_resets')

# TestResult model
class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    test_type = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    time_spent = db.Column(db.Integer, nullable=True)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    email = EmailField('Email', validators=[Email(), Length(max=150)], render_kw={"placeholder": "Optional"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    captcha = StringField('Verification: What is 2 + 3?', validators=[DataRequired()])
    submit = SubmitField('Register')
class SampleTestForm(FlaskForm):
    submit = SubmitField('Submit Test')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already registered. Please use a different one.')

    def validate_captcha(self, captcha):
        if captcha.data != '5':
            raise ValidationError('Verification failed. Please enter the correct answer (2 + 3 = 5).')

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Lazy import of ONetAPI to avoid circular imports
def get_onet_api():
    from apis import ONetAPI
    return ONetAPI()

# Aptitude Questions Definition
APTITUDE_QUESTIONS = {
    "Mathematics": {
        "easy": [
            {"id": "M1-E", "type": "numerical", "text": "Solve: 15 + 8 × 3 ÷ 4", "options": ["21", "18.5", "19.5", "20.25"], "correct": 2, "time_limit": 60},
            {"id": "M4-E", "type": "geometry", "text": "What is the area of a rectangle with length 5 cm and width 3 cm?", "options": ["15 cm²", "16 cm²", "18 cm²", "20 cm²"], "correct": 0, "time_limit": 45}
        ],
        "moderate": [
            {"id": "M2-M", "type": "algebra", "text": "If x + y = 15 and 2x - y = 6, what is the value of x?", "options": ["7", "8", "9", "10"], "correct": 0, "time_limit": 90},
            {"id": "M5-M", "type": "statistics", "text": "Find the median of: 3, 7, 2, 8, 5", "options": ["5", "6", "7", "8"], "correct": 0, "time_limit": 75}
        ],
        "hard": [
            {"id": "M3-H", "type": "calculus", "text": "What is the derivative of f(x) = 3x² + 2eˣ - ln(x)?", "options": ["6x + 2eˣ - 1/x", "6x + 2eˣ + 1/x", "3x + 2eˣ - 1/x²", "6x + eˣ - 1/x"], "correct": 0, "time_limit": 120},
            {"id": "M6-H", "type": "probability", "text": "A bag has 4 red and 6 blue balls. What’s the probability of drawing 2 red balls in a row without replacement?", "options": ["1/15", "2/15", "4/45", "6/45"], "correct": 2, "time_limit": 150}
        ]
    },
    "Logical Reasoning": {
        "easy": [
            {"id": "LR1-E", "type": "pattern", "text": "Complete the sequence: A, C, E, G, ___", "options": ["H", "I", "J", "K"], "correct": 1, "time_limit": 45},
            {"id": "LR4-E", "type": "analogy", "text": "Bird is to Fly as Fish is to ___", "options": ["Swim", "Walk", "Jump", "Crawl"], "correct": 0, "time_limit": 40}
        ],
        "moderate": [
            {"id": "LR2-M", "type": "deductive", "text": "All managers are leaders. Some leaders are visionary. Therefore:", "options": ["All managers are visionary", "Some managers may be visionary", "No managers are visionary", "Visionary people cannot be managers"], "correct": 1, "time_limit": 75},
            {"id": "LR5-M", "type": "syllogism", "text": "Some A are B. All B are C. Therefore:", "options": ["All A are C", "Some A are C", "No A are C", "All C are A"], "correct": 1, "time_limit": 90}
        ],
        "hard": [
            {"id": "LR3-H", "type": "analytical", "text": "If 3★5 = 16, 4★7 = 30, then 5★9 = ___", "options": ["44", "46", "48", "50"], "correct": 1, "time_limit": 150},
            {"id": "LR6-H", "type": "logic_puzzle", "text": "Three friends rank 1st, 2nd, 3rd in a race. A is not last, B is ahead of C. Who is 2nd?", "options": ["A", "B", "C", "Cannot determine"], "correct": 0, "time_limit": 180}
        ]
    },
    "Verbal Ability": {
        "easy": [
            {"id": "VA1-E", "type": "vocabulary", "text": "Select the antonym of EPHEMERAL:", "options": ["Transient", "Enduring", "Fleeting", "Momentary"], "correct": 1, "time_limit": 45},
            {"id": "VA4-E", "type": "synonym", "text": "Find a synonym for 'Benevolent':", "options": ["Kind", "Harsh", "Greedy", "Silent"], "correct": 0, "time_limit": 40}
        ],
        "moderate": [
            {"id": "VA2-M", "type": "comprehension", "text": "'The company’s pecuniary situation was precarious.' What does 'pecuniary' mean?", "options": ["Legal", "Financial", "Ethical", "Structural"], "correct": 1, "time_limit": 60},
            {"id": "VA5-M", "type": "sentence_completion", "text": "Her ___ attitude inspired the team to exceed their goals.", "options": ["apathetic", "motivating", "indifferent", "hostile"], "correct": 1, "time_limit": 70}
        ],
        "hard": [
            {"id": "VA3-H", "type": "critical_reasoning", "text": "Which weakens: 'Remote work increases productivity because employees save commute time'?", "options": ["Commute time averages 45 minutes daily", "Home distractions reduce focused work hours", "Companies report higher profits with remote teams", "Video conferencing tools improve collaboration"], "correct": 1, "time_limit": 120},
            {"id": "VA6-H", "type": "analogies", "text": "Mitigate : Severity :: Amplify : ___", "options": ["Volume", "Calmness", "Silence", "Weakness"], "correct": 0, "time_limit": 100}
        ]
    }
}

# Personality Questions (Big Five Inventory) - Fixed Agreeableness trait names
PERSONALITY_QUESTIONS = [
    # Openness (O) - 8 items
    {"id": 1, "trait": "Openness", "text": "I enjoy hearing new ideas", "direction": True, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 2, "trait": "Openness", "text": "I avoid philosophical discussions", "direction": False, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 3, "trait": "Openness", "text": "I have a vivid imagination", "direction": True, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 4, "trait": "Openness", "text": "I prefer routine over variety", "direction": False, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 5, "trait": "Openness", "text": "I appreciate abstract art", "direction": True, "likert_scale": ["Strongly Disagree", "Disagree", "Nuclear", "Agree", "Strongly Agree"]},
    {"id": 6, "trait": "Openness", "text": "I dislike complex theoretical concepts", "direction": False, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 7, "trait": "Openness", "text": "I enjoy trying new cultural experiences", "direction": True, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 8, "trait": "Openness", "text": "I prefer practical over creative tasks", "direction": False, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    
    # Conscientiousness (C) - 8 items
    {"id": 11, "trait": "Conscientiousness", "text": "I pay attention to details", "direction": True, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 12, "trait": "Conscientiousness", "text": "I often forget to put things back in their proper place", "direction": False, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 13, "trait": "Conscientiousness", "text": "I complete tasks thoroughly", "direction": True, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 14, "trait": "Conscientiousness", "text": "I often procrastinate important tasks", "direction": False, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 15, "trait": "Conscientiousness", "text": "I follow through on my commitments", "direction": True, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 16, "trait": "Conscientiousness", "text": "I struggle with time management", "direction": False, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 17, "trait": "Conscientiousness", "text": "I keep my living space organized", "direction": True, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 18, "trait": "Conscientiousness", "text": "I often make careless mistakes", "direction": False, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    
    # Extraversion (E) - 8 items
    {"id": 21, "trait": "Extraversion", "text": "I feel comfortable around people", "direction": True, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 22, "trait": "Extraversion", "text": "I prefer quiet evenings at home to parties", "direction": False, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 23, "trait": "Extraversion", "text": "I am the life of the party", "direction": True, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 24, "trait": "Extraversion", "text": "Large social gatherings drain my energy", "direction": False, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 25, "trait": "Extraversion", "text": "I enjoy being the center of attention", "direction": True, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 26, "trait": "Extraversion", "text": "I find it hard to start conversations", "direction": False, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 27, "trait": "Extraversion", "text": "I make friends easily", "direction": True, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 28, "trait": "Extraversion", "text": "I prefer working alone rather than in teams", "direction": False, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    
    # Agreeableness (A) - 8 items (Removed leading spaces)
    {"id": 31, "trait": "Agreeableness", "text": "I sympathize with others' feelings", "direction": True, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 32, "trait": "Agreeableness", "text": "I often argue with authority figures", "direction": False, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 33, "trait": "Agreeableness", "text": "I trust others' intentions", "direction": True, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 34, "trait": "Agreeableness", "text": "I enjoy competitive situations more than cooperative ones", "direction": False, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 35, "trait": "Agreeableness", "text": "I go out of my way to help others", "direction": True, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 36, "trait": "Agreeableness", "text": "I sometimes take advantage of others", "direction": False, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 37, "trait": "Agreeableness", "text": "I value harmony in relationships", "direction": True, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 38, "trait": "Agreeableness", "text": "I enjoy debating controversial topics", "direction": False, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    
    # Neuroticism (N) - 8 items
    {"id": 41, "trait": "Neuroticism", "text": "I often feel tense or anxious", "direction": True, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 42, "trait": "Neuroticism", "text": "I remain calm under pressure", "direction": False, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 43, "trait": "Neuroticism", "text": "I worry about things that might go wrong", "direction": True, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 44, "trait": "Neuroticism", "text": "I rarely feel sad or depressed", "direction": False, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 45, "trait": "Neuroticism", "text": "I often feel emotionally vulnerable", "direction": True, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 46, "trait": "Neuroticism", "text": "I handle stress well", "direction": False, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 47, "trait": "Neuroticism", "text": "I often feel overwhelmed by my emotions", "direction": True, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]},
    {"id": 48, "trait": "Neuroticism", "text": "I rarely experience mood swings", "direction": False, "likert_scale": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]}
]

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

# Generate dynamic test questions
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
        questions = copy.deepcopy(APTITUDE_QUESTIONS)
        # Ensure at least one question per category and difficulty
        for category in questions:
            for difficulty in questions[category]:
                q_list = questions[category][difficulty]
                if q_list:
                    questions[category][difficulty] = [random.choice(q_list)]
        
        # Fetch additional questions from OpenTDB
        category_mapping = {"Mathematics": 19, "Logical Reasoning": 25, "Verbal Ability": 10}
        for category, cat_id in category_mapping.items():
            opentdb_qs = fetch_opentdb_questions(cat_id, 2)
            if opentdb_qs:
                questions[category]["easy"].extend(opentdb_qs[:2])  # Add 2 OpenTDB questions
        
        # Flatten and shuffle all questions
        flat_questions = [q for cat in questions.values() for lvl in cat.values() for q in lvl]
        random.shuffle(flat_questions)
        return flat_questions[:10]  # Limit to 10 questions
    elif test_type == 'personality':
        # Initialize traits dictionary with consistent keys
        traits = {'Openness': [], 'Conscientiousness': [], 'Extraversion': [], 'Agreeableness': [], 'Neuroticism': []}
        for q in PERSONALITY_QUESTIONS:
            traits[q['trait']].append(q)
        
        selected_questions = []
        for trait in traits:
            trait_qs = traits[trait]
            selected_questions.extend(random.sample(trait_qs, min(2, len(trait_qs))))  # 2 questions per trait for brevity
        
        random.shuffle(selected_questions)
        return selected_questions
    return []

# Routes
@app.route('/')
def index():
    if not current_user.is_authenticated and not session.get('_flashes'):
        flash('Kindly log in to unlock comprehensive access to all features.', 'info')
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next', url_for('dashboard'))
            return redirect(next_page)
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('auth/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password, email=form.email.data or None)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    recent_tests = TestResult.query.filter_by(user_id=current_user.id).order_by(TestResult.completed_at.desc()).limit(5).all()
    if recent_tests:
        test_data = {
            'labels': [test.completed_at.strftime('%Y-%m-%d %H:%M') for test in recent_tests[::-1]],
            'scores': [test.score / 9 * 100 if test.test_type == 'sample' else test.score / 8 * 100 for test in recent_tests[::-1]],
            'types': [test.test_type for test in recent_tests[::-1]]
        }
        recommendation = "Take more tests for personalized advice!"
        if len(recent_tests) >= 3:
            recommendation = "You're doing great! Consider exploring advanced career options."
    else:
        test_data = {
            'labels': [],
            'scores': [],
            'types': []
        }
        recommendation = "Start by taking a test to see your progress!"
    return render_template('dashboard.html', user=current_user, recent_tests=recent_tests, test_data=test_data, recommendation=recommendation)

@app.route('/student')
@login_required
def student():
    return render_template('student.html', user=current_user)

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

    return render_template('degree.html', user=current_user, degrees=filtered_degrees)

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
                        return render_template('sample_test.html', questions=questions, instructions=instructions)
                score = sum(3 - answers[q['id']] for q in questions)  # Reverse scoring: 3=Always, 0=Rarely
                result = TestResult(
                    user_id=current_user.id,
                    test_type='sample',
                    score=score
                )
                db.session.add(result)
                db.session.commit()
                flash(f'Your work ethics score: {score} out of {len(questions) * 3}', 'success')
                return redirect(url_for('index'))
            return render_template('sample_test.html', questions=questions, instructions=instructions)
        
    elif test_type == 'aptitude':
        questions = generate_questions('aptitude')
        session['aptitude_questions'] = questions
        if request.method == 'POST':
            if request.form:
                time_spent = int(request.form.get('time_spent', 0))
                correct = 0
                total = len(questions)
                for question in questions:
                    answer = request.form.get(str(question['id']))
                    if answer is not None and int(answer) == question['correct']:
                        correct += 1
                score = correct
                result = TestResult(user_id=current_user.id, test_type='aptitude', score=score, time_spent=time_spent)
                db.session.add(result)
                db.session.commit()
                flash(f'Your aptitude score: {score} out of {total}', 'success')
                return redirect(url_for('dashboard'))
            total_questions = len(questions)
            return render_template('assessments/aptitude.html.jinja2', questions=questions, instructions=instructions,
                                  current_category='Mathematics', total_questions=total_questions,
                                  initial_time=600, completed_questions=0)

    elif test_type == 'personality':
        questions = generate_questions('personality')
        session['personality_questions'] = questions
        if request.method == 'POST':
            flash('Personality test submission should use the /submit_assessment endpoint.', 'warning')
            return redirect(url_for('test', type='personality'))
        current_question_index = int(request.args.get('q', 0))
        if current_question_index < 0 or current_question_index >= len(questions):
            current_question_index = 0
        question = questions[current_question_index]
        return render_template('assessments/personality.html.jinja2',
                              questions=questions,
                              instructions=instructions,
                              current_question_index=current_question_index,
                              question=question)

    return render_template('assessments/test.html')

@app.route('/submit_assessment', methods=['POST'])
@login_required
def submit_assessment():
    data = request.get_json()
    test_type = data.get('type')
    responses = data.get('responses', [])
    duration = data.get('duration', 0)

    if test_type != 'personality':
        return jsonify({'error': 'Invalid test type'}), 400

    questions = session.get('personality_questions', generate_questions('personality'))
    scores = {'Openness': 0, 'Conscientiousness': 0, 'Extraversion': 0, 'Agreeableness': 0, 'Neuroticism': 0}
    question_traits = {str(q['id']): (q['trait'], q['direction']) for q in questions}

    for response in responses:
        question_id = response['questionId']
        value = int(response['answer'])
        trait, direction = question_traits.get(question_id, (None, True))
        if trait:
            if not direction:
                value = 4 - value  # Reverse scoring for reverse-scored items
            scores[trait] += value + 1  # Scale to 1-5

    # Normalize scores to percentage (assuming 2 questions per trait for simplicity)
    for trait in scores:
        count = sum(1 for q in questions if q['trait'] == trait)
        scores[trait] = (scores[trait] / (count * 5)) * 100 if count > 0 else 0

    dominant_trait = max(scores, key=scores.get)
    trait_names = {
        'Openness': 'Openness',
        'Conscientiousness': 'Conscientiousness',
        'Extraversion': 'Extraversion',
        'Agreeableness': 'Agreeableness',
        'Neuroticism': 'Neuroticism'
    }

    result = TestResult(
        user_id=current_user.id,
        test_type='personality',
        score=int(scores[dominant_trait]),
        time_spent=duration
    )
    db.session.add(result)
    db.session.commit()

    return jsonify({
        'redirect': url_for('personality_results', scores=scores, dominant_trait=dominant_trait, trait_names=trait_names)
    })

@app.route('/personality_results')
@login_required
def personality_results():
    scores = request.args.get('scores', '{}')
    dominant_trait = request.args.get('dominant_trait', 'N/A')
    trait_names = request.args.get('trait_names', '{}')

    # Convert stringified JSON to dictionary
    import json
    try:
        scores = json.loads(scores.replace("'", "\"")) if isinstance(scores, str) else scores
        trait_names = json.loads(trait_names.replace("'", "\"")) if isinstance(trait_names, str) else trait_names
    except json.JSONDecodeError:
        scores = {'Openness': 50, 'Conscientiousness': 50, 'Extraversion': 50, 'Agreeableness': 50, 'Neuroticism': 50}
        trait_names = {
            'Openness': 'Openness',
            'Conscientiousness': 'Conscientiousness',
            'Extraversion': 'Extraversion',
            'Agreeableness': 'Agreeableness',
            'Neuroticism': 'Neuroticism'
        }
        dominant_trait = 'Openness'

    return render_template('personality_results.html', scores=scores, dominant_trait=dominant_trait, trait_names=trait_names)

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

    return render_template('progress_tracking.html', user=current_user, test_history=test_history, 
                          avg_scores=avg_scores, progress_data=progress_data)

@app.route('/profile')
@login_required
def profile():
    test_history = TestResult.query.filter_by(user_id=current_user.id).order_by(TestResult.completed_at.desc()).all()
    return render_template('profile.html', user=current_user, test_history=test_history)

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        mobile_number = request.form.get('mobile_number')
        pin_code = request.form.get('pin_code')
        dob = request.form.get('dob')

        # Handle file upload
        file = request.files.get('profile_image')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{current_user.id}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
            current_user.profile_image = f"uploads/{unique_filename}"

        if email and email != current_user.email and User.query.filter_by(email=email).first():
            flash('Email already in use by another account.', 'danger')
        else:
            if password:
                current_user.password = generate_password_hash(password)
            current_user.email = email or current_user.email
            current_user.mobile_number = mobile_number or current_user.mobile_number
            current_user.pin_code = pin_code or current_user.pin_code
            if dob:
                try:
                    current_user.dob = datetime.strptime(dob, '%Y-%m-%d')
                except ValueError:
                    flash('Invalid date format for Date of Birth. Use YYYY-MM-DD.', 'danger')
                    return render_template('profile_edit.html', user=current_user)
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile'))
    return render_template('profile_edit.html', user=current_user)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('No account found with that email address.', 'danger')
            return redirect(url_for('forgot_password'))
        
        # Generate a reset token
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
        reset = PasswordReset(user_id=user.id, token=token, expires_at=expires_at)
        db.session.add(reset)
        db.session.commit()

        # Send reset email
        reset_link = url_for('reset_password', token=token, _external=True)
        msg = Message(subject='Password Reset Request',
                      recipients=[email],
                      body=f'Click the following link to reset your password: {reset_link}\nThis link will expire in 1 hour.')
        try:
            mail.send(msg)
            flash('A password reset link has been sent to your email.', 'success')
        except Exception as e:
            print(f"Error sending email: {e}")
            flash('Failed to send reset email. Please try again later.', 'danger')
        return redirect(url_for('login'))
    return render_template('auth/forgot_password.html')

# Add a reset_password route
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    reset = PasswordReset.query.filter_by(token=token).first()
    if not reset or reset.expires_at < datetime.utcnow():
        flash('The password reset link is invalid or has expired.', 'danger')
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
        elif len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
        else:
            user = reset.user
            user.password = generate_password_hash(password)
            db.session.delete(reset)  # Remove the reset token after use
            db.session.commit()
            flash('Your password has been reset successfully. Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('auth/reset_password.html', token=token)

@app.route('/results')
@login_required
def results():
    flash('Please complete an aptitude test to view results.', 'warning')
    return redirect(url_for('test'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        if not name or not email or not message:
            flash('All fields are required.', 'danger')
        else:
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
    return render_template('contact.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

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
    return render_template('roadmap.html', 
                         milestones_completed=milestones_completed, 
                         destination=destination, 
                         animations_enabled=current_user.animations_enabled)

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
    return render_template('settings.html', user=current_user)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)