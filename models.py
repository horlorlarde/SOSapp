from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'user' or 'authority'
    display_name = db.Column(db.String(100), nullable=True)
    emergency_contacts = db.Column(db.Text, nullable=True)  # JSON string
    last_known_coords = db.Column(db.Text, nullable=True)  # JSON string {lat, lon}
    active_session_token = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def set_emergency_contacts(self, contacts):
        self.emergency_contacts = json.dumps(contacts)
    
    def get_emergency_contacts(self):
        if self.emergency_contacts:
            return json.loads(self.emergency_contacts)
        return []
    
    def set_last_known_coords(self, coords):
        self.last_known_coords = json.dumps(coords)
    
    def get_last_known_coords(self):
        if self.last_known_coords:
            return json.loads(self.last_known_coords)
        return None
    
    def __repr__(self):
        return f'<User {self.email} ({self.role})>'

class SOSIncident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')  # 'active', 'resolved'
    start_coords = db.Column(db.Text, nullable=True)  # JSON string {lat, lon}
    latest_coords = db.Column(db.Text, nullable=True)  # JSON string {lat, lon}
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('incidents', lazy=True))
    
    def set_start_coords(self, coords):
        self.start_coords = json.dumps(coords)
    
    def get_start_coords(self):
        if self.start_coords:
            return json.loads(self.start_coords)
        return None
    
    def set_latest_coords(self, coords):
        self.latest_coords = json.dumps(coords)
    
    def get_latest_coords(self):
        if self.latest_coords:
            return json.loads(self.latest_coords)
        return None
    
    def __repr__(self):
        return f'<SOSIncident {self.id} by User {self.user_id}>'

class SMSLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey('sos_incident.id'), nullable=False)
    contact = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='simulated')  # 'simulated', 'queued', 'sent'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    incident = db.relationship('SOSIncident', backref=db.backref('sms_logs', lazy=True))
    
    def __repr__(self):
        return f'<SMSLog {self.id} for Incident {self.incident_id}>'