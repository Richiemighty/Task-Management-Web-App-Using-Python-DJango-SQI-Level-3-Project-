from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def landing(request):
    return render(request, 'core/landing.html')

def login_view(request):
    return render(request, 'core/login.html')  # Create this later

def signup_view(request):
    return render(request, 'core/signup.html')  # Create this later
