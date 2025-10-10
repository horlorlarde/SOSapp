import sys
import os

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, User

def seed_demo_users():
    app, _ = create_app()
    
    with app.app_context():
        # Check if users already exist
        user_count = User.query.count()
        if user_count > 0:
            print(f"Database already contains {user_count} users. Skipping seed.")
            return
        
        # Create demo user
        user = User(
            email='user@example.com',
            display_name='Demo User',
            role='user'
        )
        user.set_password('password123')
        user.set_emergency_contacts([
            {"name": "Emergency Contact 1", "phone": "+1234567890"},
            {"name": "Emergency Contact 2", "phone": "+1234567891"}
        ])
        
        # Create demo authority
        authority = User(
            email='authority@example.com',
            display_name='Demo Authority',
            role='authority'
        )
        authority.set_password('password123')
        
        # Add to database
        db.session.add(user)
        db.session.add(authority)
        db.session.commit()
        
        print("Demo users created successfully!")
        print("User login:")
        print("  Email: user@example.com")
        print("  Password: password123")
        print("Authority login:")
        print("  Email: authority@example.com")
        print("  Password: password123")

if __name__ == '__main__':
    seed_demo_users()