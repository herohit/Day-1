import random
import string

from django.core.mail import send_mail
from django.conf import settings



def generate_otp():
    otp = ''.join(random.choices(string.digits, k=6))
    return otp


def send_otp_email(email, otp):
    subject = 'Verification Code'
    message = f'Your verification code is: {otp}'
    sender_email = settings.EMAIL_HOST_USER

    try:
        send_mail(subject, message, sender_email, [email])
        return True
    except Exception as e:
        # Log the error or handle it appropriately
        print(f"Error sending email: {str(e)}")
        return False