import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-123')
SQLALCHEMY_DATABASE_URI = 'sqlite:///careers.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = True