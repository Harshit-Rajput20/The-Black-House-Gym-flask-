from flask_mail import Mail

def init_mail(app):
    mail = Mail(app)
    return mail
