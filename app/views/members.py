# members/views.py
from flask import Blueprint, render_template, request, redirect, url_for
from models.database import db
from models.user import Member
from models.user import Membership
from datetime import datetime, timedelta
from flask import abort

members_bp = Blueprint('members', __name__, url_prefix='/members')

@members_bp.route('/', methods=['GET'])
def list_members():
    members = Member.query.all()
    return render_template('members.html', members=members)

# members/views.py
@members_bp.route('/add', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']  # Retrieve address from the form data
        new_member = Member(name=name, email=email, password=password, address=address)
        db.session.add(new_member)
        db.session.commit()
        return redirect(url_for('members.list_members'))
    return render_template('add_member.html')


@members_bp.route('/<int:member_id>/memberships', methods=['GET'])
def view_memberships(member_id):
    try:
        member = Member.query.get_or_404(member_id)
        memberships = Membership.query.filter_by(member_id=member_id).all()
        return render_template('view_memberships.html', member=member, memberships=memberships)
    except Exception as e:
        return render_template('error.html', message=str(e))



@members_bp.route('/<int:member_id>/memberships/add', methods=['GET', 'POST'])
def add_membership(member_id):
    member = Member.query.get(member_id)

    if not member:
        # Handle the case where member_id does not exist
        return render_template('error.html', message="Member not found")

    # Get the end date of the last active membership, if any
    last_membership = Membership.query.filter_by(member_id=member_id, active=True).order_by(Membership.end_date.desc()).first()
    last_membership_end_date = last_membership.end_date if last_membership else None

    if request.method == 'POST':
        duration = int(request.form['duration'])
        start_date_str = request.form['start_date']

        # Convert start_date_str to datetime object
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')

        # Check if the start date is before the end date of the last active membership, if any
        if last_membership and start_date < last_membership.end_date:
            return render_template('error.html', message="Start date must be on or after the end date of the last active membership")

        # Calculate end date for the new membership
        end_date = start_date + timedelta(days=duration * 30)  # Assuming 30 days per month

        # Add new membership
        new_membership = Membership(
            member_id=member_id,
            membership_type="Standard",  # Assuming a standard membership type
            start_date=start_date,
            end_date=end_date,
            duration=duration,
            active=True
        )
        db.session.add(new_membership)

        try:
            db.session.commit()
            # Log the membership purchase
            #logging .info(f"Membership purchased for member {member_id}. Duration: {duration} months.")
            return render_template('success.html', message="Membership added successfully")
        except Exception as e:
            # Rollback changes if an error occurs
            db.session.rollback()
            #logging .error(f"Error adding membership for member {member_id}: {str(e)}")
            return render_template('error.html', message="An error occurred while adding membership")

    return render_template('add_membership.html', member=member, last_membership_end_date=last_membership_end_date)
