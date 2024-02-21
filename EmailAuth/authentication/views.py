from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import CustomUserCreationForm 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout as auth_logout,login as auth_login,authenticate
from django.contrib.auth.decorators import login_required
from .models import Profile

from django.contrib.auth.models import User
# from .utils import generate_otp
from .utils import send_otp_email,is_otp_expired
from django.contrib import messages

from .decorator import email_verified_required
from django.utils import timezone


#homepage
@login_required(login_url='/login/')
def home(request):
    current_user_profile = Profile.objects.get(user=request.user)
    username = request.user.username
    context={'username':username,'current_user_profile':current_user_profile}
    return render(request,'homepage.html',context) 


# register view
def register(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Username already exists')
            elif User.objects.filter(email=email).exists():
                form.add_error('email', 'Email already exists')
            else:
                # Create user
                user = User.objects.create_user(username=username, email=email, password=password)

                profile = Profile.objects.create(user=user, email=email)

                # to generate otp
                otp = Profile.generate_otp()
                profile.email_verification_code = otp
                profile.email_verification_code_created_at = timezone.now()
                profile.save()


                user = authenticate(request, username=username, password=password)
                if user is not None:
                    # Log in the user
                    auth_login(request, user)

                    # if not send_otp_email(email, otp):
                    # Failed to send email, handle error
                        # return HttpResponse('Failed to send OTP email. Please try again later.')



                # Redirect to the OTP verification page
                return redirect('verify_otp')

    context = {'form': form}
    return render(request, 'register.html', context)

@login_required(login_url='/login/')
def verify_otp(request):
    profile = Profile.objects.get(user=request.user)
    if profile.is_email_verified:
        return redirect('home')
    if request.method == 'POST':
        entered_otp = request.POST.get('otp').strip()

        



        if profile.verify_email_verification_code(entered_otp):


            messages.success(request, 'Email verification successful! Now you have full access to site')
            return redirect('home')
        else:

            if is_otp_expired(profile.email_verification_code_created_at):
                profile.set_email_verification_code()
                messages.warning(request, 'The OTP has expired. A new OTP has been sent to your email.')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
    return render(request, 'verify_otp.html')



@login_required
@email_verified_required
def edit_profile(request):
    return render(request,'edit_profile.html')


# login view
def login(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    context={'form':form}
    return render(request,'login.html',context)




# logout view
def logout(request):
    auth_logout(request)
    return redirect('login') 
