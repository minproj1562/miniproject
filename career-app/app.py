from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import json
from questions import APTITUDE_QUESTIONS, PERSONALITY_QUESTIONS, CAREER_MAPPING

app = Flask(__name__)
app.config.update(
    SECRET_KEY='your_secret_key',
    SQLALCHEMY_DATABASE_URI='sqlite:///career.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    assessments = db.Column(db.JSON)

# Authentication routes (similar to previous implementation)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', 
                         aptitude_progress=user.assessments.get('aptitude_progress', 0),
                         personality_progress=user.assessments.get('personality_progress', 0))

@app.route('/aptitude-test')
def aptitude_test():
    return render_template('aptitude.html', questions=APTITUDE_QUESTIONS)

@app.route('/personality-test')
def personality_test():
    return render_template('personality.html', questions=PERSONALITY_QUESTIONS)

@app.route('/submit-assessment', methods=['POST'])
def submit_assessment():
    data = request.get_json()
    assessment_type = data['type']
    
    # Calculate scores
    scores = calculate_scores(data['responses'], assessment_type)
    
    # Update user progress
    user = User.query.get(session['user_id'])
    user.assessments = user.assessments or {}
    user.assessments[f'{assessment_type}_scores'] = scores
    user.assessments[f'{assessment_type}_progress'] = 100
    db.session.commit()
    
    return jsonify({
        'redirect': url_for('results'),
        'scores': scores
    })

def calculate_scores(responses, assessment_type):
    if assessment_type == 'aptitude':
        # Cognitive ability scoring
        scores = {'total': 0, 'categories': {}}
        for q_id, response in responses.items():
            question = next(q for q in APTITUDE_QUESTIONS if q['id'] == q_id)
            category = question['category']
            scores['categories'][category] = scores['categories'].get(category, 0) + response * question['weight']
            scores['total'] += response * question['weight']
        return scores
    
    elif assessment_type == 'personality':
        # Big Five personality scoring
        traits = {'O':0, 'C':0, 'E':0, 'A':0, 'N':0}
        for q_id, response in responses.items():
            question = next(q for q in PERSONALITY_QUESTIONS if q['id'] == q_id)
            traits[question['trait']] += response * (1 if question['direction'] else -1)
        return {t: (score/10)*100 for t, score in traits.items()}

@app.route('/results')
def results():
    user = User.query.get(session['user_id'])
    return render_template('results.html',
                         aptitude=user.assessments.get('aptitude_scores'),
                         personality=user.assessments.get('personality_scores'),
                         careers=CAREER_MAPPING)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)