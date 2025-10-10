from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user

user_bp = Blueprint('user', __name__)

@user_bp.route('/user/dashboard')
@login_required
def dashboard():
    if current_user.role != 'user':
        return redirect(url_for('auth.index'))
    
    return render_template('user_dashboard.html')