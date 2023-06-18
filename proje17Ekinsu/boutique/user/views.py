from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# from .forms import *
# Create your views here.
def userRegister(request):
    username = ''
    email = ''
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if User.objects.filter(username = username).exists():
                messages.error(request, 'Username in use')
            elif User.objects.filter(email = email).exists():
                messages.error(request, 'Email in use')
            elif len(password1) < 6:
                messages.error(request, 'Password must be at least 6 characters.')
            elif username in password1 or username.lower() in password1:
                print(username, username.lower(), password1)
                messages.error(request, 'Username and password cannot be the same.')
            else:
                user = User.objects.create_user(
                    username = username,
                    email = email,
                    password = password1
                )
                user.save()
                messages.success(request, 'The user has been created.')
                return redirect('index')
        else:
            messages.error(request, 'Passwords do not match')    
    context = {
        'username':username,
        'email':email
    }    
    return render(request, 'user/register.html', context)

def userLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Signed in')
            return redirect('index')
        else:
            messages.error(request, 'Username or password is wrong')
            return redirect('login')
    return render(request, 'user/login.html')

def userLogout(request):
    logout(request)
    return redirect('index')