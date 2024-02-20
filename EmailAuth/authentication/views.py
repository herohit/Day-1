from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import CustomUserCreationForm 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout as auth_logout,login as auth_login,authenticate
from django.contrib.auth.decorators import login_required
from .models import Profile

from django.contrib.auth.models import User
from .utils import generate_otp
from .utils import send_otp_email
from django.contrib import messages

from .decorator import email_verified_required

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

                otp = generate_otp()

                # Save email and OTP to profile
                profile = Profile.objects.create(user=user, email=email, email_verification_code=otp)


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
    if request.method == 'POST':
        entered_otp = request.POST.get('otp').strip()

        
        profile = Profile.objects.get(user=request.user)

        # Verify the entered OTP
        if entered_otp == profile.email_verification_code:
            profile.is_email_verified = True
            profile.save()


            messages.success(request, 'Email verification successful! Now you have full access to site')
            return redirect('home')
        else:
            # OTP is incorrect
            messages.error(request, 'Invalid OTP. Please try again.')
            return render(request, 'verify_otp.html')

    
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
