from app import app, celery
from flask_user.emails import send_email


@celery.task
def send_email_task(**kwargs):
    with app.app_context():
        send_email(**kwargs)