# SOS Emergency Response System

A local-first Flask application that implements a user-facing SOS system and an Authority dashboard with real-time video streaming and geolocation tracking.

## Features

- **User Registration/Login** with role-based authentication (user vs authority)
- **User Dashboard** with large SOS button for emergency alerts
- **Authority Dashboard** for monitoring and responding to emergencies
- **Real-time Communication** using WebSocket/Flask-SocketIO
- **Live Video Streaming** from user's camera to authorities
- **Geolocation Tracking** via browser Geolocation API
- **Simulated SMS Alerts** to emergency contacts
- **Multi-device LAN Testing** - accessible from other devices on the same network

## Architecture

```
SOS Emergency Response System
├── Flask Web Application (Backend)
│   ├── Flask-SocketIO for real-time communication
│   ├── SQLAlchemy with SQLite for data storage
│   ├── Flask-Login for authentication
│   └── Eventlet for async support
├── Client-Side (Frontend)
│   ├── HTML5/CSS3 for UI
│   ├── Vanilla JavaScript for interactivity
│   ├── WebSocket for real-time communication
│   ├── getUserMedia API for camera access
│   └── Geolocation API for location tracking
└── Simulation Modules
    ├── SMS Simulation (no external services)
    └── Coordinate Display (no external maps)
```

## Tech Stack

- **Backend**: Python 3.10+, Flask, Flask-SocketIO, SQLAlchemy
- **Frontend**: HTML5, CSS3, Vanilla JavaScript, Bootstrap 5
- **Database**: SQLite (via SQLAlchemy)
- **Real-time Communication**: WebSocket (Socket.IO)
- **Authentication**: Flask-Login
- **Camera Access**: Browser `getUserMedia` API
- **Geolocation**: Browser Geolocation API

## Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd sos_emergency_response
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Seed the database with demo users:
   ```bash
   python scripts/seed_demo_users.py
   ```

## Running the Application

### Method 1: Using the run scripts

On Linux/Mac:
```bash
./run.sh
```

On Windows:
```bash
run.bat
```

### Method 2: Direct execution

```bash
python app.py
```

The application will start on `http://localhost:8000` and will be accessible from other devices on the same network at `http://YOUR_LOCAL_IP:8000`.

## PyCharm Setup

1. Open the project in PyCharm
2. Go to **File → Settings → Project → Python Interpreter**
3. Create a new virtual environment or select an existing one
4. Install requirements: `pip install -r requirements.txt`
5. Right-click on `app.py` and select **Run 'app'**
6. In the Run Configuration:
   - Set **Host** to `0.0.0.0`
   - Set **Port** to `8000`
   - Enable **Run browser** if desired

## Demo Accounts

After seeding the database, you can use these accounts:

**User Account:**
- Email: `user@example.com`
- Password: `password123`

**Authority Account:**
- Email: `authority@example.com`
- Password: `password123`

## Testing the Application

### Automated Tests

Run the test suite:
```bash
python -m unittest tests/test_auth.py
python -m unittest tests/test_sos_flow.py
```

### Manual Testing (Demo Script)

1. **Start the Application:**
   - Run the application on one device (the host)
   - Note the host's local IP address:
     - Windows: `ipconfig`
     - Mac/Linux: `ifconfig`

2. **Device 1 (User):**
   - Open a browser and navigate to `http://HOST_IP:8000`
   - Login with the user account
   - Go to the User Dashboard
   - Click the SOS button
   - Grant camera and location permissions when prompted

3. **Device 2 (Authority):**
   - Open a browser and navigate to `http://HOST_IP:8000`
   - Login with the authority account
   - Go to the Authority Dashboard
   - You should see the new incident appear in real-time
   - The live video feed should start streaming
   - Location coordinates should update in real-time
   - Simulated SMS logs should appear

4. **End the SOS:**
   - On the user device, click the "Stop SOS" button
   - The authority dashboard should show the incident as resolved

## Security Notes

- Passwords are securely hashed using Werkzeug's security utilities
- Session management is handled by Flask-Login
- Socket connections are not currently authenticated (would be added in production)
- In a production environment, HTTPS should be implemented

## Limitations and Future Improvements

1. **Video Streaming:**
   - Current implementation sends base64-encoded JPEG frames over WebSocket
   - For production, consider WebRTC for better performance
   - Frame rate and quality can be adjusted based on network conditions

2. **Geolocation:**
   - Uses browser Geolocation API which requires HTTPS in production
   - Accuracy depends on device capabilities

3. **Authentication:**
   - Socket connections should be authenticated in production
   - Add token-based authentication for API endpoints

4. **Database:**
   - SQLite is used for simplicity; PostgreSQL or MySQL for production
   - Add database migrations for schema changes

5. **SMS Integration:**
   - Currently simulated; integrate with Twilio or similar for production

6. **Mapping:**
   - Currently displays coordinates textually; integrate with Mapbox or similar for visual maps

## Edge Cases Handled

- Denied camera/location permissions with graceful UI feedback
- Intermittent connectivity with frame queuing and dropping
- Server-side rate limiting for incoming frames
- Privacy considerations (no permanent video storage)

## File Structure

```
sos_app/
├── app.py                 # Flask app entrypoint
├── config.py              # Application configuration
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── run.sh                 # Linux/Mac run script
├── run.bat                # Windows run script
├── README.md              # This file
├── auth/
│   ├── routes.py          # Authentication routes
│   └── forms.py           # Authentication forms
├── user/
│   └── routes.py          # User dashboard routes
├── authority/
│   └── routes.py          # Authority dashboard routes
├── templates/
│   ├── base.html          # Base template
│   ├── index.html         # Landing page
│   ├── register.html      # Registration page
│   ├── login.html         # Login page
│   ├── user_dashboard.html # User dashboard
│   └── authority_dashboard.html # Authority dashboard
├── static/
│   └── css/
│       └── style.css      # Custom styles
├── tests/
│   ├── test_auth.py       # Authentication tests
│   └── test_sos_flow.py   # SOS flow tests
└── scripts/
    └── seed_demo_users.py # Demo user seeding script
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.