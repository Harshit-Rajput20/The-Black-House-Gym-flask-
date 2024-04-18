# app/signup.py
from flask import Blueprint, render_template, request, redirect, flash, url_for ,current_app
from models.user import User, db
# from utils.email import init_mail
from utils.mail import send_verification_email
from itsdangerous import URLSafeTimedSerializer
import datetime

signup_blueprint = Blueprint('signup', __name__)
serializer = URLSafeTimedSerializer('your_secret_key')

@signup_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():   
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['Confpassword']

        # Check if the passwords match
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(request.url)  # Redirect back to the signup page with error message

        # Check if the email is already registered
        if User.query.filter_by(email=email).first():
            flash('Email already exists. Please use a different email.', 'error')
            return redirect(request.url)  # Redirect back to the signup page with error message
        
        # Generate verification token
        verification_token = serializer.dumps(email, salt='email-verification')

        # Send verification email
        verification_link = url_for('signup.verify_email', token=verification_token, _external=True)
        # send_verification_email(email, verification_link)
        current_app.logger.info(verification_link)
        firstname = request.form['firstname']
        middlename = request.form['middlename']
        lastname = request.form['lastname']
        phone_number = request.form['phone_number']
        
        new_user = User(firstname=firstname, middlename=middlename, lastname=lastname, email=email, phone_number=phone_number, signup_date=datetime.datetime.utcnow())
        # Create a new user object
        current_app.logger.info(new_user)
 
        # Create a new user object and set password
        # new_user = User(email=email)
        new_user.set_password(password)

        # Add the user to the database with email unverified
        new_user.email_verified = False
        db.session.add(new_user)
        db.session.commit()

        flash('A verification email has been sent to your email address. Please verify your email to complete the signup process.', 'success')
        return redirect(url_for('login.login'))  # Redirect to the login page after successful signup

    # If GET request, render the signup form
    return render_template('signup.html')


@signup_blueprint.route('/verify_email/<token>')
def verify_email(token):
    try:
        email = serializer.loads(token, salt='email-verification', max_age=3600)  # Token expires after 1 hour
        user = User.query.filter_by(email=email).first()

        if user:
            user.email_verified = True
            db.session.commit()
            flash('Email verification successful. You can now login.', 'success')
        else:
            flash('Invalid verification link.', 'error')

    except Exception as e:
        flash('Invalid or expired verification link.', 'error')

    return redirect('/login')  # Redirect to the login page after email verification
