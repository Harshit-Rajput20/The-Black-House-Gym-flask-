# signup_bp.py
from flask import Blueprint, request, redirect, url_for, render_template
from datetime import datetime
from models.database import db
from models.user import User
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, flash, url_for ,current_app
from models.user import User, db
# from utils.email import init_mail
from utils.mail import send_verification_email
from itsdangerous import URLSafeTimedSerializer
import datetime

# Create a blueprint for the signup functionality
signup_bp = Blueprint('signup_bp', __name__)

@signup_bp.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Retrieve form data
        firstname = request.form['firstname']
        middlename = request.form['middlename']
        lastname = request.form['lastname']
        email = request.form['email']
        phone_number = request.form['phone_number']
        password = request.form['password']
        
        # Create a new user object
        new_user = User(firstname=firstname, middlename=middlename, lastname=lastname, email=email, phone_number=phone_number, signup_date=datetime.utcnow())
        
        # Set the password for the new user
        new_user.set_password(password)
        
        # Add the new user to the database session
        db.session.add(new_user)
        
        # Commit the changes to the database
        db.session.commit()
        
        # Redirect to the index page after successful signup
        return redirect(url_for('index'))
    
    # Render the signup.html template for GET requests
    return render_template('signup.html')
