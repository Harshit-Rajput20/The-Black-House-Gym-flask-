from flask import Blueprint, render_template, request, redirect, flash, url_for, current_app
from models.package import PackageSignupTable
from datetime import datetime
from models.user import User, db
from dateutil import parser
from utils.mail import send_verification_email
from utils.mailtwo import send_fee_due_email
 
package_bp = Blueprint('package', __name__)

@package_bp.route('/package', methods=['GET', 'POST'])
def packagesignup():
    if request.method == 'POST':
        # Get user data from the form
        print("inside pacage signup")
        packagetype = int(request.form['packagetype'])
        date = parser.parse(request.form['date'])
        email = request.form['email']

        # Check if the user exists in the database
        user = User.query.filter_by(email=email).first()

        if user:
            print("database commited1")
            # Create a new PackageSignupTable object
            new_package_signup = PackageSignupTable(packagetype=packagetype, date=date, email=email)
            print("database commited2")
            # Add the new object to the database session
            db.session.add(new_package_signup)
            print("database commited3")
           
            # Commit changes to the database
            db.session.commit()
            print("database commited4")

            send_fee_due_email(email, packagetype)

           

            # Redirect to a success page or any other page
            return redirect(url_for('package.success'))
        else:
            # User is not in the database, show a message or redirect to sign-in page
            flash('You need to sign in first.')
            return redirect(url_for('signup.signup'))  # Change 'auth.signin' to your actual sign-in route

    # If it's a GET request, just render the signup form
    return render_template('package.html')

@package_bp.route('/success')
def success():
    return "Your package has been selected successfully."
