from celery import shared_task
from django.core.mail import send_mail
import time


@shared_task
def send_welcome_email(user_email, username):
    """
    Send a welcome email to newly registered users.
    This is an example of a Celery task for authentication.
    """
    subject = f'Welcome {username}!'
    message = f'Thank you for registering, {username}. Welcome to our platform!'

    # Simulate email sending delay
    time.sleep(2)

    # In production, configure email backend in settings
    # send_mail(subject, message, 'noreply@example.com', [user_email])

    print(f"Welcome email sent to {user_email}")
    return f"Email sent to {user_email}"


@shared_task
def cleanup_expired_tokens():
    """
    Example scheduled task to clean up expired tokens.
    Could be configured with Celery Beat.
    """
    # Implementation would check token expiry and clean up
    print("Cleaning up expired tokens...")
    return "Token cleanup completed"
