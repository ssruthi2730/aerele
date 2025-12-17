import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///event_scheduler.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'event_scheduler.db')
