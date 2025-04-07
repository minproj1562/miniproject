import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize a minimal app for database setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///career_analytics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Import models (ensure this doesn't cause circular imports)
from app import User, TestResult  # Adjust the import path if necessary

with app.app_context():
    db.create_all()
    print("Database tables created!")