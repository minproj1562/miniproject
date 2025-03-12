import os

SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key')
SQLALCHEMY_DATABASE_URI = 'sqlite:///careers.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = True