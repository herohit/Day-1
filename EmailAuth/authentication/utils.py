import random
import string
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings



# def generate_otp():
#     otp = ''.join(random.choices(string.digits, k=6))
#     return otp


import pyotp


def generate_otp():
    totp = pyotp.TOTP(pyotp.random_base32(), interval=900, digits=6)
    return totp.now()


def send_otp_email(email, otp):
    subject = 'Verification Code'
    message = f'Your verification code is: {otp} . Valid upto 15 min'
    sender_email = settings.EMAIL_HOST_USER

    try:
        send_mail(subject, message, sender_email, [email])
        return True
    except Exception as e:
        # Log the error or handle it appropriately
        print(f"Error sending email: {str(e)}")
        return False
    

def is_otp_expired(created_at):
    expiration_time = created_at + timezone.timedelta(minutes=15)  # OTP expires after 15 minutes
    return expiration_time < timezone.now()