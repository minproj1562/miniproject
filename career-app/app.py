from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
import os
import json

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY', 'dev_secret_key'),
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', 'sqlite:///site.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

# Initialize extensions
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    assessments_completed = db.Column(db.Integer, default=0)

APTITUDE_QUESTIONS = [
    {"id": 1, "subject": "Mathematics", "question": "How comfortable are you solving complex algebraic equations?"},
    {"id": 2, "subject": "Science", "question": "How interested are you in analyzing chemical reactions?"},
    {"id": 3, "subject": "Logic", "question": "How easily can you identify patterns in logical sequences?"},
]

CAREER_MAPPINGS = {
    "Engineering": {"subjects": ["Mathematics", "Physics"], "score_range": [15, 25]},
    "Data Science": {"subjects": ["Mathematics", "Logic"], "score_range": [12, 22]},
    "Research Scientist": {"subjects": ["Science", "Mathematics"], "score_range": [14, 24]},
}

@app.route('/')
def home():
    return render_template('base.html')

# (Other authentication routes and helpers would go here)

@app.route('/aptitude-test')
def aptitude_test():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('aptitude.html', questions=APTITUDE_QUESTIONS)

@app.route('/submit-aptitude', methods=['POST'])
def submit_aptitude():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        responses = {k: v for k, v in request.form.items() if k.startswith('q')}
        time_data = json.loads(request.form.get('time_data', '{}'))
        
        scores = {"Total": 0}
        for q in APTITUDE_QUESTIONS:
            qid = str(q['id'])
            response = int(responses.get(f'q{qid}', 0))
            time_spent = time_data.get(qid, 180)
            time_weight = 1 - (time_spent / 180)
            subject = q['subject']
            
            scores[subject] = scores.get(subject, 0) + response * time_weight
            scores["Total"] += response * time_weight
        
        session['aptitude_scores'] = scores
        return redirect(url_for('results'))
    except Exception as e:
        app.logger.error(f"Aptitude test error: {e}")
        flash('Error processing your results. Please try again.', 'danger')
        return redirect(url_for('aptitude_test'))

@app.route('/results')
def results():
    scores = session.get('aptitude_scores')
    if not scores or 'user_id' not in session:
        return redirect(url_for('aptitude_test'))
    
    career = "General Professional"
    for career_name, data in CAREER_MAPPINGS.items():
        if data['score_range'][0] <= scores['Total'] <= data['score_range'][1]:
            career = career_name
            break
    
    user = User.query.get(session['user_id'])
    if user.assessments_completed < 1:
        user.assessments_completed += 1
        db.session.commit()
    
    return render_template('results.html', career=career, scores=scores)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
