from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import json
from questions import APTITUDE_QUESTIONS, PERSONALITY_QUESTIONS, CAREER_MAPPING
import math

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
    api_data = db.Column(db.JSON)  # Store API responses
    last_updated = db.Column(db.DateTime)

# Authentication routes (similar to previous implementation)
ADAPTIVE_TEST_SETTINGS = {
    "scaling_factors": {
        "correct_answer": 1.0,
        "wrong_answer": -0.5,
        "time_penalty": 0.2
    }
}
# Add to top
from apis import APIService, ONetAPI, PlagiarismChecker

# Add to config
app.config.update(
    LINKEDIN_API_KEY=os.getenv('LINKEDIN_KEY'),
    ONET_CREDENTIALS=(os.getenv('ONET_USER'), os.getenv('ONET_PWD')),
    COPYLEAKS_KEY=os.getenv('COPYLEAKS_KEY')
)

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
    user = User.query.get(session['user_id'])
    
    if data['type'] == 'personality':
        scores = calculate_personality(data['responses'])
    else:
        scores = calculate_aptitude(data['responses'])
    
    # Store results
    user.assessments[f"{data['type']}_scores"] = scores
    user.assessments[f"{data['type']}_progress"] = 100
    db.session.commit()
    
    return jsonify({'redirect': url_for('results')})
def calculate_personality(results):
    """Calculate Big Five scores using validated scoring protocol"""
    traits = {'O': [], 'C': [], 'E': [], 'A': [], 'N': []}
    
    for question, response in results.items():
        q = next(q for q in PERSONALITY_QUESTIONS if q['id'] == question['id'])
        score = response if q['direction'] else 4 - response  # Reverse coding
        traits[q['trait']].append(score)
    
    # Convert to percentile scores
    return {trait: (sum(scores)/len(scores)*20) for trait, scores in traits.items()}
def get_question(question_id):
    for domain, levels in APTITUDE_QUESTIONS.items():
        for difficulty_level, question_list in levels.items():
            for question in question_list:
                if question["id"] == question_id:
                    return {
                        "id": question["id"],
                        "discrimination": question["irt_params"]["discrimination"],
                        "difficulty": question["irt_params"]["difficulty"],
                        "time_limit": question["time_limit"]
                    }
    return None

def calculate_aptitude(responses):
    """IRT-based ability estimation using Bayesian updating"""
    ability = 0
    for response in responses:
        question = get_question(response['id'])
        # Use 2PL IRT model
        p = 1/(1 + math.exp(-question['discrimination'] * (ability - question['difficulty'])))
        ability += math.log(p/(1-p)) * ADAPTIVE_TEST_SETTINGS['scaling_factors']['correct_answer']
    return ability
def calculate_score(responses):
    ability_estimate = 0
    for response in responses:
        question = get_question(response.id)
        p_correct = 1 / (1 + math.exp(-question.discrimination * 
                        (ability_estimate - question.difficulty)))
        ability_estimate += ADAPTIVE_TEST_SETTINGS["scaling_factors"]["correct_answer"] \
                            if response.correct else \
                            ADAPTIVE_TEST_SETTINGS["scaling_factors"]["wrong_answer"]
        # Adjust for time penalty
        ability_estimate -= (max(0, response.time_taken - question.time_limit) / 
                           question.time_limit * 0.1) * \
                           ADAPTIVE_TEST_SETTINGS["scaling_factors"]["time_penalty"]
    return ability_estimate

@app.route('/results')
def results():
    user = User.query.get(session['user_id'])
    return render_template('results.html',
                         aptitude=user.assessments.get('aptitude_scores'),
                         personality=user.assessments.get('personality_scores'),
                         careers=CAREER_MAPPING)
@app.route('/api/careers/<soc_code>')
def career_details(soc_code):
    return jsonify(ONetAPI().get_career_details(soc_code))

@app.route('/api/job-market/<title>')
def job_market(title):
    return jsonify(APIService.get_linkedin_jobs(title))

@app.route('/api/verify-answers', methods=['POST'])
def verify_answers():
    responses = request.json.get('answers')
    scores = [PlagiarismChecker.verify_content(r) for r in responses]
    return jsonify({"originality_scores": scores})
@app.route('/login')
def login():
    return render_template('login.html')
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)