# mail.py

from flask_mail import Message
from flask import current_app
from . import mail

def send_verification_email(email, verification_link):
    """Send verification email to the user."""
    subject = 'Verify Your Email'
    body = f'Click the following link to verify your email address: {verification_link}'
    msg = Message(subject, sender=current_app.config['MAIL_USERNAME'], recipients=[email])

    # msg = Message(subject, recipients=[email])
    msg.body = body

    try:
        mail.send(msg)
        current_app.logger.info(f"Verification email sent to {email}")
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to send verification email to {email}: {str(e)}")
        return False
