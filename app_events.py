from flask import request, current_app as app
from flask_socketio import emit
import threading
import time

# We'll import socketio in a different way to avoid circular imports
from app import db
from models import User, SOSIncident, SMSLog

# Store active incidents and their rooms
active_incidents = {}
user_connections = {}

def simulate_sms(incident_id, contacts, message, socketio):
    """Simulate sending SMS messages to emergency contacts"""
    with app.app_context():
        for contact in contacts:
            # Create SMS log entry
            sms_log = SMSLog(
                incident_id=incident_id,
                contact=contact.get('name', 'Unknown') + f" ({contact.get('phone', 'N/A')})",
                message=message,
                status='sent'
            )
            db.session.add(sms_log)
        
        db.session.commit()
        
        # Emit simulated SMS event to all connected clients
        for contact in contacts:
            socketio.emit('sms:simulated', {
                'incident_id': incident_id,
                'contact': contact.get('name', 'Unknown') + f" ({contact.get('phone', 'N/A')})",
                'message': message,
                'status': 'sent'
            })

def register_events(socketio):
    """Register all SocketIO events"""
    
    @socketio.on('connect')
    def handle_connect():
        print(f'Client connected: {request.sid}')
        
    @socketio.on('disconnect')
    def handle_disconnect():
        print(f'Client disconnected: {request.sid}')
        # Clean up user connections
        if request.sid in user_connections:
            del user_connections[request.sid]

    @socketio.on('sos:init')
    def handle_sos_init(data):
        """Handle SOS initialization from user"""
        # In a real app, we would authenticate the user
        # For this demo, we'll assume the user is authenticated
        
        # Create new incident
        incident = SOSIncident(
            user_id=1,  # Demo user ID
            status='active'
        )
        incident.set_start_coords(data['coords'])
        incident.set_latest_coords(data['coords'])
        
        db.session.add(incident)
        db.session.commit()
        
        # Store incident info
        active_incidents[incident.id] = {
            'user_sid': request.sid,
            'authority_sids': []
        }
        
        # Store user connection
        user_connections[request.sid] = {
            'user_id': 1,
            'incident_id': incident.id,
            'role': 'user'
        }
        
        # Emit acknowledgment to user
        emit('user:ack', {
            'incident_id': incident.id,
            'status': 'initialized'
        })
        
        # Notify all authorities about new incident
        socketio.emit('authority:new_incident', {
            'incident_id': incident.id,
            'user_id': 1,
            'coords': data['coords'],
            'timestamp': incident.timestamp.isoformat()
        })
        
        # Simulate SMS sending to emergency contacts
        # In a real app, this would come from the user's profile
        emergency_contacts = [
            {"name": "Emergency Contact 1", "phone": "+1234567890"},
            {"name": "Emergency Contact 2", "phone": "+1234567891"}
        ]
        
        message = f"EMERGENCY: User needs help! Location: {data['coords']['lat']}, {data['coords']['lon']}"
        
        # Simulate SMS sending with a delay
        threading.Thread(target=simulate_sms, args=(incident.id, emergency_contacts, message, socketio)).start()

    @socketio.on('sos:frame')
    def handle_sos_frame(data):
        """Handle video frame from user"""
        incident_id = data['incident_id']
        
        # Validate incident exists and is active
        incident = SOSIncident.query.get(incident_id)
        if not incident or incident.status != 'active':
            return
        
        # Forward frame to all authorities
        socketio.emit('authority:frame', {
            'incident_id': incident_id,
            'frame_base64_chunk': data['frame_base64_chunk'],
            'seq': data['seq']
        })

    @socketio.on('sos:end')
    def handle_sos_end(data):
        """Handle SOS end signal from user"""
        incident_id = data['incident_id']
        
        # Update incident status
        incident = SOSIncident.query.get(incident_id)
        if incident:
            incident.status = 'resolved'
            db.session.commit()
            
            # Notify authorities
            socketio.emit('authority:incident_resolved', {
                'incident_id': incident_id
            })
            
            # Clean up active incidents
            if incident_id in active_incidents:
                del active_incidents[incident_id]