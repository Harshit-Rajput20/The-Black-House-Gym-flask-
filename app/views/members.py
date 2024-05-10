# members/views.py
from flask import Blueprint, render_template, request, redirect, url_for
from models.database import db
from models.user import Member
from models.user import Membership
from datetime import datetime, timedelta

members_bp = Blueprint('members', __name__, url_prefix='/members')

@members_bp.route('/', methods=['GET'])
def list_members():
    members = Member.query.all()
    return render_template('members.html', members=members)

@members_bp.route('/add', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        new_member = Member(name=name, email=email, password=password)
        db.session.add(new_member)
        db.session.commit()
        return redirect(url_for('members.list_members'))
    return render_template('add_member.html')

@members_bp.route('/<int:member_id>/memberships', methods=['GET'])
def view_memberships(member_id):
    member = Member.query.get(member_id)
    memberships = Membership.query.filter_by(member_id=member_id, active=True).all()
    return render_template('view_memberships.html', member=member, memberships=memberships)

@members_bp.route('/<int:member_id>/memberships/add', methods=['GET', 'POST'])
def add_membership(member_id):
    if request.method == 'POST':
        duration = int(request.form['duration'])
        start_date = datetime.utcfromtimestamp()
        
        # Deactivate existing memberships
        existing_memberships = Membership.query.filter_by(member_id=member_id, active=True).all()
        for membership in existing_memberships:
            membership.active = False
        db.session.commit()
        
        # Add new membership
        end_date = start_date + timedelta(days=duration * 30)  # Assuming 30 days per month
        new_membership = Membership(member_id=member_id, start_date=start_date, duration=duration)
        db.session.add(new_membership)
        db.session.commit()
        
        return redirect(url_for('members.view_memberships', member_id=member_id))
    return render_template('add_membership.html')
