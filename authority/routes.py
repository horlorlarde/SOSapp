from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import SOSIncident

authority_bp = Blueprint('authority', __name__)

@authority_bp.route('/authority/dashboard')
@login_required
def dashboard():
    if current_user.role != 'authority':
        return redirect(url_for('auth.index'))
    
    # Get all incidents for display
    incidents = SOSIncident.query.order_by(SOSIncident.timestamp.desc()).all()
    
    return render_template('authority_dashboard.html', incidents=incidents)