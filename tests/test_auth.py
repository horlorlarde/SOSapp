import unittest
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app, self.socketio = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
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

    def test_user_registration(self):
        response = self.client.post('/register', data={
            'email': 'newuser@example.com',
            'display_name': 'New User',
            'password': 'password123',
            'password2': 'password123',
            'role': 'user'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Congratulations, you are now registered!', response.data)

    def test_user_login(self):
        response = self.client.post('/login', data={
            'email': 'testuser@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User Dashboard', response.data)

    def test_authority_login(self):
        response = self.client.post('/login', data={
            'email': 'testauthority@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Authority Dashboard', response.data)

    def test_user_dashboard_access(self):
        # Login first
        self.client.post('/login', data={
            'email': 'testuser@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        # Access user dashboard
        response = self.client.get('/user/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User Dashboard', response.data)

    def test_authority_dashboard_access(self):
        # Login first
        self.client.post('/login', data={
            'email': 'testauthority@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        # Access authority dashboard
        response = self.client.get('/authority/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Authority Dashboard', response.data)

if __name__ == '__main__':
    unittest.main()