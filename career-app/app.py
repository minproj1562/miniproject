from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_mail import Mail, Message
from flask_migrate import Migrate
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Replace with a secure key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///career_analytics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'abc@gmail.com'  # REPLACE with your Gmail address
app.config['MAIL_PASSWORD'] = 'your-app-password-here'  # REPLACE with your Gmail App Password
app.config['MAIL_DEFAULT_SENDER'] = 'abc@gmail.com'  # REPLACE with your Gmail address

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)  # Initialize Flask-Migrate

# Add custom Jinja2 filter for datetime formatting
def datetimeformat(value, format='%Y'):
    if value == 'now':
        return datetime.now().strftime(format)
    return value
app.jinja_env.filters['datetimeformat'] = datetimeformat

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

class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    test_type = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    time_spent = db.Column(db.Integer, nullable=True)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def generate_questions(test_type):
    if test_type == 'sample':
        return [
            {"id": "q1", "question": "How often do you meet deadlines?", "options": ["Always", "Usually", "Sometimes", "Rarely"]},
            {"id": "q2", "question": "Do you take initiative at work?", "options": ["Always", "Usually", "Sometimes", "Rarely"]},
            {"id": "q3", "question": "How well do you collaborate?", "options": ["Always", "Usually", "Sometimes", "Rarely"]}
        ]
    elif test_type == 'aptitude':
        return {
            "Mathematics": {
                "easy": [
                    {"id": "m1", "text": "2 + 2 = ?", "options": ["3", "4", "5"], "correct": 1, "time_limit": 10},
                    {"id": "m2", "text": "10 - 3 = ?", "options": ["6", "7", "8"], "correct": 1, "time_limit": 10}
                ],
                "medium": [
                    {"id": "m3", "text": "5 * 6 = ?", "options": ["30", "25", "35"], "correct": 0, "time_limit": 15},
                    {"id": "m4", "text": "12 / 3 = ?", "options": ["4", "5", "3"], "correct": 0, "time_limit": 15}
                ]
            },
            "Logical Reasoning": {
                "easy": [
                    {"id": "l1", "text": "If A then B. A is true. Is B true?", "options": ["Yes", "No"], "correct": 0, "time_limit": 20},
                    {"id": "l2", "text": "All cats are mammals. Tom is a cat. Is Tom a mammal?", "options": ["Yes", "No"], "correct": 0, "time_limit": 20}
                ]
            },
            "Verbal Ability": {
                "easy": [
                    {"id": "v1", "text": "Synonym of 'Happy'?", "options": ["Sad", "Joyful", "Angry"], "correct": 1, "time_limit": 10},
                    {"id": "v2", "text": "Antonym of 'Big'?", "options": ["Large", "Small", "Huge"], "correct": 1, "time_limit": 10}
                ]
            }
        }
    return []

@app.route('/')
def index():
    if not current_user.is_authenticated and not session.get('_flashes'):
        flash('Kindly log in to unlock comprehensive access to all features.', 'info')
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=request.form.get('remember_me') == 'on')
            next_page = request.args.get('next', url_for('dashboard'))
            return redirect(next_page)
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', csrf_token=generate_csrf())

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        email = request.form.get('email', None)
        captcha = request.form.get('captcha')
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
        elif captcha != '5':
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
    return render_template('register.html', csrf_token=generate_csrf())

@app.route('/dashboard')
@login_required
def dashboard():
    recent_tests = TestResult.query.filter_by(user_id=current_user.id).order_by(TestResult.completed_at.desc()).limit(5).all()
    test_data = {
        'labels': [test.completed_at.strftime('%Y-%m-%d %H:%M') for test in recent_tests[::-1]],
        'scores': [test.score / 9 * 100 if test.test_type == 'sample' else test.score / 8 * 100 for test in recent_tests[::-1]],
        'types': [test.test_type for test in recent_tests[::-1]]
    }
    recommendation = "Take more tests for personalized advice!"
    if len(recent_tests) >= 3:
        recommendation = "You're doing great! Consider exploring advanced career options."
    return render_template('dashboard.html', user=current_user, recent_tests=recent_tests, test_data=test_data, recommendation=recommendation)

@app.route('/student')
@login_required
def student():
    return render_template('student.html', user=current_user)

@app.route('/degree')
@login_required
def degree():
    degrees = [
        {"title": "Bachelor of Science in Computer Science", "university": "University of Technology", "duration": "4 years", "description": "Focuses on programming and systems."},
        {"title": "Master of Business Administration", "university": "Global Business School", "duration": "2 years", "description": "Prepares for leadership roles."},
        {"title": "Bachelor of Arts in Psychology", "university": "Riverside University", "duration": "3 years", "description": "Explores human behavior."},
        {"title": "Master of Science in Data Science", "university": "Tech Institute", "duration": "1.5 years", "description": "Analyzes big data."}
    ]
    return render_template('degree.html', user=current_user, degrees=degrees)

@app.route('/test', methods=['GET'])
def test():
    test_type = request.args.get('type')
    if test_type == 'sample':
        questions = generate_questions('sample')
        return render_template('sample_test.html', questions=questions, csrf_token=generate_csrf())
    elif test_type == 'aptitude':
        if not current_user.is_authenticated:
            flash('Kindly log in to unlock comprehensive access to all features.', 'warning')
            return redirect(url_for('login', next=request.url))
        questions = generate_questions('aptitude')
        total_questions = sum(len(lvl) for cat in questions.values() for lvl in cat.values())
        return render_template('aptitude_test.html', questions=questions, initial_time=60, 
                              total_questions=total_questions, current_category="Mathematics", 
                              completed_questions=0, csrf_token=generate_csrf())
    return render_template('test.html')

@app.route('/test', methods=['POST'])
def test_post():
    test_type = request.args.get('type')
    if test_type == 'sample':
        questions = generate_questions('sample')
        if request.form:
            score = sum(3 - int(request.form.get(q['id'], 0)) for q in questions)
            result = TestResult(
                user_id=current_user.id if current_user.is_authenticated else None,
                test_type='sample', 
                score=score
            )
            db.session.add(result)
            db.session.commit()
            flash(f'Your work ethics score: {score} out of {len(questions) * 3}', 'success')
            return redirect(url_for('index'))
        return render_template('sample_test.html', questions=questions, csrf_token=generate_csrf())
    elif test_type == 'aptitude':
        if not current_user.is_authenticated:
            flash('Kindly log in to unlock comprehensive access to all features.', 'warning')
            return redirect(url_for('login', next=request.url))
        questions = generate_questions('aptitude')
        if request.form:
            time_spent = int(request.form.get('time_spent', 0))
            all_questions = [q for cat in questions.values() for lvl in cat.values() for q in lvl]
            correct = sum(1 for q in all_questions if request.form.get(q['id']) == str(q['correct']))
            total = len(all_questions)
            score = correct
            score_data = {
                'score': (correct / total) * 100,
                'correct': correct,
                'total': total,
                'time_spent': time_spent
            }
            result = TestResult(user_id=current_user.id, test_type='aptitude', score=score, time_spent=time_spent)
            db.session.add(result)
            db.session.commit()
            return render_template('results.html', score_data=score_data)
        total_questions = sum(len(lvl) for cat in questions.values() for lvl in cat.values())
        return render_template('aptitude_test.html', questions=questions, initial_time=60, 
                              total_questions=total_questions, current_category="Mathematics", 
                              completed_questions=0, csrf_token=generate_csrf())
    flash('Invalid test type.', 'danger')
    return redirect(url_for('test'))

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
                    return render_template('profile_edit.html', user=current_user, csrf_token=generate_csrf())
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile'))
    return render_template('profile_edit.html', user=current_user, csrf_token=generate_csrf())

@app.route('/forgot_password')
def forgot_password():
    flash('Password reset is not yet implemented. Please contact support.', 'warning')
    return redirect(url_for('login'))

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
                          recipients=['abc@gmail.com'],  # REPLACE with your Gmail address
                          body=f"Name: {name}\nEmail: {email}\nMessage: {message}")
            try:
                mail.send(msg)
                flash('Your message has been sent successfully!', 'success')
                return redirect(url_for('contact'))
            except Exception as e:
                print(f"Error sending email: {e}")
                flash('Failed to send message. Please try again later.', 'danger')
    return render_template('contact.html', csrf_token=generate_csrf())

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
        # Theme Toggle
        if 'theme' in request.form:
            theme = request.form['theme']
            current_user.theme = theme
            db.session.commit()
            flash('Theme updated successfully!', 'success')
        # Animation Toggle
        elif 'animations' in request.form:
            animations = request.form.get('animations') == 'on'
            current_user.animations_enabled = animations
            db.session.commit()
            flash('Animation settings updated!', 'success')
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
        # Reset Roadmap Progress
        elif 'reset_roadmap' in request.form:
            current_user.tests = []  # Clear test results
            db.session.commit()
            flash('Roadmap progress reset successfully!', 'success')
        # Delete Account
        elif 'delete_account' in request.form:
            db.session.delete(current_user)
            db.session.commit()
            logout_user()
            flash('Your account has been deleted.', 'info')
            return redirect(url_for('index'))
    return render_template('settings.html', user=current_user, csrf_token=generate_csrf())

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '_main_':
    app.run(debug=True, host='0.0.0.0', port=5000)