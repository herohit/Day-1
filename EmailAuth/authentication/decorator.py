from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse
from .models import Profile
from django.contrib import messages

def email_verified_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            # Get the user's profile
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            # Redirect to register page if profile does not exist
            return redirect(reverse('register'))

        # Check if email is verified
        if not profile.is_email_verified:
            messages.error(request, 'Please verify your email to access edit profile')
            return redirect('verify_otp')  # Redirect to OTP verification page if email is not verified
        
        # Call the view function if email is verified
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view