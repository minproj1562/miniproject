# config.py
import os

SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance/careers.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = True
