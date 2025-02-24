# app.py (Flask Backend)
from flask import Flask, render_template, request, session, redirect, url_for
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

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

@app.route('/')
def index():
    return render_template('career_tests.html')

@app.route('/aptitude-test')
def aptitude_test():
    session.clear()
    return render_template('aptitude_test.html')

@app.route('/submit-aptitude', methods=['POST'])
def submit_aptitude():
    responses = request.form.to_dict()
    time_data = json.loads(request.form.get('time_data'))
    
    # Calculate scores
    scores = {"Mathematics": 0, "Science": 0, "Total": 0}
    for q in APTITUDE_QUESTIONS:
        subject = q['subject']
        response = int(responses.get(f'q{q['id']}', 0))
        time_weight = 1 - (time_data[str(q['id'])] / 180)  # 3min max per question
        scores[subject] += response * time_weight
        
    session['aptitude_scores'] = scores
    return redirect(url_for('results'))

@app.route('/results')
def results():
    aptitude = session.get('aptitude_scores')
    personality = session.get('personality_scores')  # For future integration
    
    # Determine career
    career = calculate_career(aptitude, personality)
    return render_template('results.html', career=career)

def calculate_career(aptitude, personality):
    # Implement your career logic here
    for career, data in CAREER_MAPPINGS.items():
        if data['score_range'][0] <= aptitude['Total'] <= data['score_range'][1]:
            return career
    return "General Professional"

if __name__ == '_main_':
    app.run(debug=True)