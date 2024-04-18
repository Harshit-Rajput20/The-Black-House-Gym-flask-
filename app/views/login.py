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

def generate_session_token():
    """Generate a random session token."""
    return secrets.token_hex(16)  # Generate a 32-character hexadecimal string

MAX_ATTEMPTS = 5

def create_session(user):
    """Create a session token for the user and store it in the database."""
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        session_token = generate_session_token()
        expiration = datetime.utcnow() + timedelta(hours=1)  # Set session expiration time to 1 hour from now
        
        # Check if the generated session token already exists
        existing_session = Session.query.filter_by(sid=session_token).first()
        
        if not existing_session:
            # If session token is unique, create a new session
            new_session = Session(sid=session_token, user_id=str(user.id), expiration=expiration)
            try:
                db.session.add(new_session)
                db.session.commit()
                return session_token
            except IntegrityError:
                # Handle potential race condition where another process/thread inserts a session with the same token
                db.session.rollback()
                attempts += 1
                continue
        attempts += 1

    # If maximum attempts reached, return an error
    raise ValueError("Failed to generate a unique session token after {} attempts.".format(MAX_ATTEMPTS))



@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user:
            if user.email_verified:
                if user.check_password(password):
                    session_token = create_session(user)
                    session['session_token'] = session_token  # Store session token in session
                    
                    return redirect('/')  # Redirect to the homepage after successful login
                else:
                    return ({'error': 'Invalid email or password'}), 401
            else:
                return ({'error': 'Email not verified. Please check your email to verify your account.'}), 403
        else:
            return ({'error': 'Invalid email or password'}), 401
            

    return render_template('index.html')


@login_blueprint.route('/logout', methods=['GET'])
def logout():
    # Check if session token exists in the session
    if 'session_token' in session:
        # Retrieve the session token from the session
        session_token = session['session_token']

        # Query the database for the session with the given token
        session_data = Session.query.filter_by(sid=session_token).first()

        # If session data exists, delete the session from the database
        if session_data:
            db.session.delete(session_data)
            db.session.commit()

        # Clear the session
        session.clear()

        flash('You have been logged out successfully.', 'success')
    else:
        flash('You are already logged out.', 'info')

    return redirect('/')  # Redirect to the homepage after logout
