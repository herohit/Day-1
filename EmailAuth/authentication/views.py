from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm




#homepage
def home(request):
    return render(request,'homepage.html') 


# register view
def register(request):

    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('home')

    context={'form':form}
    return render(request,'register.html',context) 



# login view
def login(request):
    return render(request,'login.html') 



# logout view
def logout(request):
    return render(request,'logout.html') 
