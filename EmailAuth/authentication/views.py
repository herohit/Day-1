from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout as auth_logout,login as auth_login
from django.contrib.auth.decorators import login_required




#homepage
@login_required(login_url='/login/')
def home(request):
    username = request.user.username
    context={'username':username}
    return render(request,'homepage.html',context) 


# register view
def register(request):
    pass



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
