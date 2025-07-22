from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import  UploadedFile
from .forms import UploadFileForm
import os
from django.conf import settings


def index(request):
        files = UploadedFile.objects.all().order_by('-uploaded_at')
        return render(request, 'storage_app/index.html', {'files': files})

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
      
        # Log the user in
       login(request, user)

       return redirect('index')  # send to home page
    else:
        return render(request, 'storage_app/register.html')

def logout_view(request):
    logout(request)
    return redirect('index')


def upload_view(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            UploadedFile.objects.create(
                user=request.user,
                title=form.cleaned_data['title'],
                file=form.cleaned_data['file']
            )
            messages.success(request, "File uploaded successfully.")
            return redirect("index")
    else:
        form = UploadFileForm()
    return render(request, "storage_app/upload.html", {"form": form})
    

def handle_uploaded_file(f):
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'upload')
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, f.name) 

    with open(file_path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
