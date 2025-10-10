import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-for-sos-app'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///sos_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SOCKETIO_LOGGER = True
    ENGINEIO_LOGGER = True