# app/login.py

from flask import Blueprint, render_template, request, redirect, session, flash, g ,jsonify
from models.user import User
from models.sessions import Session
from datetime import datetime, timedelta
from models.database import db
import secrets  # For generating random session tokens
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, render_template, request, redirect, flash, url_for ,current_app
from models.user import User, db
# from utils.email import init_mail
from utils.mail import send_verification_email
from itsdangerous import URLSafeTimedSerializer
import datetime

login_blueprint = Blueprint('login', __name__)
@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            # Login successful
            # You can add session handling here if you want to keep the user logged in
            return redirect(url_for('index'))  # Redirect to dashboard page after successful login
        else:
            # Login failed
            error = 'Invalid email or password. Please try again.'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

# Sample dashboard route
@login_blueprint.route('/index')
def dashboard():
    return 'Welcome to the dashboard!'
 