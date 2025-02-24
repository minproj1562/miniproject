from flask import Flask, render_template, request, session, redirect, url_for,flash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Required for flashing messages
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# Questions for the aptitude test
QUESTIONS = [
    {
        "id": 1,
        "question": "You notice a coworker taking office supplies home. What would you do?",
        "options": [
            "Ignore it as it's not my business",
            "Report it to the supervisor immediately",
            "Talk to the coworker first to understand their situation",
            "Document the incident but wait to see if it happens again"
        ],
        "weights": [1, 3, 4, 2]
    },
    {
        "id": 2,
        "question": "Your project deadline is tomorrow, but you've discovered a minor flaw. What action do you take?",
        "options": [
            "Submit as is since it's minor",
            "Work overtime to fix it",
            "Communicate with stakeholders about the issue and propose a solution",
            "Ask for a deadline extension"
        ],
        "weights": [1, 3, 4, 2]
    },
    {
        "id": 3,
        "question": "A client offers you a personal gift for your services. How do you handle it?",
        "options": [
            "Accept it to maintain good relations",
            "Politely decline and explain company policy",
            "Accept and report it to management",
            "Suggest donating it to charity instead"
        ],
        "weights": [1, 4, 2, 3]
    },
    {
        "id": 4,
        "question": "You discover a way to increase efficiency but it might make a colleague's role redundant. What do you do?",
        "options": [
            "Keep the discovery to yourself",
            "Share it with management without consulting the colleague",
            "Discuss with the colleague first and work on a plan together",
            "Share it but propose ways to reassign the colleague"
        ],
        "weights": [1, 2, 4, 3]
    },
    {
        "id": 5,
        "question": "Your team member takes credit for your work during a presentation. How do you respond?",
        "options": [
            "Confront them publicly during the presentation",
            "Stay silent to avoid conflict",
            "Schedule a private discussion to address the issue",
            "Immediately correct them in front of everyone"
        ],
        "weights": [1, 2, 4, 1]
    },
    {
        "id": 6,
        "question": "You are assigned to work with a difficult colleague. How do you handle it?",
        "options": [
            "Avoid them and do your work independently",
            "Try to understand their perspective and communicate openly",
            "Report their behavior to HR immediately",
            "Get others involved to mediate the situation"
        ],
        "weights": [1, 4, 2, 3]
    },
    {
        "id": 7,
        "question": "You make a mistake at work that affects the team's progress. What do you do?",
        "options": [
            "Ignore it and hope no one notices",
            "Blame the situation or others to avoid taking responsibility",
            "Own up to the mistake, apologize, and propose a solution",
            "Try to cover up the mistake and fix it secretly"
        ],
        "weights": [1, 2, 4, 3]
    },
    {
        "id": 8,
        "question": "Your supervisor asks you to complete an urgent task, but you already have a full schedule. How do you respond?",
        "options": [
            "Turn down the task and stick to your current schedule",
            "Ask for help to get your current tasks done while taking on the new one",
            "Prioritize the urgent task and delay your other tasks",
            "Communicate openly with your supervisor about your workload and ask for guidance"
        ],
        "weights": [1, 4, 3, 2]
    },
    {
        "id": 9,
        "question": "How do you handle a situation when your manager gives you critical feedback?",
        "options": [
            "Get defensive and explain why the mistake happened",
            "Listen carefully, accept the feedback, and work to improve",
            "Ignore the feedback and continue doing things your way",
            "Feel demotivated and let the feedback affect your performance"
        ],
        "weights": [1, 4, 2, 3]
    },
    {
        "id": 10,
        "question": "You are given a challenging task that you don’t know how to complete. What do you do?",
        "options": [
            "Avoid asking for help and try to figure it out on your own",
            "Look for resources or ask a colleague for guidance",
            "Tell your supervisor you don’t know how to do it",
            "Give up and request to be reassigned to another task"
        ],
        "weights": [1, 4, 2, 3]
    },
    {
        "id": 11,
        "question": "You discover that your colleague has been spreading rumors about you. How do you handle the situation?",
        "options": [
            "Confront them publicly in front of the team",
            "Talk to the colleague privately and clarify any misunderstandings",
            "Ignore the rumors and focus on your work",
            "Report the issue to HR immediately"
        ],
        "weights": [1, 4, 3, 2]
    },
    {
        "id": 12,
        "question": "How would you handle a situation where you are overworked and on the verge of burnout?",
        "options": [
            "Push through the exhaustion and keep working",
            "Talk to your supervisor about adjusting your workload",
            "Take a day off and hope that you can catch up later",
            "Work overtime to make up for the lost time"
        ],
        "weights": [1, 4, 3, 2]
    },
    {
        "id": 13,
        "question": "Your coworker consistently arrives late to work, causing delays in the team. What would you do?",
        "options": [
            "Ignore the behavior and hope it gets better",
            "Talk to your coworker privately and offer help",
            "Report them to your manager",
            "Talk to the team to discuss how to handle the situation"
        ],
        "weights": [1, 4, 2, 3]
    },
    {
        "id": 14,
        "question": "You have conflicting priorities, and you are unable to complete everything on time. What do you do?",
        "options": [
            "Focus on the easiest tasks first",
            "Communicate with stakeholders and adjust expectations",
            "Complete the most urgent tasks first, ignoring the others",
            "Work overtime to complete all tasks on time"
        ],
        "weights": [1, 4, 3, 2]
    },
    {
        "id": 15,
        "question": "A team member asks for help on a task you already finished. How do you respond?",
        "options": [
            "Ignore the request and move on to your next task",
            "Help them out, even if it takes extra time",
            "Tell them to figure it out on their own",
            "Passively assist them without much involvement"
        ],
        "weights": [1, 4, 2, 3]
    },
    {
        "id": 16,
        "question": "You are given a task you do not fully understand. What do you do?",
        "options": [
            "Attempt to figure it out alone, even if it takes a long time",
            "Ask for clarification from a colleague or supervisor",
            "Request more training before attempting the task",
            "Decline the task and suggest someone else take it on"
        ],
        "weights": [1, 4, 3, 2]
    },
    {
        "id": 17,
        "question": "You notice that a colleague is being treated unfairly in the workplace. How do you respond?",
        "options": [
            "Ignore it, as it’s not my problem",
            "Support the colleague and report the issue to HR",
            "Stay neutral and don’t get involved",
            "Talk to the colleague to understand their perspective and suggest a solution"
        ],
        "weights": [1, 4, 2, 3]
    },
    {
        "id": 18,
        "question": "How do you handle working with a team where there is a lack of communication?",
        "options": [
            "Ignore the issue and keep working",
            "Communicate openly with the team and propose regular check-ins",
            "Report the issue to the manager immediately",
            "Try to take over and lead the team on your own"
        ],
        "weights": [1, 4, 3, 2]
    },
    {
        "id": 19,
        "question": "You are asked to perform a task that you believe goes against your personal values. How do you handle it?",
        "options": [
            "Refuse to do the task and explain why",
            "Complete the task reluctantly without question",
            "Find a way to compromise and complete the task",
            "Ignore your values for the sake of the team"
        ],
        "weights": [1, 4, 3, 2]
    },
    {
        "id": 20,
        "question": "You are asked to mentor a new team member. How do you approach the task?",
        "options": [
            "Provide only basic guidance and let them figure things out on their own",
            "Offer detailed instructions and follow up frequently",
            "Give them minimal instructions and let them shadow you",
            "Teach them everything you know, even if they don’t ask"
        ],
        "weights": [1, 4, 3, 2]
    }
]

def calculate_score(answers):
    """Calculate the final score and provide an assessment."""
    total_points = 0
    max_possible = 0
    
    for q_id, answer_idx in answers.items():
        q_id = int(q_id)
        question = next(q for q in QUESTIONS if q["id"] == q_id)
        total_points += question["weights"][int(answer_idx)]
        max_possible += max(question["weights"])
    
    percentage = (total_points / max_possible) * 100
    
    if percentage >= 85:
        assessment = "Excellent work ethics! You demonstrate strong integrity and professional judgment."
    elif percentage >= 70:
        assessment = "Good work ethics. You generally make sound ethical decisions but there's room for improvement."
    elif percentage >= 50:
        assessment = "Fair work ethics. Consider reviewing professional ethics guidelines and workplace policies."
    else:
        assessment = "Needs improvement. It's recommended to study workplace ethics and consult with HR or supervisors."
    
    return {
        "score": round(percentage, 1),
        "assessment": assessment
    }

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

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Get data from the form
        username = request.form["username"]
        email = request.form["email"]
        mobile_number = request.form["mobile_number"]
        pin_code = request.form["pin_code"]
        dob = request.form["dob"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Ensure password and confirm password match
        if password != confirm_password:
            flash('Password and Confirm Password do not match!', 'danger')
            return redirect(url_for('register'))

        # Ensure the username is unique
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))

        # Ensure the email is unique
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already registered. Please use a different one.', 'danger')
            return redirect(url_for('register'))

        # Create a new user
        new_user = User(
            username=username,
            email=email,
            mobile_number=mobile_number,
            pin_code=pin_code,
            dob=dob,
            password=password
        )

        # Add user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Query the database to check if the user exists
        user = User.query.filter_by(username=username).first()

        # Check if user exists and if password matches
        if user and user.password == password:
            flash('Login successful!', 'success')
            return redirect(url_for('success'))
        else:
            flash('Login failed. Check your username and password.', 'danger')

    return render_template("login.html")


@app.route("/success")
def success():
    return render_template('personal.html')



@app.route('/')
@app.route('/home')
def home():
    session.clear()
    return render_template('index.html')


@app.route('/student')
def student():
    return render_template('std.html')

@app.route('/degree')
def degree():
    return render_template('degree.html')

@app.route('/career')
def career():
    return render_template('career.html')

@app.route('/online')
def online():
    return render_template('online.html')

@app.route('/software_engg')
def software():
    return render_template('software_engg.html')

@app.route('/brand')
def brand():
    return render_template('brand.html')

@app.route('/yourself')
def yourself():
    return render_template('yourself.html')


@app.route('/interview')
def interview():
    return render_template('interview.html')

@app.route('/introvert')
def introvert():
    return render_template('introvert.html')

@app.route('/test')
def test():
    return render_template('test.html', questions=QUESTIONS)

@app.route('/submit', methods=['POST'])
def submit():
    answers = request.form.to_dict()
    results = calculate_score(answers)
    return render_template('results.html', results=results)

# Add to your existing app.py
INTEREST_QUESTIONS = [
    {
        "id": 1,
        "activity": "Test the quality of parts before shipment",
        "category": "Technical"
    },
    {
        "id": 2,
        "activity": "Study the structure of the human body",
        "category": "Medical"
    },
    {
        "id": 3,
        "activity": "Conduct a musical choir",
        "category": "Arts"
    },
    {
        "id": 4,
        "activity": "Give career guidance to people",
        "category": "Social"
    },
    {
        "id": 5,
        "activity": "Sell restaurant franchises to individuals",
        "category": "Business"
    },
    {
        "id": 6,
        "activity": "Generate the monthly payroll checks for an office",
        "category": "Administrative"
    },
    {
        "id": 7,
        "activity": "I enjoy developing long-term stratergies and plans",
        "category": "Technical"
    },
    {
        "id": 8,
        "activity": "Study animal behavior",
        "category": "Scientific"
    },
    {
        "id": 9,
        "activity": "Direct a play",
        "category": "Arts"
    },
    {
        "id": 10,
        "activity": "Do volunteer work at a non-profit organization",
        "category": "Social"
    },
    {
        "id": 11,
        "activity": "Sell merchandise at a department store",
        "category": "Business"
    }
]

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
    
    career_pages = {
        "Software Engineer": "/careers/software-engineer",
        "Network Administrator": "/careers/network-administrator",
        "Quality Control Specialist": "/careers/quality-control-specialist",
        "Doctor": "/careers/doctor",
        "Nurse": "/careers/nurse",
        "Medical Researcher": "/careers/medical-researcher",
        "Graphic Designer": "/careers/graphic-designer",
        "Music Teacher": "/careers/music-teacher",
        "Theater Director": "/careers/theater-director",
        "Counselor": "/careers/counselor",
        "Social Worker": "/careers/social-worker",
        "HR Manager": "/careers/hr-manager",
        "Sales Manager": "/careers/sales-manager",
        "Business Consultant": "/careers/business-consultant",
        "Entrepreneur": "/careers/entrepreneur",
        "Office Manager": "/careers/office-manager",
        "Executive Assistant": "/careers/executive-assistant",
        "Project Coordinator": "/careers/project-coordinator",
        "Research Scientist": "/careers/research-scientist",
        "Laboratory Technician": "/careers/laboratory-technician",
        "Data Analyst": "/careers/data-analyst"
    }
    recommendations = []
    for category, score in top_categories:
        for career in career_paths[category]:
            recommendations.append({
                "career": career,
                "link": career_pages.get(career, "#")  # Default to "#" if no link is found
            })
    return recommendations[:5]  # Return top 5 recommendations

@app.route('/interest_test')
def interest_test():
    return render_template('interest_test.html', questions=INTEREST_QUESTIONS)

@app.route('/submit_interests', methods=['POST'])
def submit_interests():
    answers = request.form.to_dict()
    
    # Calculate category scores
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
    
    # Find top categories
    sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
    top_categories = sorted_categories[:3]
    
    # Get career recommendations
    career_recommendations = get_career_recommendations(top_categories)
    
    # Store results in session
    session['interest_results'] = {
        'categories': sorted_categories,
        'recommendations': career_recommendations
    }
    
    return render_template('interest_results.html', 
                         categories=sorted_categories,
                         recommendations=career_recommendations)


if __name__ == '__main__':
    app.run(debug=True)