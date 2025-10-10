import unittest
import sys
import os
import json

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, User, SOSIncident

class SOSFlowTestCase(unittest.TestCase):
    def setUp(self):
        self.app, self.socketio = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        # Create test client
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            
            # Create test users
            user = User(email='testuser@example.com', display_name='Test User', role='user')
            user.set_password('password123')
            
            authority = User(email='testauthority@example.com', display_name='Test Authority', role='authority')
            authority.set_password('password123')
            
            db.session.add(user)
            db.session.add(authority)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_sos_incident_creation(self):
        with self.app.app_context():
            # Create a new SOS incident
            incident = SOSIncident(
                user_id=1,
                status='active'
            )
            incident.set_start_coords({'lat': 40.7128, 'lon': -74.0060})
            incident.set_latest_coords({'lat': 40.7128, 'lon': -74.0060})
            
            db.session.add(incident)
            db.session.commit()
            
            # Verify incident was created
            retrieved_incident = SOSIncident.query.get(incident.id)
            self.assertIsNotNone(retrieved_incident)
            self.assertEqual(retrieved_incident.user_id, 1)
            self.assertEqual(retrieved_incident.status, 'active')
            
            # Verify coordinates
            start_coords = retrieved_incident.get_start_coords()
            latest_coords = retrieved_incident.get_latest_coords()
            self.assertEqual(start_coords['lat'], 40.7128)
            self.assertEqual(start_coords['lon'], -74.0060)
            self.assertEqual(latest_coords['lat'], 40.7128)
            self.assertEqual(latest_coords['lon'], -74.0060)

    def test_password_hashing(self):
        with self.app.app_context():
            user = User.query.filter_by(email='testuser@example.com').first()
            self.assertTrue(user.check_password('password123'))
            self.assertFalse(user.check_password('wrongpassword'))

    def test_user_role_assignment(self):
        with self.app.app_context():
            user = User.query.filter_by(email='testuser@example.com').first()
            authority = User.query.filter_by(email='testauthority@example.com').first()
            
            self.assertEqual(user.role, 'user')
            self.assertEqual(authority.role, 'authority')

if __name__ == '__main__':
    unittest.main()