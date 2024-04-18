from celery import Celery

celery = Celery(__name__)

def make_celery(app):
    celery.conf.update(app.config)
    return celery

# Initialize Celery
make_celery(app)

# Define Celery tasks
@celery.task
def send_fee_due_email_task(receiver_email, package_type):
    # Your task implementation here
    pass
