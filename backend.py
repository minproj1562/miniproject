from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this to a secure secret key
db = SQLAlchemy(app)

# Define a User model for the registration form
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile_number = db.Column(db.String(15), nullable=False)
    pin_code = db.Column(db.String(6), nullable=False)
    dob = db.Column(db.String(10), nullable=False)  # Date of birth in format YYYY-MM-DD
    password = db.Column(db.String(120), nullable=False)

# Create the database tables (run this once to create the database)
with app.app_context():
    db.create_all()

# Sample questions and career mappings
APTITUDE_QUESTIONS = [
    {"id": 1, "subject": "Mathematics", "question": "Solving complex algebraic equations"},
    {"id": 2, "subject": "Science", "question": "Analyzing chemical reactions"},
    # Add more questions...
]

CAREER_MAPPINGS = {
    "Engineering": {"subjects": ["Mathematics", "Physics"], "score_range": [80, 100]},
    "Data Science": {"subjects": ["Mathematics", "Statistics"], "score_range": [70, 90]},
    # Add more mappings...
}

INTEREST_QUESTIONS = [
    {"id": 1, "activity": "Test the quality of parts before shipment", "category": "Technical"},
    {"id": 2, "activity": "Study the structure of the human body", "category": "Medical"},
    # Add more questions...
]

# Routes
@app.route('/')
def home():
    session.clear()
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        mobile_number = request.form['mobile_number']
        pin_code = request.form['pin_code']
        dob = request.form['dob']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Password and Confirm Password do not match!', 'danger')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already registered. Please use a different one.', 'danger')
            return redirect(url_for('register'))

        new_user = User(
            username=username,
            email=email,
            mobile_number=mobile_number,
            pin_code=pin_code,
            dob=dob,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your username and password.', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/aptitude-test')
def aptitude_test():
    return render_template('aptitude_test.html', questions=APTITUDE_QUESTIONS)

@app.route('/submit-aptitude', methods=['POST'])
def submit_aptitude():
    responses = request.form.to_dict()
    time_data = json.loads(request.form.get('time_data', '{}'))
    
    scores = {"Mathematics": 0, "Science": 0, "Total": 0}
    for q in APTITUDE_QUESTIONS:
        subject = q['subject']
        response = int(responses.get(f'q{q["id"]}', 0))
        time_weight = 1 - (time_data[str(q['id'])] / 180)  # 3min max per question
        scores[subject] += response * time_weight
        
    session['aptitude_scores'] = scores
    return redirect(url_for('results'))

@app.route('/results')
def results():
    aptitude = session.get('aptitude_scores')
    career = calculate_career(aptitude)
    return render_template('results.html', career=career)

def calculate_career(aptitude):
    for career, data in CAREER_MAPPINGS.items():
        if data['score_range'][0] <= aptitude['Total'] <= data['score_range'][1]:
            return career
    return "General Professional"

@app.route('/interest_test')
def interest_test():
    return render_template('interest_test.html', questions=INTEREST_QUESTIONS)

@app.route('/submit_interests', methods=['POST'])
def submit_interests():
    answers = request.form.to_dict()
    
    categories = {
        "Technical": 0,
        "Medical": 0,
        "Arts": 0,
        "Social": 0,
        "Business": 0,
        "Administrative": 0,
        "Scientific": 0
    }
    
    for q_id, rating in answers.items():
        q_id = int(q_id.replace('q', ''))
        question = next(q for q in INTEREST_QUESTIONS if q["id"] == q_id)
        categories[question["category"]] += int(rating)
    
    sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
    top_categories = sorted_categories[:3]
    
    career_recommendations = get_career_recommendations(top_categories)
    
    session['interest_results'] = {
        'categories': sorted_categories,
        'recommendations': career_recommendations
    }
    
    return render_template('interest_results.html', 
                         categories=sorted_categories,
                         recommendations=career_recommendations)

def get_career_recommendations(top_categories):
    career_paths = {
        "Technical": ["Software Engineer", "Network Administrator", "Quality Control Specialist"],
        "Medical": ["Doctor", "Nurse", "Medical Researcher"],
        "Arts": ["Graphic Designer", "Music Teacher", "Theater Director"],
        "Social": ["Counselor", "Social Worker", "HR Manager"],
        "Business": ["Sales Manager", "Business Consultant", "Entrepreneur"],
        "Administrative": ["Office Manager", "Executive Assistant", "Project Coordinator"],
        "Scientific": ["Research Scientist", "Laboratory Technician", "Data Analyst"]
    }
    
    recommendations = []
    for category, score in top_categories:
        for career in career_paths[category]:
            recommendations.append({
                "career": career,
                "link": f"/careers/{career.replace(' ', '-').lower()}"
            })
    return recommendations[:5]  # Return top 5 recommendations

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)