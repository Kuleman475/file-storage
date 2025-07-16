from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

def index(request):
    return render(request, 'storage_app/index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')  # or wherever you want to go after login
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    else:
        return render(request, 'storage_app/login.html')

def register(request):
    if request.method == 'POST':
       username = request.POST['username']
       password = request.POST['password']
       email = request.POST['email']
       phone = request.POST['phone']

       if User.objects.filter(username=username).exists():
           messages.error(request, 'Username already taken.')
           return redirect('register')
        
        # Create the user
       user = User.objects.create_user(username=username, password=password, email=email)
        # (Optional) store phone somewhere; User model doesn’t have phone by default

        # Log the user in
       login(request, user)

       return redirect('index')  # send to home page
    else:
        return render(request, 'storage_app/register.html')

def logout_view(request):
    logout(request)
    return redirect('index')