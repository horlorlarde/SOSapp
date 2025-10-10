from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager
from config import Config
from models import db
import eventlet

# Apply eventlet monkey patching for async support
eventlet.monkey_patch()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')
    
    # Setup login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    from models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from auth.routes import auth_bp
    from user.routes import user_bp
    from authority.routes import authority_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(authority_bp)
    
    # Import and register SocketIO events after app creation to avoid circular imports
    with app.app_context():
        from app_events import register_events
        register_events(socketio)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app, socketio

if __name__ == '__main__':
    # Create app instance
    app, socketio = create_app()
    
    # Run the app with SocketIO on port 8000 to avoid conflicts
    socketio.run(app, host='0.0.0.0', port=8000, debug=True)