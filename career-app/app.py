import os
import sys
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, Blueprint, send_from_directory, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_wtf import FlaskForm
from wtforms import BooleanField, HiddenField, SubmitField  # Import WTForms fields
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_session import Session
from datetime import datetime
from collections import defaultdict
from flask_caching import Cache
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo
import logging
import random
import copy
import json
from PIL import Image
from datetime import datetime, timezone
import numpy as np
import pdfkit
from pathlib import Path 
import requests
# Import question data
from questions import (
    APTITUDE_QUESTIONS, PERSONALITY_QUESTIONS, SCORING_WEIGHTS,
    CAREER_MAPPING, SKILL_GAP_QUESTIONS, LEARNING_RESOURCES, ADAPTIVE_TEST_SETTINGS
)
from forms import ProfileForm, LoginForm, RegisterForm, ContactForm
from jinja2 import Environment

app = Flask(__name__,static_url_path='/static', static_folder='static')
# Configure Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'  # Store session data on the server’s filesystem
app.config['SESSION_FILE_DIR'] = os.path.join(app.instance_path, 'sessions')  # Directory for session files
app.config['SESSION_PERMANENT'] = False  # Sessions expire when the browser closes
app.config['SESSION_USE_SIGNER'] = True  # Sign session cookies for security
app.config['SESSION_KEY_PREFIX'] = 'session:'  # Prefix for session keys
# Initialize Flask-Session
Session(app)
def zfill_filter(value, width=2):
    return str(value).zfill(width)

app.jinja_env.filters['zfill'] = zfill_filter
app.config['SECRET_KEY'] = '033dc7a2f8382c4dd7bd18a473e24db20b088146eb846900'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///career_analytics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'abc@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password-here'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
app.config['WTF_CSRF_HEADERS'] = ['X-CSRF-Token']
app.config['PDFKIT_CONFIG'] = {
    'wkhtmltopdf': 'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'  
}
app.config['HTML2PDF_API_KEY'] = 'L5zgjIt6LMDfgCdiz5AziCtzkyvbRoiDjtwfYwa67ZqTtCJMV6hHp98QsqZyzLeC'
mail = Mail(app)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
test_bp = Blueprint('test', __name__)

def format_number(value):
    try:
        return "{:,.0f}".format(float(value))
    except (ValueError, TypeError):
        return value

app.jinja_env.filters['format_number'] = format_number

def select_next_question(user_id, current_theta):
    questions = session.get('aptitude_questions', [])
    user_responses = session.get('aptitude_responses', [])
    if not questions:
        return None  # No questions available

    # Calculate difficulty based on theta
    difficulty_thresholds = {'easy': -1.0, 'medium': 0.0, 'hard': 1.0}
    difficulty = 'easy'
    if current_theta > difficulty_thresholds['hard']:
        difficulty = 'hard'
    elif current_theta > difficulty_thresholds['medium']:
        difficulty = 'medium'

    # Filter unattempted questions by difficulty
    attempted_ids = [r['question_id'] for r in user_responses]
    available_questions = [q for q in questions if q['id'] not in attempted_ids and q.get('difficulty', 'medium') == difficulty]

    # Fallback to other difficulties if no questions are available
    if not available_questions:
        for diff in ['medium', 'hard', 'easy']:
            if diff != difficulty:
                available_questions = [q for q in questions if q['id'] not in attempted_ids and q.get('difficulty', 'medium') == diff]
                if available_questions:
                    break

    return random.choice(available_questions) if available_questions else None

def cosine_similarity(a, b):
    a = np.array(a, dtype=float).flatten()  # Ensure 1D and numeric
    b = np.array(b, dtype=float).flatten()
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)

# Models
class CareerMatchForm(FlaskForm):
    global_opportunities = BooleanField('Show Global Opportunities')
    region = HiddenField()
    submit = SubmitField('Update')
    
# models.py (add Resume model)
class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    resume_data = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=True)
    animations_enabled = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    # New fields for settings
    theme = db.Column(db.String(10), default='light', nullable=False)  # For theme preference
    notify_test_reminders = db.Column(db.Boolean, default=True, nullable=False)  # Notification preferences
    notify_badge_earned = db.Column(db.Boolean, default=True, nullable=False)
    notify_progress_updates = db.Column(db.Boolean, default=True, nullable=False)
    email_notifications = db.Column(db.Boolean, default=True, nullable=False)  # Email preferences
    email_newsletters = db.Column(db.Boolean, default=False, nullable=False)
    profile_visibility = db.Column(db.String(10), default='public', nullable=False)  # Profile visibility
    preferred_test_categories = db.Column(db.JSON, default=lambda: [], nullable=False) 
    mobile_number = db.Column(db.String(20), nullable=True)# Preferred test categories
    pin_code = db.Column(db.String(10), nullable=True)
    dob = db.Column(db.Date, nullable=True)
    bio= db.Column(db.Text,        nullable=True)
    # Existing relationships
    tests = db.relationship('TestResult', backref='user', lazy=True)
    badges = db.relationship('Badge', backref='user', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)
    aptitude_scores = db.Column(db.JSON, default="{}", nullable=False)  # Changed to string default
    personality_scores = db.Column(db.JSON, default="{}", nullable=False)  # Changed to string default
    skill_gap_scores = db.Column(db.JSON, default="{}", nullable=False)  # Added field with default
    skill_gap_completed_at = db.Column(db.DateTime)
    top_careers = db.Column(db.Text)  # Add this line
    resumes = db.relationship('Resume', backref='user', lazy=True)

class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    test_type = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Float, nullable=False)
    time_spent = db.Column(db.Integer, nullable=True)
    details = db.Column(db.Text, nullable=True)
    completed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    icon = db.Column(db.String(50), nullable=False)
    date_earned = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
with app.app_context():
    db.create_all()

def convert_salary(salary, region, currency):
    if region == 'IN' and currency == 'USD':
        try:
            response = requests.get('https://api.exchangerate-api.com/v4/latest/USD', timeout=5)
            rate = response.json()['rates']['INR']
            return salary * rate
        except Exception as e:
            logger.error(f"Currency conversion failed: {e}")
            return salary * 83  # Fallback rate
    return salary


def calculate_career_match(user_scores, career_data, completed_tests):
    """
    Calculate career match score based on available test results (aptitude, personality, or both).
    
    Args:
        user_scores (dict): Dictionary containing 'aptitude' and/or 'personality' scores.
        career_data (dict): Career data from CAREER_MAPPING.
        completed_tests (list): List of completed test types ('aptitude', 'personality', 'skill_gap').
    
    Returns:
        dict: Match score, fit reasons, and fit level.
    """
    total_score = 0
    max_score = 0
    fit_reasons = []
    
    # Dynamically adjust weights based on completed tests
    weights = {
        'aptitude': 1.0 if 'aptitude' in completed_tests else 0.0,
        'personality': 1.0 if 'personality' in completed_tests else 0.0,
        'skill_gap': 0.0  # Keep skill_gap optional for now
    }
    total_weight = sum(w for w in weights.values() if w > 0)

    # 1. Trait Alignment (Personality)
    if 'personality' in completed_tests and user_scores.get('personality'):
        personality_user = user_scores['personality']
        personality_career = career_data['personality']
        for trait in personality_career:
            if trait in personality_user:
                max_score += 100
                diff = abs(personality_user[trait] - personality_career[trait])
                trait_score = max(0, 100 - diff)  # Inverse difference as score
                total_score += trait_score * (weights['personality'] / total_weight)
                if personality_user[trait] >= personality_career[trait] * 0.8 and personality_career[trait] > 50:
                    fit_reasons.append(f"High {trait} personality ({personality_user[trait]}%)")
                elif personality_user[trait] <= personality_career[trait] * 1.2 and personality_career[trait] < 50:
                    fit_reasons.append(f"Low {trait} personality ({personality_user[trait]}%)")

    # 2. Competency Match (Aptitude)
    if 'aptitude' in completed_tests and user_scores.get('aptitude'):
        aptitude_user = user_scores['aptitude']
        aptitude_career = career_data['aptitude']
        for category in aptitude_career:
            if category in aptitude_user:
                max_score += 100
                match_percentage = min(aptitude_user[category] / aptitude_career[category], 1.0) * 100
                total_score += match_percentage * (weights['aptitude'] / total_weight)
                if aptitude_user[category] >= aptitude_career[category] * 0.8:
                    fit_reasons.append(f"High {category} aptitude ({aptitude_user[category]}%)")

    # 3. Skill Proximity (Skill Gap) - Optional
    if 'skill_gap' in completed_tests and user_scores.get('skill_gap'):
        user_skill = user_scores['skill_gap'].get('score', 0)
        required_skill = career_data['skills']['required']
        max_score += 100
        skill_score = min(user_skill / required_skill, 1.0) * 100
        total_score += skill_score * (weights['skill_gap'] / total_weight)
        if user_skill >= required_skill * 0.8:
            fit_reasons.append(f"Strong skill proficiency ({user_skill}%)")

    # Normalize score and determine fit level
    overall_score = (total_score / max_score * 100) if max_score > 0 else 0
    if overall_score >= 75:
        fit_level = "Highly Suitable"
    elif overall_score >= 50:
        fit_level = "Moderately Suitable"
    else:
        fit_level = "Not Assessed"
        if not fit_reasons:
            fit_reasons = ["Limited data. Complete more tests (e.g., both Aptitude and Personality) for a better assessment"]

    return {
        "fit_level": fit_level,
        "score": overall_score,
        "reasons": fit_reasons
    }

@app.before_request
def init_session():
    if 'used_aptitude' not in session:
        session['used_aptitude'] = []
    if 'aptitude_history' not in session:
        session['aptitude_history'] = defaultdict(list)
        
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

class ONetAPI:
    def __init__(self):
        self.base_url = "https://services.onetcenter.org/v1.9/ws/online/"
        self.auth = ("career_analysis_app", "7284kqu")  # Your credentials

    def get_occupation_summary(self, soc_code):
        url = f"{self.base_url}occupations/{soc_code}/summary"
        try:
            response = requests.get(url, auth=self.auth, timeout=10)
            logger.debug(f"Fetching summary for SOC {soc_code}. Status: {response.status_code}, Response: {response.text[:1000]}")
        
            if response.status_code == 200:
                try:
                    root = ET.fromstring(response.content)
                    # Extract title
                    title = root.find(".//title").text if root.find(".//title") is not None else soc_code
                    
                    # Extract description
                    description = root.find(".//description").text if root.find(".//description") is not None else "No description available"
                    
                    # Extract wage data
                    wages_elem = root.find(".//wages/national/annual/median")
                    median_wage = float(wages_elem.text) if wages_elem is not None and wages_elem.text else 100000
                    
                    # Extract outlook data (growth rate)
                    # O*NET might use different paths; try multiple possibilities
                    growth_rate_elem = root.find(".//outlook/projections/percent_change") or root.find(".//outlook/growth_rate")
                    growth_rate = float(growth_rate_elem.text) if growth_rate_elem is not None and growth_rate_elem.text else 0
                    
                    return {
                        "title": title,
                        "description": description,
                        "wages": {"median": median_wage},
                        "currency": "USD",
                        "outlook": {"growth_rate": growth_rate}
                    }
                except (ET.ParseError, ValueError, AttributeError) as e:
                    logger.error(f"Error parsing XML for {soc_code}: {e}, Response: {response.text}")
                    return {
                        "title": soc_code,
                        "description": "Error retrieving data",
                        "wages": {"median": 100000},
                        "currency": "USD",
                        "outlook": {"growth_rate": 0}
                    }
            else:
                logger.error(f"API request failed for {soc_code} with status {response.status_code}")
                return {
                    "title": soc_code,
                    "description": "Data unavailable",
                    "wages": {"median": 100000},
                    "currency": "USD",
                    "outlook": {"growth_rate": 0}
                }
        except requests.RequestException as e:
            logger.error(f"Request failed for {soc_code}: {e}")
            return {
                "title": soc_code,
                "description": "Connection error",
                "wages": {"median": 100000},
                "currency": "USD",
                "outlook": {"growth_rate": 0}
            }

    def get_abilities(self, soc_code):
        url = f"{self.base_url}occupations/{soc_code}/details/abilities"
        response = requests.get(url, auth=self.auth, timeout=10)
        logger.debug(f"Response status: {response.status_code}, Content: {response.text[:500]}...")
        if response.status_code == 200:
           root = ET.fromstring(response.content)
           abilities = []
           for elem in root.findall(".//element"):
              name = elem.find("name").text
              level = float(elem.find("score/[scale_id='LV']/value").text) if elem.find("score/[scale_id='LV']/value") else 50
              abilities.append({"name": name, "level": level})
           return abilities
        return []

    def get_work_styles(self, soc_code):
        url = f"{self.base_url}occupations/{soc_code}/details/work_styles"
        response = requests.get(url, auth=self.auth, timeout=10)
        logger.debug(f"Response status: {response.status_code}, Content: {response.text[:500]}...")
        if response.status_code == 200:
            try:
                root = ET.fromstring(response.content)
                work_styles = [
                    {"name": elem.find("name").text, "description": elem.find("description").text}
                    for elem in root.findall(".//element")
                    if elem.find("name") is not None and elem.find("description") is not None
                ]
                return work_styles if work_styles else []
            except ET.ParseError as e:
                logger.error(f"XML parse error for work_styles {soc_code}: {e}, Response: {response.text}")
                return []
        logger.warning(f"Work styles request failed with status {response.status_code} for {soc_code}")
        return []

    def get_skills(self, soc_code):
        url = f"{self.base_url}occupations/{soc_code}/details/skills"
        response = requests.get(url, auth=self.auth, timeout=10)
        logger.debug(f"Response status: {response.status_code}, Content: {response.text[:500]}...")
        if response.status_code == 200:
            try:
                root = ET.fromstring(response.content)
                skills = [
                    {"name": elem.find("name").text, "description": elem.find("description").text}
                    for elem in root.findall(".//element")
                    if elem.find("name") is not None and elem.find("description") is not None
                ]
                return skills if skills else []
            except ET.ParseError as e:
                logger.error(f"XML parse error for skills {soc_code}: {e}, Response: {response.text}")
                return []
        logger.warning(f"Skills request failed with status {response.status_code} for {soc_code}")
        return []

    def get_education(self, soc_code):
        url = f"{self.base_url}occupations/{soc_code}/details/education"
        response = requests.get(url, auth=self.auth, timeout=10)
        logger.debug(f"Response status: {response.status_code}, Content: {response.text[:500]}...")
        if response.status_code == 200:
            try:
                root = ET.fromstring(response.content)
                education = {
                    "level_required": [
                        {
                            "name": cat.find("name").text,
                            "score": int(cat.find("score").text) if cat.find("score") is not None else 0
                        }
                        for cat in root.findall(".//category")
                        if cat.find("name") is not None
                    ]
                }
                return education if education["level_required"] else {"level_required": []}
            except ET.ParseError as e:
                logger.error(f"XML parse error for education {soc_code}: {e}, Response: {response.text}")
                return {"level_required": []}
        logger.warning(f"Education request failed with status {response.status_code} for {soc_code}")
        return {"level_required": []}

# GeoPy for region mapping
from geopy.geocoders import Nominatim

def get_region_from_pin(pin_code):
    geolocator = Nominatim(user_agent="career_analytics")
    try:
        location = geolocator.geocode(pin_code, language='en')
        if location and 'India' in location.address:
            return 'IN'
        return 'US'
    except Exception:
        return 'US'  # Default to US if geolocation fails
 
# Mappings for aptitude and personality to O*NET
APTITUDE_TO_ONET = {
    "math": "Mathematical Reasoning",
    "logic": "Deductive Reasoning",
    "creativity": "Originality",
    "communication": "Oral Expression",
    "spatial": "Spatial Orientation",
    "analytical": "Information Ordering"
}

PERSONALITY_TO_ONET = {
    "Openness": "Innovation",
    "Conscientiousness": "Dependability",
    "Extraversion": "Leadership",
    "Agreeableness": "Cooperation",
    "Neuroticism": "Stress Tolerance"
}

# Career list with SOC codes
CAREERS = {
    "Software Developer": "15-1252.00",
    "Data Scientist": "15-2051.01",
    "Graphic Designer": "27-1024.00",
    "Financial Analyst": "13-2051.00",
    "Bank Manager": "11-3031.02",
    "Research Scientist": "19-1042.00",
    "Accountant": "13-2011.00",
    "Mathematician": "15-2021.00",
    "Marketing Manager": "11-2021.00"
}

class EdxAPI:
    def search_courses(self, subject=None, limit=5):
        # Mock course data for EdxAPI
        courses = [
            {"title": "Introduction to Computer Science", "university": "MITx", "duration": "Self-paced", "description": "Learn the basics of computer science.", "degree_level": "Beginner", "field_of_study": "Computer Science", "country": "USA"},
            {"title": "Data Science Fundamentals", "university": "HarvardX", "duration": "Self-paced", "description": "Introduction to data science concepts.", "degree_level": "Intermediate", "field_of_study": "Data Science", "country": "USA"},
            {"title": "Business Analytics", "university": "ColumbiaX", "duration": "Self-paced", "description": "Learn business analytics techniques.", "degree_level": "Intermediate", "field_of_study": "Business", "country": "USA"},
            {"title": "Graphic Design Basics", "university": "CalArts", "duration": "Self-paced", "description": "Introduction to graphic design principles.", "degree_level": "Beginner", "field_of_study": "Graphic Design", "country": "USA"},
            {"title": "Psychology 101", "university": "Yale", "duration": "Self-paced", "description": "Explore the basics of psychology.", "degree_level": "Beginner", "field_of_study": "Psychology", "country": "USA"}
        ]
        if subject:
            courses = [course for course in courses if course['field_of_study'] == subject]
        return courses[:limit]
    
def get_indian_courses(field_of_study=None, degree_level=None, limit=5):
    """
    Fetch mock course data for India.
    
    Args:
        field_of_study (str, optional): The field of study to filter courses.
        degree_level (str, optional): The degree level to filter courses.
        limit (int): The maximum number of courses to return.
        
    Returns:
        list: A list of mock courses.
    """
    indian_courses = [
        {"title": "Bachelor of Technology in Computer Science", "university": "IIT Delhi", "duration": "4 years", "description": "Comprehensive program in computer science and engineering.", "degree_level": "Bachelor", "field_of_study": "Computer Science", "country": "India"},
        {"title": "Master of Business Administration", "university": "IIM Ahmedabad", "duration": "2 years", "description": "Premier MBA program for business leaders.", "degree_level": "Master", "field_of_study": "Business", "country": "India"},
        {"title": "Bachelor of Science in Data Science", "university": "Christ University, Bangalore", "duration": "3 years", "description": "Focuses on data analysis and machine learning.", "degree_level": "Bachelor", "field_of_study": "Data Science", "country": "India"},
        {"title": "Master of Arts in Psychology", "university": "University of Mumbai", "duration": "2 years", "description": "Advanced study of human behavior and mental processes.", "degree_level": "Master", "field_of_study": "Psychology", "country": "India"},
        {"title": "Bachelor of Design in Graphic Design", "university": "NID Ahmedabad", "duration": "4 years", "description": "Specialization in visual communication and design.", "degree_level": "Bachelor", "field_of_study": "Graphic Design", "country": "India"}
    ]
    
    filtered_courses = indian_courses
    if field_of_study:
        filtered_courses = [course for course in filtered_courses if course['field_of_study'] == field_of_study]
    if degree_level:
        filtered_courses = [course for course in filtered_courses if course['degree_level'] == degree_level]
    return filtered_courses[:limit]

# Custom Jinja2 filter for datetime formatting
@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return value.strftime(format)


# Generate dynamic test questions with no repeats in a session
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
        # Retrieve used questions from session to avoid repeats
        used_questions = session.get('used_aptitude', [])
        
        # Collect all questions by difficulty across categories
        all_easy = []
        all_moderate = []
        all_hard = []
        for category in APTITUDE_QUESTIONS.keys():
            for q in APTITUDE_QUESTIONS[category]['easy']:
                if q['id'] not in used_questions:
                    all_easy.append(q)
            for q in APTITUDE_QUESTIONS[category]['moderate']:
                if q['id'] not in used_questions:
                    all_moderate.append(q)
            for q in APTITUDE_QUESTIONS[category]['hard']:
                if q['id'] not in used_questions:
                    all_hard.append(q)
        
        # Validate sufficient questions are available
        if len(all_easy) < 5:
            raise ValueError(f"Not enough easy questions available. Required: 5, Found: {len(all_easy)}")
        if len(all_moderate) < 7:
            raise ValueError(f"Not enough moderate questions available. Required: 7, Found: {len(all_moderate)}")
        if len(all_hard) < 8:
            raise ValueError(f"Not enough hard questions available. Required: 8, Found: {len(all_hard)}")
        
        # Randomly select questions
        selected_easy = random.sample(all_easy, 5)
        selected_moderate = random.sample(all_moderate, 7)
        selected_hard = random.sample(all_hard, 8)
        
        # Combine in the specified order
        questions = selected_easy + selected_moderate + selected_hard
        
        # Ensure time_limit is set
        for q in questions:
            q['time_limit'] = q.get('time_limit', 60)
        
        # Update session data
        session['aptitude_questions'] = questions
        session['used_aptitude'] = [q['id'] for q in questions]
        session['aptitude_responses'] = []
        session['ability_estimate'] = 0.0
        session['aptitude_correct'] = 0
        session['aptitude_total'] = 0
        
        # Initialize category counts and scores for all categories
        session['aptitude_category_counts'] = {cat: 0 for cat in APTITUDE_QUESTIONS.keys()}
        session['aptitude_category_scores'] = {cat: 0 for cat in APTITUDE_QUESTIONS.keys()}
        
        return questions
    
    elif test_type == 'personality':
        questions = random.sample(PERSONALITY_QUESTIONS, min(10, len(PERSONALITY_QUESTIONS)))
        for q in questions:
            q['time_limit'] = q.get('time_limit', 60)
        session['personality_questions'] = questions
        return questions
    
    elif test_type == 'skill_gap':
        field = session.get('selected_field', 'Software Development')
        available_questions = copy.deepcopy(SKILL_GAP_QUESTIONS.get(field, []))
        if len(available_questions) < 10:
            flash(f'Insufficient questions for {field}.', 'danger')
            return []
        questions = random.sample(available_questions, 10)
        for q in questions:
            q['time_limit'] = q.get('time_limit', 60)
        session['skill_gap_questions'] = questions
        session['skill_gap_correct'] = 0
        session['skill_gap_total'] = 0
        session['responses'] = []
        return questions
        
    return []

# Routes
@app.route('/')
def index():
    if not current_user.is_authenticated and not session.get('_flashes'):
        flash('Kindly log in to unlock comprehensive access to all features.', 'info')
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all() if current_user.is_authenticated else []
    return render_template('index.html', active_page='index', notifications=notifications, current_year=datetime.utcnow().year)

@app.route('/student')
@login_required
def student():
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
    return render_template('student.html', user=current_user, active_page='student', notifications=notifications)

@app.route('/degree', methods=['GET'])
@login_required
def degree():
    """
    Degree search with India/Abroad toggle, institute listings, and test requirements.
    """
    # Fetch query parameters
    location_type    = request.args.get('location_type', 'india')  # 'india' or 'abroad'
    degree_level     = request.args.get('degree_level', '').strip()
    field_of_study   = request.args.get('field_of_study', '').strip()
    duration         = request.args.get('duration', '').strip()
    country          = request.args.get('country', '').strip()
    university_sel   = request.args.get('university', '').strip()
    keyword          = request.args.get('keyword', '').strip().lower()
    sort_by          = request.args.get('sort_by', '').strip()

    # Base courses fetched via EdX or local data
    # For simplicity, reuse LEARNING_RESOURCES mapping as 'degrees'
    raw_degrees = LEARNING_RESOURCES.get(field_of_study or 'General', [])

    # Apply basic filters on raw_degrees
    filtered_degrees = raw_degrees
    if degree_level:
        filtered_degrees = [d for d in filtered_degrees if d.get('degree_level') == degree_level]
    if duration:
        filtered_degrees = [d for d in filtered_degrees if d.get('duration') == duration]
    if keyword:
        filtered_degrees = [d for d in filtered_degrees if keyword in d.get('title', '').lower()]
    # Sorting
    if sort_by == 'title':
        filtered_degrees.sort(key=lambda x: x.get('title',''))

    # --- Fetch Institutes via Hipolabs API ---
    institutes = []
    try:
        if location_type == 'india':
            resp = requests.get('https://universities.hipolabs.com/search', params={'country': 'India'})
        else:
            # Abroad: require user-selected country, default to 'United States'
            target = country or 'United States'
            resp = requests.get('https://universities.hipolabs.com/search', params={'country': target})
        if resp.status_code == 200:
            all_unis = resp.json()
            # Filter by field_of_study keyword in university name
            if field_of_study:
                institutes = [u for u in all_unis if field_of_study.lower() in u['name'].lower()]
            else:
                institutes = all_unis
            # Limit to top 10
            institutes = institutes[:10]
    except Exception as e:
        institutes = []
        print("Error fetching institutes:", e)

    # --- Test Requirements Mapping ---
    TEST_MAP = {
        'Engineering': ['JEE Main', 'JEE Advanced'],
        'Medicine':    ['NEET'],
        'Business':    ['CAT', 'GMAT'],
        'Arts':        ['CUET'],
        'General':     []
    }
    # For abroad, add TOEFL/IELTS for all fields
    base_tests = TEST_MAP.get(field_of_study, TEST_MAP['General'])
    if location_type == 'abroad':
        abroad_tests = ['TOEFL', 'IELTS']
        tests = base_tests + abroad_tests
    else:
        tests = base_tests

    # Dropdown options (static or derived)
    countries       = sorted({u.get('country','') for u in institutes if u.get('country')})
    degree_levels   = sorted({d.get('degree_level','') for d in raw_degrees})
    fields_of_study = sorted(CAREER_MAPPING.keys())
    durations       = sorted({d.get('duration','') for d in raw_degrees})
    universities    = sorted({u.get('name','') for u in institutes})

    # Notifications
    notifications = (
        Notification.query
        .filter_by(user_id=current_user.id, is_read=False)
        .order_by(Notification.date.desc())
        .limit(5)
        .all()
    )

    return render_template(
        'degree.html',
        degrees=filtered_degrees,
        institutes=institutes,
        tests=tests,
        countries=countries,
        universities=universities,
        degree_levels=degree_levels,
        fields_of_study=fields_of_study,
        durations=durations,
        selected_location=location_type,
        selected_degree_level=degree_level,
        selected_field_of_study=field_of_study,
        selected_duration=duration,
        selected_country=country,
        selected_university=university_sel,
        keyword=keyword,
        sort_by=sort_by,
        notifications=notifications
    )

@app.route('/degree/compare', methods=['GET', 'POST'])
@login_required
def compare_degrees():
    user_id = current_user.id
    user = User.query.get(user_id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('degree'))

    # Fetch user's aptitude scores to suggest relevant degrees
    aptitude_scores = json.loads(user.aptitude_scores) if user.aptitude_scores else {}
    top_careers = json.loads(user.top_careers) if user.top_careers else []

    if not top_careers and not aptitude_scores:
        flash('Please complete an aptitude test to get personalized degree recommendations.', 'warning')
        return redirect(url_for('degree'))

    # Fetch degree data based on top careers or aptitude
    degree_data = {}
    onet_api = ONetAPI()
    selected_degrees = request.form.getlist('degree_select') if request.method == 'POST' else []

    if request.method == 'POST' and selected_degrees:
        for soc_code in selected_degrees[:3]:  # Limit to 3 for comparison
            details = onet_api.get_occupation_summary(soc_code)
            education = onet_api.get_education(soc_code)
            skills = onet_api.get_skills(soc_code)
            if details and education:
                degree_data[soc_code] = {
                    'title': details.get('title', 'Unknown'),
                    'education': education.get('level_required', [{'name': 'Not specified', 'score': 0}]),
                    'required_skills': [skill.get('name', 'N/A') for skill in skills],
                    'description': details.get('description', 'No description available')
                }
    else:
        # Default to top careers from aptitude if available
        career_codes = top_careers[:3] if top_careers else ['15-1252.00', '15-2051.01', '27-1024.00']  # Default SOC codes
        for soc_code in career_codes:
            details = onet_api.get_occupation_summary(soc_code)
            education = onet_api.get_education(soc_code)
            skills = onet_api.get_skills(soc_code)
            if details and education:
                degree_data[soc_code] = {
                    'title': details.get('title', 'Unknown'),
                    'education': education.get('level_required', [{'name': 'Not specified', 'score': 0}]),
                    'required_skills': [skill.get('name', 'N/A') for skill in skills],
                    'description': details.get('description', 'No description available')
                }

    # Match degrees with aptitude scores for recommendation
    recommendations = []
    for soc_code, data in degree_data.items():
        match_score = 0
        if aptitude_scores:
            career_aptitude = {APTITUDE_TO_ONET.get(k, k): v for k, v in aptitude_scores.items()}
            onet_abilities = onet_api.get_abilities(soc_code)
            required_aptitude = {a['name']: float(a.get('level', 50)) for a in onet_abilities} if onet_abilities else {}
            match_score = sum(min(career_aptitude.get(k, 0), required_aptitude.get(k, 0)) for k in set(career_aptitude) & set(required_aptitude)) / max(len(career_aptitude), 1) * 100
        recommendations.append({'soc_code': soc_code, 'score': match_score, 'data': data})

    recommendations.sort(key=lambda x: x['score'], reverse=True)
    degree_data = {r['soc_code']: r['data'] for r in recommendations[:3]}  # Top 3 matches

    notifications = Notification.query.filter_by(user_id=user_id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
    return render_template(
        'degree_compare.html',
        user=user,
        degree_data=degree_data,
        aptitude_scores=aptitude_scores,
        notifications=notifications
    )

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
    tests = TestResult.query.filter_by(user_id=current_user.id).order_by(TestResult.completed_at.desc()).all()
    badges = Badge.query.filter_by(user_id=current_user.id).order_by(Badge.date_earned.desc()).limit(5).all()
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
    
    # Use session's completed_tests if available, otherwise build from test history
    completed_tests = session.get('completed_tests', [t.test_type for t in tests])
    test_results = session.get('test_results', {})
    
    # Build test_results from TestResult if not in session
    for test in tests:
        if test.test_type not in test_results:
            test_results[test.test_type] = {'score': test.score}
    session['test_results'] = test_results

    # Generate test labels and scores for the chart
    test_labels = [test.completed_at.strftime('%Y-%m-%d') for test in tests]
    test_scores = [test.score for test in tests]
    
    # Calculate average score and recommendation
    recent_tests = [t for t in tests if t.test_type in ['aptitude', 'personality', 'skill_gap']]
    max_score = 10  # Adjust based on your scoring system
    recommendation = "Take more tests to improve your skills!" if len(recent_tests) < 3 else "Great job! Consider exploring career matches."

    return render_template('dashboard.html', 
                          user=current_user, 
                          tests=tests, 
                          recent_tests=recent_tests,
                          badges=badges, 
                          notifications=notifications,
                          completed_tests=completed_tests,
                          test_results=test_results,
                          test_labels=test_labels,
                          test_scores=test_scores,
                          max_score=max_score,
                          recommendation=recommendation,
                          active_page='dashboard')

@app.route('/test', methods=['GET', 'POST'])
@login_required
def test():
    test_type = request.args.get('type')
    instructions = {
        "time_limit": "You have 10 minutes to complete this test.",
        "honesty": "Please answer all questions honestly and without external assistance.",
        "scientific_accuracy": "This test is designed to assess your skills with validated questions."
    }

    # Enforce test sequence
    completed_tests = session.get('completed_tests', [])
    if test_type == 'personality' and 'aptitude' not in completed_tests:
        flash('Please complete the Aptitude Test before taking the Personality Test.', 'warning')
        return redirect(url_for('dashboard'))
    if test_type == 'skill_gap' and ('aptitude' not in completed_tests or 'personality' not in completed_tests):
        flash('Please complete both the Aptitude and Personality Tests before taking the Skill Gap Test.', 'warning')
        return redirect(url_for('dashboard'))

    if not test_type:
        flash('Please select a test type (e.g., aptitude, personality, skill_gap).', 'warning')
        return redirect(url_for('dashboard'))

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
        # Clear previous session data to start fresh
        session.pop('aptitude_questions', None)
        session.pop('aptitude_responses', None)
        session.pop('ability_estimate', None)
        session.pop('used_aptitude', None)
        session.pop('aptitude_correct', None)
        session.pop('aptitude_total', None)
        session.pop('aptitude_category_scores', None)
        session.pop('aptitude_category_counts', None)

        # Generate questions
        questions = generate_questions('aptitude')
        if not questions:
            flash('No aptitude questions available at this time.', 'danger')
            return redirect(url_for('dashboard'))

        # Initialize session data
        session['aptitude_questions'] = questions  # Store all questions
        session['aptitude_responses'] = []
        session['ability_estimate'] = 0.0
        session['current_question_index'] = session.get('current_question_index', 0)

        current_question_index = session['current_question_index']
        total_questions = len(questions)

        if current_question_index >= total_questions:
            return redirect(url_for('aptitude_results'))

        question = questions[current_question_index]
        category = next((cat for cat, levels in APTITUDE_QUESTIONS.items() if any(question['id'] in [q['id'] for q in level] for level in levels.values())), "Unknown")

        if request.method == 'POST':
            user_answer = request.form.get('answer')
            if user_answer is not None:
                session['aptitude_responses'].append(int(user_answer))
                session['current_question_index'] += 1
                return redirect(url_for('test', type='aptitude'))

        notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
        return render_template('assessments/aptitude.html',
                              questions=[question],
                              instructions=instructions,
                              current_category=category,
                              total_questions=total_questions,
                              completed_questions=current_question_index,
                              current_question_index=current_question_index,
                              initial_time=question['time_limit'],
                              active_page='test',
                              test_type='aptitude',
                              notifications=notifications)

    elif test_type == 'personality':
        questions = session.get('personality_questions')
        if not questions or request.method == 'GET':
            questions = generate_questions('personality')
            session['personality_questions'] = questions
            logger.debug(f"Session questions: {questions}")
            # logger.debug(f"Received responses: {responses}")
        notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
        return render_template('assessments/personality.html',
                              questions=questions,
                              instructions=instructions,
                              active_page='test',
                              test_type='personality',
                              notifications=notifications)

    elif test_type == 'interest_test':
        selected_field = request.args.get('field', session.get('selected_field', None))
        if not selected_field:
            return render_template('assessments/interest_test.html', selected_field=None, questions=[], total_questions=0, completed_questions=0, current_question_index=0, initial_time=60)

        session['selected_field'] = selected_field
        questions = session.get('skill_gap_questions', [])
        if not questions or session.get('skill_gap_field') != selected_field:
            session.pop('skill_gap_questions', None)
            session.pop('skill_gap_correct', None)
            session.pop('skill_gap_total', None)
            session.pop('responses', None)
            questions = generate_questions('skill_gap')
            if not questions:
                return redirect(url_for('dashboard'))
            session['skill_gap_field'] = selected_field

        current_question_index = int(request.args.get('q', 0))
        if current_question_index >= len(questions):
            return redirect(url_for('skill_gap_results'))
        question = questions[current_question_index]
        return render_template('assessments/interest_test.html',
                              selected_field=selected_field,
                              questions=[question],
                              total_questions=len(questions),
                              completed_questions=current_question_index,
                              current_question_index=current_question_index,
                              initial_time=question['time_limit'])

    flash(f'Invalid test type: {test_type}. Please choose aptitude, personality, or skill_gap.', 'danger')
    return redirect(url_for('dashboard'))

@test_bp.route('/aptitude', methods=['GET', 'POST'])
def aptitude_test():
    user_id = current_user.id  # Use current_user.id instead of request.args.get('user_id')
    if not user_id:
        flash('User not found.', 'danger')
        return redirect(url_for('dashboard'))

    # Initialize or retrieve ability estimate
    current_theta = float(session.get('ability_estimate', 0.0))
    questions = session.get('aptitude_questions', [])
    user_responses = session.get('aptitude_responses', [])
    used_questions = session.get('used_aptitude', [])

    if request.method == 'POST':
        # Process the submitted answer
        answer = request.form.get('answer')
        question_id = request.form.get('question_id')
        if not answer or not question_id:
            flash('Answer or question ID missing.', 'danger')
            return redirect(url_for('aptitude_test'))

        try:
            answer = int(answer)
        except ValueError:
            flash('Invalid answer format.', 'danger')
            return redirect(url_for('aptitude_test'))

        # Find the current question
        current_question = next((q for q in questions if q['id'] == question_id), None)
        if not current_question:
            flash('Question not found.', 'danger')
            return redirect(url_for('aptitude_test'))

        # Check if the answer is correct and update session data
        is_correct = answer == current_question.get('correct')
        user_responses.append({
            'question_id': question_id,
            'answer': answer,
            'correct': is_correct,
            'time_spent': int(request.form.get('time_spent', 0))
        })
        session['aptitude_responses'] = user_responses

        # Update category-based scoring
        category = next(
            (cat for cat, levels in APTITUDE_QUESTIONS.items() if any(
                question_id in [q['id'] for q in level] for level in levels.values()
            )),
            "Unknown"
        )
        session['aptitude_total'] = session.get('aptitude_total', 0) + 1
        session['aptitude_correct'] = session.get('aptitude_correct', 0) + (1 if is_correct else 0)
        session['aptitude_category_counts'] = session.get('aptitude_category_counts', defaultdict(int))
        session['aptitude_category_scores'] = session.get('aptitude_category_scores', defaultdict(int))
        session['aptitude_category_counts'][category] += 1
        session['aptitude_category_scores'][category] += (1 if is_correct else 0)
        session.modified = True

        # Update theta based on IRT (simplified)
        irt_params = current_question.get('irt_params', {'difficulty': 0.0, 'discrimination': 1.0})
        expected_prob = 1 / (1 + np.exp(-irt_params['discrimination'] * (current_theta - irt_params['difficulty'])))
        if is_correct:
            current_theta += ADAPTIVE_TEST_SETTINGS['scaling_factors']['correct_answer'] * (1 - expected_prob)
        else:
            current_theta += ADAPTIVE_TEST_SETTINGS['scaling_factors']['wrong_answer'] * expected_prob
        session['ability_estimate'] = current_theta

        # Select next question with adaptive difficulty
        current_question_index = int(request.args.get('q', 0))
        next_question = select_next_question(user_id, current_theta)
        if next_question:
            questions[current_question_index + 1] = next_question
            used_questions.append(next_question['id'])
            session['aptitude_questions'] = questions
            session['used_aptitude'] = used_questions
            return redirect(url_for('aptitude_test', q=current_question_index + 1))
        else:
            # Test complete - save results
            overall_score = (session['aptitude_correct'] / session['aptitude_total']) * 100 if session['aptitude_total'] > 0 else 0
            detailed_scores = {
                cat: (session['aptitude_category_scores'][cat] / session['aptitude_category_counts'][cat]) * 100
                for cat in session['aptitude_category_counts'] if session['aptitude_category_counts'][cat] > 0
            }
            result = TestResult(
                user_id=user_id,
                test_type='aptitude',
                score=overall_score,
                time_spent=sum(r['time_spent'] for r in user_responses),
                details=json.dumps(detailed_scores)
            )
            current_user.aptitude_scores = json.dumps(detailed_scores)
            db.session.add(result)

            # Award badges
            if not Badge.query.filter_by(user_id=user_id, name="First Test Completed").first():
                badge = Badge(user_id=user_id, name="First Test Completed", description="Completed your first aptitude test!", icon="fas fa-trophy")
                db.session.add(badge)
            if overall_score >= 80:
                if not Badge.query.filter_by(user_id=user_id, name="Aptitude Master").first():
                    badge = Badge(user_id=user_id, name="Aptitude Master", description="Scored 80% or higher in aptitude test!", icon="fas fa-star")
                    db.session.add(badge)

            # Send notification
            notification = Notification(
                user_id=user_id,
                message=f"Aptitude Test completed! Score: {overall_score:.1f}%. Well done!",
                type="test_result"
            )
            db.session.add(notification)
            db.session.commit()

            completed_tests = session.get('completed_tests', [])
            if 'aptitude' not in completed_tests:
                completed_tests.append('aptitude')
                session['completed_tests'] = completed_tests

            # Clear session data
            session.pop('aptitude_questions', None)
            session.pop('aptitude_responses', None)
            session.pop('ability_estimate', None)
            session.pop('used_aptitude', None)
            session.pop('aptitude_correct', None)
            session.pop('aptitude_total', None)
            session.pop('aptitude_category_scores', None)
            session.pop('aptitude_category_counts', None)

            return redirect(url_for('aptitude_results'))

    # Handle GET request - initialize or continue test
    if not questions:
        session.pop('aptitude_questions', None)
        session.pop('aptitude_responses', None)
        session.pop('ability_estimate', None)
        session.pop('used_aptitude', None)
        session.pop('aptitude_correct', None)
        session.pop('aptitude_total', None)
        session.pop('aptitude_category_scores', None)
        session.pop('aptitude_category_counts', None)

        questions = generate_questions('aptitude')
        if not questions:
            flash('No aptitude questions available at this time.', 'danger')
            return redirect(url_for('dashboard'))

        session['aptitude_questions'] = questions
        session['aptitude_responses'] = []
        session['ability_estimate'] = 0.0

    current_question_index = int(request.args.get('q', 0))
    if current_question_index >= len(questions):
        return redirect(url_for('aptitude_results'))

    question = questions[current_question_index]
    category = next(
        (cat for cat, levels in APTITUDE_QUESTIONS.items() if any(
            question['id'] in [q['id'] for q in level] for level in levels.values()
        )),
        "Unknown"
    )
    notifications = Notification.query.filter_by(user_id=user_id, is_read=False).order_by(Notification.date.desc()).limit(5).all()

    return render_template(
        'assessments/aptitude.html',
        questions=[question],
        instructions={
            "time_limit": "You have 10 minutes to complete this test.",
            "honesty": "Please answer all questions honestly and without external assistance.",
            "scientific_accuracy": "This test is designed to assess your skills with validated questions."
        },
        current_category=category,
        total_questions=len(questions),
        completed_questions=current_question_index,
        current_question_index=current_question_index,
        initial_time=question['time_limit'],
        active_page='test',
        test_type='aptitude',
        notifications=notifications
    )

@app.route('/career_assessment', methods=['GET'])
def career_assessment():
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all() if current_user.is_authenticated else []
    return render_template('career_assessment.html',active_page='career_assessment', notifications=notifications)

@app.route('/submit_aptitude', methods=['POST'])
@login_required
def submit_aptitude():
    data = request.get_json()
    if not data or 'responses' not in data:
        return jsonify({'error': 'No data provided'}), 400

    responses = data['responses']
    time_spent = data.get('time_spent', 0)
    current_question_index = data.get('current_question_index', 0)

    questions = session.get('aptitude_questions', [])
    user_responses = session.get('aptitude_responses', [])
    
    if not questions or current_question_index >= len(questions):
        return jsonify({'error': 'No more questions available'}), 400

    current_response = responses[-1]
    question_id = current_response['questionId']
    
    try:
        answer = int(current_response['answer'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid answer format'}), 400

    current_question = next((q for q in questions if q['id'] == question_id), None)
    if not current_question:
        return jsonify({'error': 'Question not found'}), 400

    is_correct = answer == current_question['correct']
    user_responses.append({
        'question_id': question_id,
        'answer': answer,
        'correct': is_correct,
        'time_spent': time_spent
    })
    session['aptitude_responses'] = user_responses

    # Update category-based scoring
    category = next(
        (cat for cat, levels in APTITUDE_QUESTIONS.items() if any(
            question_id in [q['id'] for q in level] for level in levels.values()
        )),
        "Unknown"
    )
    
    # Ensure category exists in dictionaries (safeguard)
    if category not in session['aptitude_category_counts']:
        session['aptitude_category_counts'][category] = 0
        session['aptitude_category_scores'][category] = 0

    session['aptitude_total'] += 1
    if is_correct:
        session['aptitude_correct'] += 1
    session['aptitude_category_counts'][category] += 1
    if is_correct:
        session['aptitude_category_scores'][category] += 1
    session.modified = True

    # Proceed to next question or complete test
    if current_question_index + 1 < len(questions):
        next_question = questions[current_question_index + 1]
        return jsonify({
            'question': next_question,
            'current_question_index': current_question_index + 1
        })
    else:
        # Test complete - calculate and save results
        overall_score = (session['aptitude_correct'] / session['aptitude_total']) * 100 if session['aptitude_total'] > 0 else 0
        detailed_scores = {
            cat: (session['aptitude_category_scores'][cat] / session['aptitude_category_counts'][cat]) * 100
            for cat in session['aptitude_category_counts'] if session['aptitude_category_counts'][cat] > 0
        }
        result = TestResult(
            user_id=current_user.id,
            test_type='aptitude',
            score=overall_score,
            time_spent=sum(r['time_spent'] for r in user_responses),
            details=json.dumps(detailed_scores)
        )
        current_user.aptitude_scores = json.dumps(detailed_scores)
        db.session.add(result)

        # Award badges
        if not Badge.query.filter_by(user_id=current_user.id, name="First Test Completed").first():
            badge = Badge(user_id=current_user.id, name="First Test Completed", description="Completed your first aptitude test!", icon="fas fa-trophy")
            db.session.add(badge)
        if overall_score >= 80:
            if not Badge.query.filter_by(user_id=current_user.id, name="Aptitude Master").first():
                badge = Badge(user_id=current_user.id, name="Aptitude Master", description="Scored 80% or higher in aptitude test!", icon="fas fa-star")
                db.session.add(badge)

        # Send notification
        notification = Notification(
            user_id=current_user.id,
            message=f"Aptitude Test completed! Score: {overall_score:.1f}%. Well done!",
            type="test_result"
        )
        db.session.add(notification)
        db.session.commit()

        # Update completed tests
        completed_tests = session.get('completed_tests', [])
        if 'aptitude' not in completed_tests:
            completed_tests.append('aptitude')
            session['completed_tests'] = completed_tests

        # Store results in session for display
        session['test_results'] = session.get('test_results', {})
        session['test_results']['aptitude'] = {
            'score': overall_score,
            'correct': session['aptitude_correct'],
            'total': session['aptitude_total'],
            'time_spent': sum(r['time_spent'] for r in user_responses),
            'detailed_scores': detailed_scores,
            'responses': user_responses,
            'questions': questions
        }

        # Clear session data
        session.pop('aptitude_questions', None)
        session.pop('aptitude_responses', None)
        session.pop('ability_estimate', None)
        session.pop('used_aptitude', None)
        session.pop('aptitude_correct', None)
        session.pop('aptitude_total', None)
        session.pop('aptitude_category_scores', None)
        session.pop('aptitude_category_counts', None)

        return jsonify({'redirect': url_for('aptitude_results')})

@app.route('/submit_assessment', methods=['POST'])
@login_required
def submit_assessment():
    data = request.get_json()
    logger.debug(f"Received JSON data: {data}")
    if not data or 'responses' not in data or data.get('type') != 'personality':
        logger.error("Invalid data format or type")
        return jsonify({'error': 'Invalid data'}), 400

    responses = data['responses']
    duration = data.get('duration', 0)
    questions = session.get('personality_questions', [])
    logger.debug(f"Processing {len(responses)} responses with {len(questions)} questions")

    if not questions or len(responses) != len(questions):
        logger.error("Mismatch in response and question count")
        return jsonify({'error': 'Session data missing or incomplete responses'}), 400

    scores = {'Openness': 0, 'Conscientiousness': 0, 'Extraversion': 0, 'Agreeableness': 0, 'Neuroticism': 0}
    counts = {trait: 0 for trait in scores}
    trait_mapping = {'O': 'Openness', 'C': 'Conscientiousness', 'E': 'Extraversion', 'A': 'Agreeableness', 'N': 'Neuroticism'}

    for response in responses:
        if not isinstance(response, dict) or 'questionId' not in response or 'answer' not in response:
            logger.error(f"Invalid response format: {response}")
            continue
        try:
            question_id = int(response['questionId'])
        except ValueError:
            logger.error(f"Invalid questionId: {response['questionId']}")
            continue
        question = next((q for q in questions if q['id'] == question_id), None)
        if not question:
            logger.warning(f"Question ID {question_id} not found")
            continue
        try:
            value = int(response['answer'])
            if value < 0 or value > 4:
                logger.warning(f"Invalid answer value {value} for question {question['id']}")
                continue
            trait = question.get('trait')
            if not trait or trait not in trait_mapping:
                logger.error(f"Invalid or missing trait {trait} for question {question['id']}")
                continue
            trait_name = trait_mapping[trait]
            direction = question.get('direction', 'positive')
            score = value if direction == 'positive' else (4 - value)
            scores[trait_name] += score
            counts[trait_name] += 1
            logger.debug(f"Scored {trait_name}: value={value}, direction={direction}, score={score}")
        except ValueError as e:
            logger.error(f"Invalid answer type in response {response}: {e}")
            continue

    for trait in scores:
        if counts[trait] > 0:
            scores[trait] = (scores[trait] / (counts[trait] * 4)) * 100
        else:
            scores[trait] = 0
            logger.warning(f"No valid responses for {trait}")

    dominant_trait = max(scores, key=scores.get)
    result = TestResult(
        user_id=current_user.id,
        test_type='personality',
        score=scores[dominant_trait],
        time_spent=duration,
        details=json.dumps(scores)
    )
    current_user.personality_scores = json.dumps(scores)
    db.session.add(result)

    # Award badges
    if not Badge.query.filter_by(user_id=current_user.id, name="First Test Completed").first():
        badge = Badge(user_id=current_user.id, name="First Test Completed", description="Completed your first personality test!", icon="fas fa-trophy")
        db.session.add(badge)
    if scores[dominant_trait] >= 80:
        if not Badge.query.filter_by(user_id=current_user.id, name="Personality Pro").first():
            badge = Badge(user_id=current_user.id, name="Personality Pro", description="Scored 80% or higher in personality trait!", icon="fas fa-star")
            db.session.add(badge)

    # Send notification
    notification = Notification(
        user_id=current_user.id,
        message=f"Personality Test completed! Dominant trait: {dominant_trait} ({scores[dominant_trait]:.1f}%)",
        type="test_result"
    )
    db.session.add(notification)
    db.session.commit()

    completed_tests = session.get('completed_tests', [])
    if 'personality' not in completed_tests:
        completed_tests.append('personality')
        session['completed_tests'] = completed_tests

    test_results = session.get('test_results', {})
    test_results['personality'] = {'score': scores[dominant_trait], 'details': scores}
    session['test_results'] = test_results

    session.pop('personality_questions', None)
    return jsonify({'redirect': url_for('personality_results')})

from collections import defaultdict

def identify_weaknesses(questions, responses, correct_count):
    weaknesses = defaultdict(lambda: {"count": 0, "description": "", "tips": [], "resources": []})
    total_questions = len(questions)
    total_wrong = max(0, total_questions - correct_count)

    for response in responses:
        question_id = response['questionId']
        answer = int(response['answer'])
        question = next((q for q in questions if q['id'] == question_id), None)
        if question and answer != question.get('correct', -1):
            text = question['text'].lower()
            # Software Development
            if "python" in text:
                topic = "Python Programming"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "understanding Python syntax and concepts",
                    "tips": ["Practice coding exercises", "Review Python tutorials"],
                    "resources": LEARNING_RESOURCES["Software Development"]["basic"]
                })
            elif "inheritance" in text or "object-oriented" in text:
                topic = "Object-Oriented Programming"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "grasping OOP concepts like inheritance",
                    "tips": ["Study class hierarchies", "Implement small OOP projects"],
                    "resources": LEARNING_RESOURCES["Software Development"]["intermediate"]
                })
            elif "git" in text:
                topic = "Version Control"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "using Git for version control",
                    "tips": ["Practice Git commands", "Explore Git workflows"],
                    "resources": LEARNING_RESOURCES["Software Development"]["basic"]
                })
            elif "http" in text or "restful" in text:
                topic = "RESTful APIs"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "understanding HTTP status codes and API design",
                    "tips": ["Study API basics", "Test APIs with Postman"],
                    "resources": LEARNING_RESOURCES["Software Development"]["intermediate"]
                })
            elif "time complexity" in text or "algorithm" in text:
                topic = "Algorithms"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "analyzing time complexity and algorithm efficiency",
                    "tips": ["Solve algorithm problems", "Review Big O notation"],
                    "resources": LEARNING_RESOURCES["Software Development"]["advanced"]
                })
            elif "sql" in text or "database" in text:
                topic = "SQL"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "writing efficient database queries",
                    "tips": ["Practice SQL joins", "Learn indexing"],
                    "resources": LEARNING_RESOURCES["Software Development"]["intermediate"]
                })
            elif "docker" in text or "container" in text:
                topic = "Containerization"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "using Docker for application deployment",
                    "tips": ["Build Docker images", "Learn Docker Compose"],
                    "resources": LEARNING_RESOURCES["Software Development"]["advanced"]
                })
            elif "testing" in text and "unit" not in text:
                topic = "Software Testing"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "implementing regression and integration tests",
                    "tips": ["Write test cases", "Automate testing"],
                    "resources": LEARNING_RESOURCES["Software Development"]["intermediate"]
                })
            elif "ci/cd" in text or "devops" in text:
                topic = "DevOps"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "understanding CI/CD pipelines",
                    "tips": ["Set up a CI/CD tool", "Learn Jenkins or GitHub Actions"],
                    "resources": LEARNING_RESOURCES["Software Development"]["advanced"]
                })
            elif "unit testing" in text or "unittest" in text:
                topic = "Unit Testing"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "writing unit tests in Python",
                    "tips": ["Use unittest or pytest", "Practice TDD"],
                    "resources": LEARNING_RESOURCES["Software Development"]["intermediate"]
                })
            # Data Science
            elif "pandas" in text or "data manipulation" in text:
                topic = "Data Manipulation"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "manipulating data with Pandas",
                    "tips": ["Learn DataFrame operations", "Practice with datasets"],
                    "resources": LEARNING_RESOURCES["Data Science"]["basic"]
                })
            elif "p-value" in text or "hypothesis" in text:
                topic = "Statistics"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "applying statistical tests",
                    "tips": ["Review hypothesis testing", "Learn p-values"],
                    "resources": LEARNING_RESOURCES["Data Science"]["intermediate"]
                })
            elif "supervised" in text or "logistic regression" in text:
                topic = "Machine Learning"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "understanding supervised learning algorithms",
                    "tips": ["Study logistic regression", "Implement classifiers"],
                    "resources": LEARNING_RESOURCES["Data Science"]["advanced"]
                })
            elif "matplotlib" in text or "bar chart" in text:
                topic = "Data Visualization"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "creating effective charts with Matplotlib",
                    "tips": ["Explore Seaborn", "Practice plotting"],
                    "resources": LEARNING_RESOURCES["Data Science"]["basic"]
                })
            # Graphic Design
            elif "photoshop" in text:
                topic = "Photoshop Skills"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "using Photoshop for image editing",
                    "tips": ["Learn tool functionalities", "Practice photo retouching"],
                    "resources": LEARNING_RESOURCES["Graphic Design"]["basic"]
                })
            elif "illustrator" in text:
                topic = "Illustrator Skills"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "creating vector graphics with Illustrator",
                    "tips": ["Master the Pen Tool", "Design simple logos"],
                    "resources": LEARNING_RESOURCES["Graphic Design"]["intermediate"]
                })
            elif "color theory" in text:
                topic = "Color Theory"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "understanding color relationships",
                    "tips": ["Study the color wheel", "Experiment with palettes"],
                    "resources": LEARNING_RESOURCES["Graphic Design"]["basic"]
                })
            # Business Management
            elif "swot" in text:
                topic = "Strategic Planning"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "developing strategic plans",
                    "tips": ["Practice SWOT analysis", "Study business cases"],
                    "resources": LEARNING_RESOURCES["Business Management"]["intermediate"]
                })
            elif "financial forecasting" in text:
                topic = "Financial Forecasting"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "predicting financial performance",
                    "tips": ["Learn financial modeling", "Analyze historical data"],
                    "resources": LEARNING_RESOURCES["Business Management"]["advanced"]
                })
            elif "leadership style" in text:
                topic = "Leadership"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "understanding leadership styles",
                    "tips": ["Study leadership theories", "Practice team management"],
                    "resources": LEARNING_RESOURCES["Business Management"]["intermediate"]
                })
            elif "gantt chart" in text:
                topic = "Project Management"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "visualizing project timelines",
                    "tips": ["Use project management tools", "Plan a small project"],
                    "resources": LEARNING_RESOURCES["Business Management"]["basic"]
                })
            # Scientific
            elif "scientific method" in text:
                topic = "Research Methodology"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "applying the scientific method",
                    "tips": ["Formulate hypotheses", "Design experiments"],
                    "resources": LEARNING_RESOURCES["Scientific"]["basic"]
                })
            elif "p-value" in text or "anova" in text:
                topic = "Statistics"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "interpreting statistical results",
                    "tips": ["Study statistical tests", "Practice data analysis"],
                    "resources": LEARNING_RESOURCES["Scientific"]["intermediate"]
                })
            elif "control group" in text or "confounding variable" in text:
                topic = "Experimental Design"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "designing controlled experiments",
                    "tips": ["Identify variables", "Minimize bias"],
                    "resources": LEARNING_RESOURCES["Scientific"]["advanced"]
                })
            elif "literature review" in text or "citation style" in text:
                topic = "Academic Writing"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "writing and citing research",
                    "tips": ["Read academic papers", "Practice proper citation"],
                    "resources": LEARNING_RESOURCES["Scientific"]["basic"]
                })
            # Cybersecurity
            elif "firewall" in text or "phishing" in text or "https" in text or "two-factor" in text:
                topic = "Network Security"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "protecting networks and web applications",
                    "tips": ["Learn about firewalls", "Understand phishing tactics"],
                    "resources": LEARNING_RESOURCES["Cybersecurity"]["basic"]
                })
            elif "wireshark" in text or "packet sniffer" in text:
                topic = "Packet Analysis"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "analyzing network traffic",
                    "tips": ["Use Wireshark", "Study network protocols"],
                    "resources": LEARNING_RESOURCES["Cybersecurity"]["intermediate"]
                })
            elif "encryption" in text or "vpn" in text:
                topic = "Encryption and Privacy"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "securing data transmission",
                    "tips": ["Learn about AES", "Set up a VPN"],
                    "resources": LEARNING_RESOURCES["Cybersecurity"]["advanced"]
                })
            elif "zero-day" in text or "penetration testing" in text:
                topic = "Advanced Threats"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "identifying and mitigating advanced threats",
                    "tips": ["Study vulnerability research", "Practice pen testing"],
                    "resources": LEARNING_RESOURCES["Cybersecurity"]["advanced"]
                })
            # Environmental Engineering
            elif "wastewater" in text or "stormwater" in text:
                topic = "Water Management"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "managing water resources and treatment",
                    "tips": ["Study treatment processes", "Learn about runoff control"],
                    "resources": LEARNING_RESOURCES["Environmental Engineering"]["basic"]
                })
            elif "global warming" in text or "air pollution" in text:
                topic = "Climate Science"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "understanding environmental impacts",
                    "tips": ["Read about carbon footprints", "Study pollution control"],
                    "resources": LEARNING_RESOURCES["Environmental Engineering"]["intermediate"]
                })
            elif "renewable energy" in text:
                topic = "Energy Systems"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "implementing renewable energy solutions",
                    "tips": ["Learn about solar and wind", "Study energy storage"],
                    "resources": LEARNING_RESOURCES["Environmental Engineering"]["advanced"]
                })
            # Ethical Hacking
            elif "ethical hacking" in text or "vulnerability scanning" in text:
                topic = "Ethical Hacking Goals"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "understanding ethical hacking principles",
                    "tips": ["Study ethical guidelines", "Learn about legal implications"],
                    "resources": LEARNING_RESOURCES["Ethical Hacking"]["basic"]
                })
            elif "sql injection" in text or "brute force" in text:
                topic = "Attack Methods"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "identifying and preventing common attacks",
                    "tips": ["Learn about OWASP Top 10", "Practice secure coding"],
                    "resources": LEARNING_RESOURCES["Ethical Hacking"]["intermediate"]
                })
            elif "man-in-the-middle" in text or "social engineering" in text:
                topic = "Advanced Attacks"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "defending against sophisticated attack vectors",
                    "tips": ["Study attack simulations", "Learn mitigation techniques"],
                    "resources": LEARNING_RESOURCES["Ethical Hacking"]["advanced"]
                })
            # Urban Planning
            elif "urban planning" in text or "gis" in text:
                topic = "Planning Tools"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "using GIS and planning software",
                    "tips": ["Learn ArcGIS", "Practice spatial analysis"],
                    "resources": LEARNING_RESOURCES["Urban Planning"]["basic"]
                })
            elif "mixed-use" in text or "zoning" in text:
                topic = "Land Use"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "understanding land use regulations",
                    "tips": ["Study zoning laws", "Analyze case studies"],
                    "resources": LEARNING_RESOURCES["Urban Planning"]["intermediate"]
                })
            elif "transit-oriented" in text or "walkability" in text:
                topic = "Transportation Planning"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "designing sustainable urban transport",
                    "tips": ["Study urban design", "Plan transit routes"],
                    "resources": LEARNING_RESOURCES["Urban Planning"]["advanced"]
                })
            # Voice Acting
            elif "voice actor" in text or "diction" in text:
                topic = "Vocal Skills"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "improving vocal performance",
                    "tips": ["Practice enunciation", "Record and review performances"],
                    "resources": LEARNING_RESOURCES["Voice Acting"]["basic"]
                })
            elif "adr" in text or "demo reel" in text:
                topic = "Industry Knowledge"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "understanding voice acting industry terms",
                    "tips": ["Research industry standards", "Create a demo reel"],
                    "resources": LEARNING_RESOURCES["Voice Acting"]["intermediate"]
                })
            elif "convey emotion" in text or "pacing" in text:
                topic = "Performance Skills"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "delivering emotional and paced performances",
                    "tips": ["Practice script reading", "Work on timing"],
                    "resources": LEARNING_RESOURCES["Voice Acting"]["advanced"]
                })
            # Astronomy
            elif "light-year" in text or "supernova" in text:
                topic = "Basic Astronomy"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "understanding fundamental astronomy concepts",
                    "tips": ["Read introductory books", "Use astronomy apps"],
                    "resources": LEARNING_RESOURCES["Astronomy"]["basic"]
                })
            elif "doppler effect" in text or "redshift" in text:
                topic = "Observational Astronomy"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "interpreting astronomical observations",
                    "tips": ["Study spectroscopy", "Analyze real data"],
                    "resources": LEARNING_RESOURCES["Astronomy"]["intermediate"]
                })
            elif "black hole" in text or "kepler’s first law" in text:
                topic = "Advanced Astrophysics"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "grasping complex astronomical phenomena",
                    "tips": ["Study orbital mechanics", "Explore cosmology"],
                    "resources": LEARNING_RESOURCES["Astronomy"]["advanced"]
                })
            # Wildlife Conservation
            elif "wildlife conservation" in text or "endangered species" in text:
                topic = "Conservation Biology"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "understanding conservation principles",
                    "tips": ["Study ecology", "Volunteer with conservation groups"],
                    "resources": LEARNING_RESOURCES["Wildlife Conservation"]["basic"]
                })
            elif "habitat fragmentation" in text or "biodiversity hotspot" in text:
                topic = "Environmental Impact"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "assessing human impact on ecosystems",
                    "tips": ["Read about habitat loss", "Study conservation strategies"],
                    "resources": LEARNING_RESOURCES["Wildlife Conservation"]["intermediate"]
                })
            elif "keystone species" in text or "ecological data" in text:
                topic = "Ecosystem Analysis"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "analyzing ecological relationships",
                    "tips": ["Study food webs", "Practice data collection"],
                    "resources": LEARNING_RESOURCES["Wildlife Conservation"]["advanced"]
                })
            # Medicine
            elif "red blood cells" in text or "cpr" in text:
                topic = "Basic Physiology"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "understanding human body functions",
                    "tips": ["Study anatomy", "Practice first aid"],
                    "resources": LEARNING_RESOURCES["Medicine"]["basic"]
                })
            elif "hypoglycemia" in text or "ecg" in text:
                topic = "Clinical Knowledge"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "diagnosing and treating medical conditions",
                    "tips": ["Review medical textbooks", "Shadow healthcare professionals"],
                    "resources": LEARNING_RESOURCES["Medicine"]["intermediate"]
                })
            elif "differential diagnosis" in text or "antibiotic" in text:
                topic = "Advanced Diagnostics"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "performing complex medical assessments",
                    "tips": ["Practice case studies", "Learn pharmacology"],
                    "resources": LEARNING_RESOURCES["Medicine"]["advanced"]
                })
            # Education
            elif "formative assessment" in text or "scaffolding" in text:
                topic = "Teaching Strategies"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "implementing effective teaching methods",
                    "tips": ["Plan lessons", "Use diverse assessment tools"],
                    "resources": LEARNING_RESOURCES["Education"]["basic"]
                })
            elif "learning theory" in text:
                topic = "Educational Psychology"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "understanding how students learn",
                    "tips": ["Study cognitive development", "Apply learning theories"],
                    "resources": LEARNING_RESOURCES["Education"]["intermediate"]
                })
            elif "lesson plan" in text or "interactive quizzes" in text:
                topic = "Classroom Management"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "organizing and engaging classroom activities",
                    "tips": ["Develop lesson plans", "Use educational tech"],
                    "resources": LEARNING_RESOURCES["Education"]["advanced"]
                })
            # Law
            elif "source of law" in text or "habeas corpus" in text:
                topic = "Legal Fundamentals"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "understanding legal systems and terms",
                    "tips": ["Read legal texts", "Study case law"],
                    "resources": LEARNING_RESOURCES["Law"]["basic"]
                })
            elif "tort" in text or "cross-examination" in text:
                topic = "Civil and Criminal Law"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "applying legal principles in practice",
                    "tips": ["Mock trials", "Legal research"],
                    "resources": LEARNING_RESOURCES["Law"]["intermediate"]
                })
            elif "pro bono" in text:
                topic = "Legal Practice"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "understanding legal service delivery",
                    "tips": ["Study ethics", "Volunteer legal aid"],
                    "resources": LEARNING_RESOURCES["Law"]["advanced"]
                })
            # Mechanical Engineering
            elif "gear" in text or "cad" in text:
                topic = "Mechanical Design"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "designing mechanical systems",
                    "tips": ["Practice CAD software", "Study mechanical components"],
                    "resources": LEARNING_RESOURCES["Mechanical Engineering"]["basic"]
                })
            elif "stress" in text or "force, mass, acceleration" in text:
                topic = "Mechanics"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "applying principles of mechanics",
                    "tips": ["Solve physics problems", "Review Newton's laws"],
                    "resources": LEARNING_RESOURCES["Mechanical Engineering"]["intermediate"]
                })
            elif "bearing" in text:
                topic = "Friction and Wear"
                weaknesses[topic]["count"] += 1
                weaknesses[topic].update({
                    "description": "understanding mechanical friction",
                    "tips": ["Study tribology", "Analyze bearing designs"],
                    "resources": LEARNING_RESOURCES["Mechanical Engineering"]["advanced"]
                })

    # Filter significant weaknesses (more than 20% of wrong answers)
    significant_weaknesses = {
        area: data for area, data in weaknesses.items()
        if data["count"] > 0 and (data["count"] / total_wrong) > 0.2
    }
    return significant_weaknesses if significant_weaknesses else None

def calculate_match(score, weaknesses, field):
    recommendations = {"Basic": [], "Intermediate": [], "Advanced": []}
    weaknesses = weaknesses or {}
    if score < 40 or (weaknesses and len(weaknesses) > 2):
        recommendations["Basic"].extend(LEARNING_RESOURCES.get(field, {}).get("basic", []))
        for topic in weaknesses:
            recommendations["Basic"].extend(weaknesses[topic].get("resources", []))
    elif 40 <= score < 70 or (weaknesses and 1 <= len(weaknesses) <= 2):
        recommendations["Intermediate"].extend(LEARNING_RESOURCES.get(field, {}).get("intermediate", []))
        for topic in weaknesses:
            recommendations["Intermediate"].extend(weaknesses[topic].get("resources", []))
    else:  # score >= 70
        recommendations["Advanced"].extend(LEARNING_RESOURCES.get(field, {}).get("advanced", []))
        if not weaknesses and score >= 80:
            recommendations["Advanced"].append({"name": "Mastery Resources", "url": "#", "description": "Explore advanced topics"})
    return recommendations

@app.route('/submit_skill_gap', methods=['POST'])
@login_required
def submit_skill_gap():
    data = request.get_json()
    if not data or 'responses' not in data:
        return jsonify({'error': 'No data provided'}), 400

    session.setdefault('skill_gap_total', 0)
    session.setdefault('skill_gap_correct', 0)

    responses = data['responses']
    time_spent = data.get('time_spent', 0)
    current_question_index = data.get('current_question_index', 0)
    questions = session.get('skill_gap_questions', [])
    selected_field = session.get('selected_field', 'Software Development')

    if not questions or current_question_index >= len(questions):
        return jsonify({'error': 'Invalid session data or no more questions'}), 400

    current_response = responses[-1]
    question_id = current_response['questionId']
    
    try:
        answer = int(current_response['answer'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid answer format. Answer must be an integer.'}), 400

    question = next((q for q in questions if q['id'] == question_id), None)
    if not question:
        return jsonify({'error': 'Question not found'}), 400

    session['skill_gap_total'] += 1
    if answer == question.get('correct', -1):
        session['skill_gap_correct'] += 1

    session.modified = True

    if current_question_index + 1 >= len(questions):
        score = (session['skill_gap_correct'] / session['skill_gap_total']) * 100 if session['skill_gap_total'] > 0 else 0
        detailed_scores = {selected_field: score}
        
        # Identify weaknesses
        correct_count = session['skill_gap_correct']
        weaknesses = identify_weaknesses(questions, responses, correct_count)
        if weaknesses:
            session['weaknesses'] = weaknesses
        else:
            session['weaknesses'] = {}  # Ensure weaknesses is always a dict for template

        result = TestResult(
            user_id=current_user.id,
            test_type='skill_gap',
            score=score,
            time_spent=time_spent,
            details=json.dumps(detailed_scores)
        )
        current_user.skill_gap_scores = json.dumps(detailed_scores)
        db.session.add(result)
        db.session.commit()

        # Award badges and notifications
        if not Badge.query.filter_by(user_id=current_user.id, name="First Test Completed").first():
            badge = Badge(user_id=current_user.id, name="First Test Completed", description="Completed your first skill gap test!", icon="fas fa-trophy")
            db.session.add(badge)
        if score >= 80:
            if not Badge.query.filter_by(user_id=current_user.id, name="Skill Expert").first():
                badge = Badge(user_id=current_user.id, name="Skill Expert", description="Scored 80% or higher in skill gap test!", icon="fas fa-star")
                db.session.add(badge)

        notification = Notification(
            user_id=current_user.id,
            message=f"Skill Gap Test for {selected_field} completed! Score: {score:.1f}%",
            type="test_result"
        )
        db.session.add(notification)
        db.session.commit()

        completed_tests = session.get('completed_tests', [])
        if 'skill_gap' not in completed_tests:
            completed_tests.append('skill_gap')
            session['completed_tests'] = completed_tests

        test_results = session.get('test_results', {})
        test_results['skill_gap'] = {
            'score': score,
            'correct': session['skill_gap_correct'],
            'total': session['skill_gap_total'],
            'time_spent': time_spent,
            'detailed_scores': detailed_scores
        }
        session['test_results'] = test_results

        session.pop('skill_gap_questions', None)
        session.pop('skill_gap_correct', None)
        session.pop('skill_gap_total', None)

        return jsonify({'redirect': url_for('skill_gap_results')})

    next_question = questions[current_question_index + 1]
    return jsonify({'question': next_question, 'current_question_index': current_question_index + 1})

@app.route('/interest_test', methods=['GET'])
@login_required
def interest_test():
    selected_field = request.args.get('field', session.get('selected_field', None))
    if not selected_field:
        return render_template('assessments/interest_test.html', selected_field=None, questions=[], total_questions=0, completed_questions=0, current_question_index=0, initial_time=60)

    session['selected_field'] = selected_field
    questions = session.get('skill_gap_questions', [])
    if not questions or session.get('skill_gap_field') != selected_field:
        session.pop('skill_gap_questions', None)
        session.pop('skill_gap_correct', None)
        session.pop('skill_gap_total', None)
        session.pop('responses', None)  # Clear previous responses
        questions = generate_questions('skill_gap')
        if not questions:
            return redirect(url_for('dashboard'))
        session['skill_gap_field'] = selected_field

    current_question_index = int(request.args.get('q', 0))
    if current_question_index >= len(questions):
        return redirect(url_for('skill_gap_results'))
    question = questions[current_question_index]
    return render_template('assessments/interest_test.html',
                          selected_field=selected_field,
                          questions=[question],
                          total_questions=len(questions),
                          completed_questions=current_question_index,
                          current_question_index=current_question_index,
                          initial_time=question['time_limit'])

@app.route('/interest_test/next', methods=['POST'])
@login_required
def interest_test_next():
    data = request.get_json()
    if not data or 'responses' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    current_question_index = data.get('current_question_index', 0)
    responses = data['responses']
    time_spent = data.get('time_spent', 0)
    questions = session.get('skill_gap_questions', [])
    total_questions = 10

    if not questions or len(questions) < total_questions:
        questions = generate_questions('skill_gap')
        if not questions:
            return jsonify({'error': 'Not enough questions'}), 500
        session['skill_gap_questions'] = questions

    response = responses[-1]
    question_id = response['questionId']
    try:
        answer = int(response['answer'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid answer format'}), 400

    question = next((q for q in questions if q['id'] == question_id), None)
    if question:
        session['skill_gap_total'] = session.get('skill_gap_total', 0) + 1
        session['responses'] = session.get('responses', []) + [response]
        if answer == question.get('correct', -1):
            session['skill_gap_correct'] = session.get('skill_gap_correct', 0) + 1
    session.modified = True

    if current_question_index + 1 >= total_questions:
        skill_gap_total = session.get('skill_gap_total', 1)
        score = (session.get('skill_gap_correct', 0) / skill_gap_total) * 100 if skill_gap_total > 0 else 0
        weaknesses = identify_weaknesses(questions, session.get('responses', []), session.get('skill_gap_correct', 0))
        session['weaknesses'] = weaknesses or {}

        detailed_scores = {session.get('selected_field', 'Unknown'): score}
        result = TestResult(
            user_id=current_user.id,
            test_type='skill_gap',
            score=score,
            time_spent=time_spent,
            details=json.dumps(detailed_scores)
        )
        current_user.skill_gap_scores = json.dumps(detailed_scores)
        db.session.add(result)
        db.session.commit()

        if not Badge.query.filter_by(user_id=current_user.id, name="First Test Completed").first():
            badge = Badge(user_id=current_user.id, name="First Test Completed", description="Completed your first skill gap test!", icon="fas fa-trophy")
            db.session.add(badge)
        if score >= 80:
            if not Badge.query.filter_by(user_id=current_user.id, name="Skill Expert").first():
                badge = Badge(user_id=current_user.id, name="Skill Expert", description="Scored 80% or higher in skill gap test!", icon="fas fa-star")
                db.session.add(badge)

        notification = Notification(
            user_id=current_user.id,
            message=f"Skill Gap Test for {session.get('selected_field', 'Unknown')} completed! Score: {score:.1f}%",
            type="test_result"
        )
        db.session.add(notification)
        db.session.commit()

        completed_tests = session.get('completed_tests', [])
        if 'skill_gap' not in completed_tests:
            completed_tests.append('skill_gap')
            session['completed_tests'] = completed_tests

        session.pop('skill_gap_questions', None)
        session.pop('skill_gap_correct', None)
        session.pop('skill_gap_total', None)
        session.pop('responses', None)

        return jsonify({'redirect': url_for('skill_gap_results')})

    next_question = questions[current_question_index + 1]
    return jsonify({
        'question': next_question,
        'current_question_index': current_question_index + 1,
        'initial_time': next_question['time_limit']
    })

@app.route('/skill_gap_results')
@login_required
def skill_gap_results():
    score = (session.get('skill_gap_correct', 0) / session.get('skill_gap_total', 1)) * 100 if session.get('skill_gap_total', 1) > 0 else 0
    weaknesses = session.get('weaknesses', {})
    field = session.get('selected_field', 'Unknown')
    match_recommendations = calculate_match(score, weaknesses, field)

    # Determine feedback message based on score
    feedback_message = ""
    if score >= 80:
        feedback_message = f"Congratulations! You answered all questions correctly, indicating complete mastery in {field}. This reflects your exceptional proficiency across all assessed areas."
    elif 40 <= score < 70:
        feedback_message = f"Your skill level in {field} is {score:.0f}%. You have a moderate skill gap. Consider reviewing the recommended resources to improve."
    else:  # score < 40
        feedback_message = f"Your skill level in {field} is {score:.0f}%. You have a significant skill gap. We recommend starting with the Basic tier resources and focusing on the identified weaknesses."

    return render_template('skill_gap_results.html', 
                          score=score, 
                          weaknesses=weaknesses, 
                          field=field, 
                          match_recommendations=match_recommendations,
                          feedback_message=feedback_message,
                          total_questions=10,
                          correct_answers=session.get('skill_gap_correct', 0),
                          incorrect_answers=session.get('skill_gap_total', 1) - session.get('skill_gap_correct', 0))

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

@app.route('/aptitude_results')
@login_required
def aptitude_results():
    test_results = session.get('test_results', {})
    score_data = test_results.get('aptitude', None)
    has_personality = 'personality' in session.get('completed_tests', [])
    has_aptitude = 'aptitude' in session.get('completed_tests', [])

    if not score_data:
        # Fallback to latest TestResult if session data is missing
        latest_test = TestResult.query.filter_by(
            user_id=current_user.id,
            test_type='aptitude'
        ).order_by(TestResult.completed_at.desc()).first()
        if not latest_test:
            flash('No aptitude test results found. Please complete the test first.', 'warning')
            return redirect(url_for('dashboard'))
        
        detailed_scores = json.loads(latest_test.details) if latest_test.details else {}
        score_data = {
            'test_type': 'aptitude',
            'score': latest_test.score,
            'correct': int((latest_test.score / 100) * 20),  # Adjusted calculation
            'total': 20,
            'time_spent': latest_test.time_spent or 0,
            'detailed_scores': detailed_scores
        }

    # Ensure test_type is set
    score_data['test_type'] = 'aptitude'
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()

    return render_template(
        'results.html',
        score_data=score_data,
        has_personality=has_personality,
        has_aptitude=has_aptitude,
        active_page='results',
        notifications=notifications
    )

@app.route('/personality_results')
@login_required
def personality_results():
    # Get test results
    latest_test = TestResult.query.filter_by(
        user_id=current_user.id, 
        test_type='personality'
    ).order_by(TestResult.completed_at.desc()).first()
    
    if not latest_test:
        flash('No personality test results found.', 'warning')
        return redirect(url_for('dashboard'))

    scores = json.loads(latest_test.details)
    
    # Ensure all traits exist in scores
    for trait in ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']:
        scores.setdefault(trait, 0)

    # Calculate dominant trait
    dominant_trait = max(scores, key=lambda k: scores[k])

    # Scientific trait data
    trait_data = {
    'Openness': {
        'color': '#6366f1',
        'icon': 'lightbulb',
        'explanation': 'Reflects imagination, curiosity, and appreciation for new experiences',
        'brain_correlation': 'Dorsolateral prefrontal cortex activity',
        'life_impact': 'Predicts creative problem-solving abilities',
        'behavioral_impacts': [
            'Seeks novel experiences',
            'Engages in creative pursuits',
            'Appreciates art and beauty',
            'Explores new ideas and concepts',
            'Enjoys abstract thinking'
        ]
    },
    'Conscientiousness': {
        'color': '#10b981',
        'icon': 'clock',
        'explanation': 'Indicates self-discipline, goal-directed behavior, and reliability',
        'brain_correlation': 'Anterior cingulate cortex activation',
        'life_impact': 'Strong predictor of academic and career success',
        'behavioral_impacts': [
            'Plans and organizes tasks effectively',
            'Meets deadlines consistently',
            'Pays attention to detail',
            'Follows through on commitments',
            'Maintains a structured routine'
        ]
    },
    'Extraversion': {
        'color': '#f59e0b',
        'icon': 'people',
        'explanation': 'Relates to sociability, assertiveness, and positive emotionality',
        'brain_correlation': 'Ventral striatum responsiveness',
        'life_impact': 'Associated with leadership potential',
        'behavioral_impacts': [
            'Initiates conversations easily',
            'Thrives in social settings',
            'Expresses emotions outwardly',
            'Seeks stimulation and excitement',
            'Enjoys being the center of attention'
        ]
    },
    'Agreeableness': {
        'color': '#ef4444',
        'icon': 'heart',
        'explanation': 'Reflects compassion, cooperation, and social harmony',
        'brain_correlation': 'Mirror neuron system activity',
        'life_impact': 'Key factor in team collaboration',
        'behavioral_impacts': [
            'Shows empathy towards others',
            'Cooperates well in teams',
            'Avoids conflicts',
            'Helps others in need',
            'Values harmonious relationships'
        ]
    },
    'Neuroticism': {
        'color': '#8b5cf6',
        'icon': 'activity',
        'explanation': 'Indicates emotional sensitivity and stress reactivity',
        'brain_correlation': 'Amygdala hyperactivation',
        'life_impact': 'Affects emotional resilience',
        'behavioral_impacts': [
            'Experiences mood swings',
            'Worries about future events',
            'Sensitive to stress',
            'Tends to overthink situations',
            'May have difficulty relaxing'
        ]
    }
}

    # Dominant trait details
    dominant_data = trait_data.get(dominant_trait, trait_data['Conscientiousness'])

    return render_template(
        'personality_results.html',
        scores=scores,
        dominant_trait=dominant_trait,
        dominant_data=dominant_data,
        trait_data=trait_data,
        trait_names={
            'Openness': 'Openness to Experience',
            'Conscientiousness': 'Conscientiousness',
            'Extraversion': 'Extraversion',
            'Agreeableness': 'Agreeableness',
            'Neuroticism': 'Neuroticism'
        },
        has_aptitude=TestResult.query.filter_by(
            user_id=current_user.id, 
            test_type='aptitude'
        ).count() > 0,
        notifications=Notification.query.filter_by(
            user_id=current_user.id, 
            is_read=False
        ).order_by(Notification.date.desc()).limit(5).all()
    )
    
def calculate_career_fit(user_scores, career_requirements, test_types_completed):
    fit_reasons = []
    total_match_score = 0
    max_possible_score = 0

    # Aptitude fit
    if 'aptitude' in test_types_completed and user_scores['aptitude']:
        for apt, user_score in user_scores['aptitude'].items():
            required_score = career_requirements['aptitude'].get(apt, 0)
            if required_score > 0:  # Only consider aptitudes required by the career
                max_possible_score += 100  # Each aptitude contributes up to 100 points
                match_percentage = min(user_score / required_score, 1.0) * 100
                total_match_score += match_percentage
                if user_score >= required_score * 0.8:  # 80% threshold
                    fit_reasons.append(f"High {apt} aptitude ({user_score}%)")

    # Personality fit
    if 'personality' in test_types_completed and user_scores['personality']:
        for trait, user_score in user_scores['personality'].items():
            required_score = career_requirements['personality'].get(trait, 0)
            if required_score > 0:  # Only consider traits required by the career
                max_possible_score += 100
                match_percentage = min(user_score / required_score, 1.0) * 100 if required_score > 50 else (100 - user_score) / (100 - required_score) * 100
                total_match_score += match_percentage
                if user_score >= required_score * 0.8 and required_score > 50:
                    fit_reasons.append(f"High {trait} personality ({user_score}%)")
                elif user_score <= required_score * 1.2 and required_score < 50:
                    fit_reasons.append(f"Low {trait} personality ({user_score}%)")

    # Skill fit (optional)
    if 'skill_gap' in test_types_completed and user_scores['skill_gap']:
        required_skill = career_requirements['skills']['required']
        user_skill = user_scores['skill_gap'].get('score', 0)
        max_possible_score += 100
        match_percentage = min(user_skill / required_skill, 1.0) * 100
        total_match_score += match_percentage
        if user_skill >= required_skill * 0.8:
            fit_reasons.append(f"Strong skill proficiency ({user_skill}%)")

    # Calculate overall fit level
    overall_score = (total_match_score / max_possible_score * 100) if max_possible_score > 0 else 0
    if overall_score >= 75:
        fit_level = "Highly Suitable"
    elif overall_score >= 50:
        fit_level = "Moderately Suitable"
    else:
        fit_level = "Not Assessed"
        fit_reasons = ["Complete more tests for a better assessment"] if not fit_reasons else fit_reasons

    return {"fit_level": fit_level, "score": overall_score, "reasons": fit_reasons}

def get_precise_career_matches(user_scores, region, show_global):
    """Get top 5 career matches based on user scores and O*NET data."""
    matches = []
    onet_api = ONetAPI()
    for career_name, career_data in CAREER_MAPPING.items():
        soc_code = CAREERS.get(career_name, "15-1252.00")
        onet_summary = onet_api.get_occupation_summary(soc_code) or {}
        onet_abilities = {a['name']: {'level': 50, 'importance': 3} for a in onet_api.get_abilities(soc_code)} or {}
        onet_work_styles = {ws['name']: {'level': 50, 'importance': 3} for ws in onet_api.get_work_styles(soc_code)} or {}

        # Ensure required keys exist with defaults
        for ability in APTITUDE_TO_ONET.values():
            if ability not in onet_abilities:
                onet_abilities[ability] = {'level': 50, 'importance': 3}
        for style in PERSONALITY_TO_ONET.values():
            if style not in onet_work_styles:
                onet_work_styles[style] = {'level': 50, 'importance': 3}

        # Construct career_data_for_match for calculate_match
        career_data_for_match = {
            'personality': {k: v['level'] for k, v in onet_work_styles.items()},
            'aptitude': {k: v['level'] for k, v in onet_abilities.items()},
            'skills': {'required': onet_summary.get('skill_level', 70)}
        }
        match_score = calculate_career_match(user_scores, career_data_for_match)  # Replace compute_career_match

        # Fetch additional O*NET details
        onet_skills = onet_api.get_skills(soc_code)
        onet_education = onet_api.get_education(soc_code)

        onet_details = {
            'title': onet_summary.get('title', career_name),
            'median_wage': onet_summary.get('wages', {}).get('median', 100000),
            'currency': 'USD' if show_global else 'INR' if region == 'IN' else 'USD',
            'growth_rate': onet_summary.get('outlook', {}).get('growth_rate', 0),
            'skills': [skill.get('name', 'N/A') for skill in onet_skills],
            'education': onet_education.get('level_required', [])
        }
        if region == 'IN' and not show_global and onet_details['median_wage']:
            onet_details['median_wage'] *= 83  # USD to INR approximation

        matches.append({
            'name': career_name,
            'description': onet_summary.get('description', career_data.get('description', '')),
            'match_score': match_score,
            'onet_details': onet_details,
            'resources': get_recommendations(career_name, match_score)
        })

    matches.sort(key=lambda x: x['match_score'], reverse=True)
    return matches[:5]

@app.route('/career_match', methods=['GET', 'POST'])
@login_required
def career_match():
    form = CareerMatchForm()
    region = get_region_from_pin(current_user.pin_code) if current_user.pin_code else 'US'
    show_global = form.global_opportunities.data if form.validate_on_submit() else False

    # Fetch user test scores and completed tests
    completed_tests = session.get('completed_tests', [t.test_type for t in TestResult.query.filter_by(user_id=current_user.id).all()])
    app.logger.debug(f"Completed tests: {completed_tests}")
    
    try:
        aptitude_scores = json.loads(current_user.aptitude_scores) if current_user.aptitude_scores else {}
        personality_scores = json.loads(current_user.personality_scores) if current_user.personality_scores else {}
        skill_gap_scores = json.loads(current_user.skill_gap_scores) if current_user.skill_gap_scores else {}
    except json.JSONDecodeError as e:
        app.logger.error(f"JSON decode error: {e}")
        aptitude_scores, personality_scores, skill_gap_scores = {}, {}, {}

    app.logger.debug(f"User scores - Aptitude: {aptitude_scores}, Personality: {personality_scores}, Skill Gap: {skill_gap_scores}")

    user_scores = {
        'aptitude': aptitude_scores,
        'personality': personality_scores,
        'skill_gap': skill_gap_scores if skill_gap_scores else {'score': 0}
    }

    matches = []
    onet_api = ONetAPI()

    for career_name, career_data in CAREER_MAPPING.items():
        soc_code = CAREERS.get(career_name, "15-1252.00")
        onet_summary = onet_api.get_occupation_summary(soc_code) or {}
        fit = calculate_career_match(user_scores, career_data, completed_tests)
        app.logger.debug(f"Career: {career_name}, SOC: {soc_code}, Fit: {fit}")

        # Relaxed threshold: Include "Not Assessed" for debugging
        if fit['fit_level'] in ['Highly Suitable', 'Moderately Suitable', 'Not Assessed']:
            median_wage = onet_summary.get('wages', {}).get('median', 100000)
            growth_rate = onet_summary.get('outlook', {}).get('growth_rate', 0)
            currency = 'USD' if show_global or region != 'IN' else 'INR'
            if region == 'IN' and not show_global and median_wage:
                median_wage = convert_salary(median_wage, region, 'USD')

            matches.append({
                'name': career_name,
                'description': onet_summary.get('description', career_data.get('description', '')),
                'fit_level': fit['fit_level'],
                'fit_reasons': fit['reasons'],
                'score': fit['score'],
                'median_wage': median_wage,
                'currency': currency,
                'growth_rate': growth_rate
            })

    matches.sort(key=lambda x: x['score'], reverse=True)
    top_matches = matches[:5]

    if not top_matches:
        app.logger.warning("No matches found. Check user scores and fit calculation.")
    
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
    return render_template('career_match.html', matches=top_matches, form=form, completed_tests=completed_tests, active_page='career_match', notifications=notifications)

def get_recommendations(missing_skills):
    """Get real courses from EdX API based on missing skills"""
    edx_api = EdxAPI()
    courses = []
    for skill in missing_skills[:2]:  # Get courses for top 2 missing skills
        courses += edx_api.search_courses(subject=skill, limit=2)
    return courses[:3]  # Return max 3 courses

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
   
@app.route('/full_analysis')
@login_required
def full_analysis():
    analysis = {
        'aptitude': {
            'completed_at': current_user.aptitude_completed_at,
            'score': sum(current_user.aptitude_scores.values()) / len(current_user.aptitude_scores) if current_user.aptitude_scores else 0,
            'details': current_user.aptitude_scores or {}
        },
        'personality': {
            'completed_at': current_user.personality_completed_at,
            'score': sum(current_user.personality_scores.values()) / len(current_user.personality_scores) if current_user.personality_scores else 0,
            'details': current_user.personality_scores or {}
        },
        'skill_gap': {
            'completed_at': current_user.skill_gap_completed_at,
            'score': current_user.skill_gap_scores.get('score', 0) if current_user.skill_gap_scores else 0,
            'details': current_user.skill_gap_scores or {}
        }
    }
    region = get_region_from_pin(current_user.pin_code) if current_user.pin_code else 'US'
    user_scores = {
        'aptitude': current_user.aptitude_scores or {},
        'personality': current_user.personality_scores or {},
        'skill_gap': current_user.skill_gap_scores or {}
    }
    matches = get_precise_career_matches(user_scores, region, False)
    return render_template('full_analysis.html', analysis=analysis, matches=matches)
    
@app.route('/career_path')
@login_required
def career_path():
    results = TestResult.query.filter_by(user_id=current_user.id).all()
    career_scores = defaultdict(float)
    for result in results:
        details = json.loads(result.details) if result.details else {}
        if result.test_type == 'skill_gap':
            for career, data in CAREER_MAPPING.items():
                for skill in data['skills']:
                    if skill in details:
                        career_scores[career] += details[skill] * 0.5
    data = {
        'labels': list(career_scores.keys()),
        'scores': [career_scores[c] for c in career_scores]
    }
    return render_template('career_path.html', data=data, active_page='career_path')

@app.route('/career_details/<career_name>')
@login_required
def career_details(career_name):
    onet_api = ONetAPI()
    soc_code = CAREERS.get(career_name, "15-1252.00")
    career_data = onet_api.get_occupation_summary(soc_code) or {'title': career_name, 'description': 'No description available', 'wages': {'median': 50000}, 'outlook': {'growth_rate': 0}}
    skills = onet_api.get_skills(soc_code) or []
    education = onet_api.get_education(soc_code) or {'level_required': []}

    # Fetch courses based on skills
    edx_api = EdxAPI()
    courses = edx_api.search_courses(subject=career_name, limit=3)

    onet_data = {
        'description': career_data.get('description', 'No description available'),
        'salary': f"USD {career_data.get('wages', {}).get('median', 50000):,}",
        'job_outlook': f"{career_data.get('outlook', {}).get('growth_rate', 0)}% growth",
        'courses': [{'name': c['title'], 'url': f"https://edx.org/course/{c['title'].replace(' ', '-')}", 'level': c['degree_level']} for c in courses]
    }

    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
    return render_template('career_details.html', career_name=career_name, career_data=onet_data, active_page='career_details', notifications=notifications)
    
@app.route('/resources')
@login_required
def resources():
    """
    Render the vintage‑styled newsletter page.
    We simply pass the raw resource dicts (with date as string).
    """
    career_path = session.get('selected_field', 'Software Development')
    if career_path not in CAREER_MAPPING:
        career_path = 'Software Development'

    # Get the list of dicts; each dict has keys: title, description, category, url, date, image_url?
    resources = LEARNING_RESOURCES.get(career_path, [])

    # Fetch up to 5 unread notifications
    notifications = (
        Notification.query
        .filter_by(user_id=current_user.id, is_read=False)
        .order_by(Notification.date.desc())
        .limit(5)
        .all()
    )

    return render_template(
        'std.html',
        resources=resources,
        notifications=notifications
    )

@app.route('/api/resources')
@login_required
def api_resources():
    """
    Return JSON list of resources (date stays as string) for client‑side JS.
    """
    career_path = session.get('selected_field', 'Software Development')
    if career_path not in CAREER_MAPPING:
        career_path = 'Software Development'

    raw = LEARNING_RESOURCES.get(career_path, [])
    # Sort by date string descending (ISO YYYY-MM-DD sorts lexically)
    resources = sorted(raw, key=lambda r: r.get('date',''), reverse=True)
    return jsonify(resources)

@app.route('/api/institutes')
@login_required
def api_institutes():
    country = request.args.get('country', 'India')
    name    = request.args.get('name', '')
    params  = {'country': country}
    if name:
        params['name'] = name

    try:
        resp = requests.get(
            'https://universities.hipolabs.com/search',
            params=params,
            timeout=5
        )
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        app.logger.error(f"Error fetching institutes: {e}")
        return jsonify({'error': 'Could not load institutes'}), 502

    return jsonify(data)

   
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        if form.password.data:
            current_user.password = generate_password_hash(form.password.data)
        if form.profile_image.data and allowed_file(form.profile_image.data.filename):
            filename = secure_filename(f"profile_{current_user.id}.{form.profile_image.data.filename.rsplit('.', 1)[1].lower()}")
            image = Image.open(form.profile_image.data)
            image = image.resize((150, 150), Image.LANCZOS)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            current_user.profile_image = f"uploads/{filename}"
            current_user.pin_code = request.form.get('pin_code')
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    form.email.data = current_user.email
    tests = TestResult.query.filter_by(user_id=current_user.id).order_by(TestResult.completed_at.desc()).all()
    badges = Badge.query.filter_by(user_id=current_user.id).order_by(Badge.date_earned.desc()).all()
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
    return render_template('profile.html', user=current_user, form=form, tests=tests, badges=badges,
                          active_page='profile', notifications=notifications)
    
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

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = Message(subject=f"Contact from {form.name.data}", recipients=['abc@gmail.com'],
                      body=f"Name: {form.name.data}\nEmail: {form.email.data}\nMessage: {form.message.data}")
        try:
            mail.send(msg)
            flash('Message sent successfully!', 'success')
            return redirect(url_for('contact'))
        except Exception as e:
            flash(f'Failed to send message: {str(e)}', 'danger')
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all() if current_user.is_authenticated else []
    return render_template('contact.html', form=form, active_page='contact', notifications=notifications)

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

@app.route('/faq')
def faq():
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all() if current_user.is_authenticated else []
    return render_template('faq.html', active_page='faq', notifications=notifications)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        print("Form data received:", request.form)
        
        # Theme Preferences
        if 'theme' in request.form:
            theme = request.form['theme']
            if theme in ['light', 'dark']:
                current_user.theme = theme
                db.session.commit()
                flash('Theme updated successfully!', 'success')
            else:
                flash('Invalid theme selection.', 'danger')
        
        # Notification Preferences
        elif 'notify_test_reminders' in request.form:
            current_user.notify_test_reminders = 'notify_test_reminders' in request.form
            current_user.notify_badge_earned = 'notify_badge_earned' in request.form
            current_user.notify_progress_updates = 'notify_progress_updates' in request.form
            db.session.commit()
            flash('Notification preferences updated successfully!', 'success')
        
        # Email Preferences
        elif 'email_notifications' in request.form:
            current_user.email_notifications = 'email_notifications' in request.form
            current_user.email_newsletters = 'email_newsletters' in request.form
            db.session.commit()
            flash('Email preferences updated successfully!', 'success')
        
        # Profile Visibility
        elif 'profile_visibility' in request.form:
            visibility = request.form['profile_visibility']
            if visibility in ['public', 'private']:
                current_user.profile_visibility = visibility
                db.session.commit()
                flash('Profile visibility updated successfully!', 'success')
            else:
                flash('Invalid visibility selection.', 'danger')
        
        # Preferred Test Categories
        elif 'pref_aptitude' in request.form or 'pref_personality' in request.form or 'pref_skill_gap' in request.form:
            categories = []
            if 'pref_aptitude' in request.form:
                categories.append('aptitude')
            if 'pref_personality' in request.form:
                categories.append('personality')
            if 'pref_skill_gap' in request.form:
                categories.append('skill_gap')
            current_user.preferred_test_categories = categories
            db.session.commit()
            flash('Preferred test categories updated successfully!', 'success')
        
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
        
        # Reset Roadmap (existing functionality)
        elif 'reset_roadmap' in request.form:
            TestResult.query.filter_by(user_id=current_user.id).delete()
            db.session.commit()
            flash('Roadmap progress reset successfully!', 'success')
        
        # Delete Account
        elif 'delete_account' in request.form:
            confirm_username = request.form.get('confirm_username')
            if confirm_username != current_user.username:
                flash('Username does not match. Account deletion aborted.', 'danger')
            else:
                # Delete all user-related data
                TestResult.query.filter_by(user_id=current_user.id).delete()
                Badge.query.filter_by(user_id=current_user.id).delete()
                Notification.query.filter_by(user_id=current_user.id).delete()
                db.session.delete(current_user)
                db.session.commit()
                logout_user()
                flash('Your account has been deleted.', 'info')
                return redirect(url_for('index'))
        
        return redirect(url_for('settings'))
    
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()
    return render_template('settings.html', user=current_user, active_page='settings', notifications=notifications)

@app.route('/progress_tracking')
@login_required
def progress_tracking():
    # Fetch test history from database
    test_history = TestResult.query.filter_by(user_id=current_user.id).order_by(TestResult.completed_at.asc()).all()
    
    # Streak calculation function
    def calculate_streak(test_dates):
        if not test_dates:
            return 0
        
        current_streak = 1
        sorted_dates = sorted(test_dates, reverse=True)
        
        for i in range(1, len(sorted_dates)):
            if (sorted_dates[i-1] - sorted_dates[i]).days == 1:
                current_streak += 1
            else:
                break
        return current_streak

    # Calculate current streak
    test_dates = [test.completed_at.date() for test in test_history if test.completed_at]
    current_streak = calculate_streak(test_dates)

    # Handle empty test history
    total_tests = len(test_history)
    if total_tests == 0:
        flash('No tests taken yet. Take a test to track your progress!', 'info')
        return redirect(url_for('test'))

    # Calculate average scores
    test_types = ['sample', 'aptitude', 'personality']
    avg_scores = {}
    for test_type in test_types:
        type_tests = [test for test in test_history if test.test_type == test_type]
        max_score = 9 if test_type == 'sample' else (5 if test_type == 'personality' else 10)
        avg_scores[test_type] = (sum(test.score for test in type_tests) / (len(type_tests) * max_score)) * 100 if type_tests else 0

    # Prepare progress data (CORRECTED SECTION)
    progress_data = {
        'labels': [test.completed_at.strftime('%Y-%m-%d') for test in test_history],
        'scores': [
            (test.score / (
                9 if test.test_type == 'sample' 
                else (5 if test.test_type == 'personality' else 10)
            )) * 100 
            for test in test_history
        ],
        'types': [test.test_type for test in test_history]
    }

    # Define career tasks
    career_path = session.get('selected_field', 'Software Development')
    if career_path not in CAREER_MAPPING:
        career_path = 'Software Development'

    tasks = [
        {"name": "Complete Initial Assessment", "completed": any(t.test_type == 'aptitude' for t in test_history)},
        {"name": "Enroll in Courses", "completed": False},
        {"name": "Practice Skills", "completed": any(t.test_type == 'skill_gap' and career_path in json.loads(t.details) for t in test_history)},
        {"name": "Build Portfolio", "completed": False},
        {"name": "Apply for Jobs", "completed": False}
    ]

    # Calculate progress
    completed_tasks = sum(1 for task in tasks if task["completed"])
    progress_percentage = (completed_tasks / len(tasks)) * 100 if tasks else 0

    # Fetch notifications
    notifications = Notification.query.filter_by(
        user_id=current_user.id, 
        is_read=False
    ).order_by(Notification.date.desc()).limit(5).all()

    return render_template(
        'progress_tracking.html',
        user=current_user,
        test_history=test_history,
        avg_scores=avg_scores,
        progress_data=progress_data,
        tasks=tasks,
        progress_percentage=progress_percentage,
        current_streak=current_streak,
        total_tests=total_tests,
        active_page='progress_tracking',
        notifications=notifications
    )

@app.route('/roadmap')
@login_required
def roadmap():
    # Fetch test history for the user, ordered by completion date
    test_history = TestResult.query.filter_by(user_id=current_user.id).order_by(TestResult.completed_at.asc()).all()
    total_tests = len(test_history)

    # Determine the user's career path from the session, default to 'Software Development'
    career_path = session.get('selected_field', 'Software Development')
    if career_path not in CAREER_MAPPING:
        career_path = 'Software Development'

    # Define career goals and milestones for different career paths
    career_roadmaps = {
        "Software Development": {
            "career_goal": "Senior Software Engineer",
            "milestones": [
                {
                    "title": "Completed Aptitude Test",
                    "description": "Assessed core skills",
                    "details": "Evaluated logical reasoning, problem-solving, and basic technical knowledge.",
                    "date": next((t.completed_at for t in test_history if t.test_type == 'aptitude'), None),  # Keep timezone-aware
                    "type": "test",
                    "completed": any(t.test_type == 'aptitude' for t in test_history),
                    "progress": 100 if any(t.test_type == 'aptitude' for t in test_history) else 0
                },
                {
                    "title": "Skill Gap Assessment",
                    "description": "Evaluated coding skills",
                    "details": "Assessed proficiency in Python, JavaScript, and software development fundamentals.",
                    "date": next((t.completed_at for t in test_history if t.test_type == 'skill_gap' and 'Software Development' in json.loads(t.details)), None),  # Keep timezone-aware
                    "type": "test",
                    "completed": any(t.test_type == 'skill_gap' and 'Software Development' in json.loads(t.details) for t in test_history),
                    "progress": 100 if any(t.test_type == 'skill_gap' and 'Software Development' in json.loads(t.details) for t in test_history) else 0
                },
                {
                    "title": "First Project",
                    "description": "Built a basic application",
                    "details": "Developed a to-do list app using HTML, CSS, and JavaScript.",
                    "date": datetime(2025, 3, 10, tzinfo=timezone.utc),  # Make timezone-aware
                    "type": "project",
                    "completed": False,
                    "progress": 50
                },
                {
                    "title": "Portfolio Creation",
                    "description": "Showcased projects",
                    "details": "Created a portfolio website with 3 projects, hosted on GitHub Pages.",
                    "date": datetime(2025, 3, 15, tzinfo=timezone.utc),  # Make timezone-aware
                    "type": "project",
                    "completed": False,
                    "progress": 30
                },
                {
                    "title": "Job Application",
                    "description": "Applied to entry-level roles",
                    "details": "Submitted applications to 5 software development positions.",
                    "date": datetime(2025, 3, 20, tzinfo=timezone.utc),  # Make timezone-aware
                    "type": "job",
                    "completed": False,
                    "progress": 20
                }
            ]
        },
        "Data Science": {
            "career_goal": "Lead Data Scientist",
            "milestones": [
                {
                    "title": "Completed Aptitude Test",
                    "description": "Assessed analytical skills",
                    "details": "Evaluated mathematical reasoning, statistics, and problem-solving abilities.",
                    "date": next((t.completed_at for t in test_history if t.test_type == 'aptitude'), None),  # Keep timezone-aware
                    "type": "test",
                    "completed": any(t.test_type == 'aptitude' for t in test_history),
                    "progress": 100 if any(t.test_type == 'aptitude' for t in test_history) else 0
                },
                {
                    "title": "Skill Gap Assessment",
                    "description": "Evaluated data skills",
                    "details": "Assessed proficiency in Python, R, and data analysis techniques.",
                    "date": next((t.completed_at for t in test_history if t.test_type == 'skill_gap' and 'Data Science' in json.loads(t.details)), None),  # Keep timezone-aware
                    "type": "test",
                    "completed": any(t.test_type == 'skill_gap' and 'Data Science' in json.loads(t.details) for t in test_history),
                    "progress": 100 if any(t.test_type == 'skill_gap' and 'Data Science' in json.loads(t.details) for t in test_history) else 0
                },
                {
                    "title": "Statistics Mastery",
                    "description": "Completed stats course",
                    "details": "Finished an online course on advanced statistics and probability.",
                    "date": datetime(2025, 3, 12, tzinfo=timezone.utc),  # Make timezone-aware
                    "type": "course",
                    "completed": False,
                    "progress": 70
                },
                {
                    "title": "Data Project",
                    "description": "Analyzed a dataset",
                    "details": "Performed exploratory data analysis on a public dataset using Pandas and Matplotlib.",
                    "date": datetime(2025, 3, 18, tzinfo=timezone.utc),  # Make timezone-aware
                    "type": "project",
                    "completed": False,
                    "progress": 40
                },
                {
                    "title": "Research Publication",
                    "description": "Published findings",
                    "details": "Published a research paper on machine learning applications in a journal.",
                    "date": datetime(2025, 3, 25, tzinfo=timezone.utc),  # Make timezone-aware
                    "type": "publication",
                    "completed": False,
                    "progress": 10
                }
            ]
        }
    }

    # Get roadmap data for the user's career path, default to Software Development if not found
    roadmap_data = career_roadmaps.get(career_path, career_roadmaps["Software Development"])
    milestones = roadmap_data["milestones"]

    # Fetch unread notifications for the user, limited to the 5 most recent
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.date.desc()).limit(5).all()

    # Get the current date as a timezone-aware datetime
    current_date = datetime.now(timezone.utc)

    # Render the roadmap template with the necessary data
    return render_template('roadmap.html',
                          user=current_user,
                          career_goal=roadmap_data["career_goal"],
                          milestones=milestones,
                          career_path=career_path,
                          current_date=current_date,
                          animations_enabled=current_user.animations_enabled,
                          active_page='roadmap',
                          notifications=notifications)

@app.route('/resume_builder', methods=['GET', 'POST'])
@login_required
def resume_builder():
    if request.method == 'POST':
        try:
            resume_data = {
                'template': request.form.get('template', 'modern'),
                'personal_info': {
                    'name': request.form.get('name', '').strip(),
                    'email': request.form.get('email', '').strip(),
                    'phone': request.form.get('phone', '').strip(),
                    'linkedin': request.form.get('linkedin', '').strip(),
                },
                'summary': request.form.get('summary', '').strip(),
                'education': [],
                'experience': [],
                'skills': json.loads(request.form.get('skills', '[]'))
            }

            # Handle photo upload
            photo_file = request.files.get('photo')
            if photo_file and photo_file.filename:
                filename = secure_filename(f'resume_photo_{current_user.id}_{photo_file.filename}')
                photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                os.makedirs(os.path.dirname(photo_path), exist_ok=True)
                photo_file.save(photo_path)
                resume_data['photo'] = url_for('static', filename=f'uploads/{filename}')

            # Process education
            education = request.form.getlist('education[]')
            institutions = request.form.getlist('institution[]')
            dates = request.form.getlist('education_date[]')
            for deg, inst, date in zip(education, institutions, dates):
                if deg.strip() and inst.strip():
                    resume_data['education'].append({
                        'degree': deg.strip(),
                        'institution': inst.strip(),
                        'date': date.strip()
                    })

            # Process experience (optional)
            positions = request.form.getlist('position[]')
            companies = request.form.getlist('company[]')
            descriptions = request.form.getlist('description[]')
            exp_dates = request.form.getlist('experience_date[]')
            for pos, comp, desc, date in zip(positions, companies, descriptions, exp_dates):
                if any([pos.strip(), comp.strip(), desc.strip()]):
                    resume_data['experience'].append({
                        'position': pos.strip(),
                        'company': comp.strip(),
                        'description': desc.strip(),
                        'date': date.strip()
                    })

            # Save to database
            resume = Resume.query.filter_by(user_id=current_user.id).first()
            if resume:
                resume.resume_data = resume_data
                resume.updated_at = datetime.now(pytz.utc)
            else:
                resume = Resume(user_id=current_user.id, resume_data=resume_data)
                db.session.add(resume)
            db.session.commit()

            return jsonify({'success': True, 'resume_id': resume.id})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    # GET request
    resume = Resume.query.filter_by(user_id=current_user.id).first()
    resume_data = resume.resume_data if resume else {}
    return render_template('resume.html', resume=resume_data)

@app.route('/api/career-suggestions')
def career_suggestions():
    query = request.args.get('skills', '').lower()
    all_skills = [
        "Python", "JavaScript", "Java", "C++", "SQL", "HTML", "CSS",
        "Project Management", "Data Analysis", "Machine Learning",
        "Cloud Computing", "Cybersecurity", "Graphic Design", "Marketing",
        "Leadership", "Communication", "Problem Solving", "Teamwork"
    ]
    suggestions = [skill for skill in all_skills if query in skill.lower()]
    return jsonify(suggestions[:5])

@app.route('/get-template-html')
def get_template_html():
    template_name = request.args.get('template', 'modern')
    template_file = f'resume_{template_name}.html'
    try:
        with open(os.path.join(app.template_folder, template_file), 'r') as f:
            return f.read()
    except FileNotFoundError:
        return render_template('resume_modern.html')  # Fallback

@app.route('/export-resume/<int:resume_id>')
@login_required
def export_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    template_name = resume.resume_data.get('template', 'modern')
    
    # Render template with CSS
    html_content = render_template(f'resume_{template_name}.html', resume=resume.resume_data)
    
    # Include base CSS
    base_css = Path(app.static_folder) / 'css' / 'resume.css'
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'user-style-sheet': str(base_css),
        'encoding': 'UTF-8'
    }
    
    pdf = pdfkit.from_string(html_content, False, options=options)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={current_user.username}_resume.pdf'
    return response

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
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5001)