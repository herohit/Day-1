from django.db import models
from django.contrib.auth.models import User

import pyotp
from django.utils import timezone
from .utils import generate_otp , send_otp_email
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    email_verification_code = models.CharField(max_length=6)
    email_verification_code_created_at = models.DateTimeField(null=True)
    is_email_verified = models.BooleanField(default=False)


    @staticmethod
    def generate_otp():
        return generate_otp()

    def set_email_verification_code(self):
        self.email_verification_code = self.generate_otp()
        self.email_verification_code_created_at = timezone.now()
        self.save()
        # send_otp_email(self.email, self.email_verification_code)

    def verify_email_verification_code(self, otp):
        if self.email_verification_code == otp and (timezone.now() - self.email_verification_code_created_at).total_seconds() <= 900:
            self.is_email_verified = True
            self.save()
            return True
        return False

    def __str__(self):
        return self.email

