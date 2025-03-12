from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from data import aptitude_questions, personality_questions, careers
import numpy as np
import json

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    assessments = db.relationship('Assessment', backref='user', lazy=True)

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    results = db.Column(db.JSON)
    timestamp = db.Column(db.DateTime, default=db.func.now())

# Helper Functions
def calculate_aptitude_score(responses):
    scores = {cat: 0 for cat in aptitude_questions.CATEGORIES}
    for response in responses:
        question = next(q for q in aptitude_questions.QUESTIONS if q['id'] == response['question_id'])
        time_ratio = min(response['time'] / question['time_limit'], 1)
        time_weight = 1 - time_ratio
        score = response['correct'] * question['difficulty'] * time_weight
        scores[question['category']] += score
    max_scores = {cat: sum(q['difficulty'] for q in aptitude_questions.QUESTIONS if q['category'] == cat) for cat in scores}
    return {cat: (scores[cat] / max_scores[cat]) * 100 for cat in scores}

def calculate_personality_profile(responses):
    traits = {t: {'total': 0, 'count': 0} for t in personality_questions.CATEGORIES}
    for q_id, response in responses.items():
        question = next(q for q in personality_questions.QUESTIONS if q['id'] == int(q_id))
        for trait, value in response.items():
            traits[trait]['total'] += value
            traits[trait]['count'] += 1
    return {trait: (data['total'] / (data['count'] or 1)) * 25 for trait, data in traits.items()}

# Routes
@app.route('/assessments/aptitude', methods=['POST'])
def submit_aptitude():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        responses = request.get_json()
        scores = calculate_aptitude_score(responses)
        
        assessment = Assessment(
            user_id=session['user_id'],
            type='aptitude',
            results=scores
        )
        db.session.add(assessment)
        db.session.commit()
        
        return jsonify({'redirect': url_for('personality_test')}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/assessments/personality', methods=['POST'])
def submit_personality():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        responses = request.get_json()
        profile = calculate_personality_profile(responses)
        
        assessment = Assessment(
            user_id=session['user_id'],
            type='personality',
            results=profile
        )
        db.session.add(assessment)
        db.session.commit()
        
        return jsonify({'redirect': url_for('results')}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/results')
def results():
    # Comb