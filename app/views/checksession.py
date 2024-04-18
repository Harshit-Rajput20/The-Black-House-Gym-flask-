from models.sessions import Session
from models.user import User
from models.user import AdminRole  # Assuming you have a model for admin roles
from datetime import datetime
from flask import session
from flask import Blueprint, render_template, request, redirect, flash, url_for ,current_app
from models.user import User, db
# from utils.email import init_mail
from utils.mail import send_verification_email
from itsdangerous import URLSafeTimedSerializer
import datetime

def check_session():
    """Retrieve session token from session and perform actions based on its validity."""
    session_token = session.get('session_token')

    if session_token:
        # Retrieve session from the database
        session_data = Session.query.filter_by(sid=session_token).first()

        if session_data:
            # Check if session has expired
            if session_data.expiration > datetime.utcnow():
                # Session is valid, retrieve user details from the database
                user_id = session_data.user_id
                user = User.query.get(user_id)

                if user:
                    # Check if user is an admin and get admin rights
                    admin_rights = None
                    if user.is_admin:
                        # User is a super admin
                        
                        admin_role = AdminRole.query.get(user.admin_role_id)
                        if admin_role:
                            admin_rights = {
                                'can_access_backup': admin_role.can_access_backup,
                                'can_edit_posts': admin_role.can_edit_posts,
                                'can_edit_courses': admin_role.can_edit_courses,
                                'can_upload_pdfs': admin_role.can_upload_pdfs,
                                'can_manage_admins': admin_role.can_manage_admins
                            }
                        else:
                            admin_rights = {
                            'can_access_backup': False,
                            'can_edit_posts': False,
                            'can_edit_courses': False,
                            'can_upload_pdfs': False,
                            'can_manage_admins': False
                            }
                    # elif user.admin_role_id:
                        # User has an admin role, fetch the role's permissions
                       
                    # Return user and admin rights
                    return user, admin_rights
                else:
                    # User not found in the database
                    return None, None
            else:
                # Session has expired, clear session
                session.clear()
                return None, None
        else:
            # Session not found in the database
            return None, None
    else:
        # Session token not found in session
        return None, None
