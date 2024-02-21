from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    email_verification_code = models.CharField(max_length=6)
    is_email_verified = models.BooleanField(default=False)
    # email_verification_timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email

