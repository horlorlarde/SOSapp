from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from models import db, User
from auth.forms import RegistrationForm, LoginForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'user':
            return redirect(url_for('user.dashboard'))
        elif current_user.role == 'authority':
            return redirect(url_for('authority.dashboard'))
    return render_template('index.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email already registered.')
            return render_template('register.html', form=form)
        
        user = User(
            email=form.email.data,
            display_name=form.display_name.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        
        # Set default emergency contacts for users
        if form.role.data == 'user':
            user.set_emergency_contacts([
                {"name": "Emergency Contact 1", "phone": "+1234567890"},
                {"name": "Emergency Contact 2", "phone": "+1234567891"}
            ])
        
        db.session.add(user)
        db.session.commit()
        
        flash('Congratulations, you are now registered!')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return render_template('login.html', form=form)
        
        login_user(user)
        next_page = request.args.get('next')
        
        if not next_page:
            if user.role == 'user':
                next_page = url_for('user.dashboard')
            elif user.role == 'authority':
                next_page = url_for('authority.dashboard')
        
        return redirect(next_page)
    
    return render_template('login.html', form=form)

@auth_bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('auth.index'))