from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import TaskForm
from .models import Task




def landing(request):
    return render(request, 'core/landing.html')

def signup_view(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'signup':
            # Handle sign up
            first_name = request.POST.get('firstname')
            last_name = request.POST.get('lastname')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if not username:
                messages.error(request, "Username is required.")
                return redirect('/signup/?signup=true')

            if password1 != password2:
                messages.error(request, "Passwords do not match.")
                return redirect('/signup/?login=true')

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return redirect('/signup/?login=true')

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
                return redirect('/signup/?login=true')
        
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            login(request, user)
            return redirect('dashboard')  # Or wherever

        elif form_type == 'login':
            # Handle login
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')

            else:
                messages.error(request, "Invalid login credentials.")
                return redirect('/signup/?login=true')

    return render(request, 'core/signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('/signup/?login=true')



@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)  # Only show tasks belonging to the logged-in user
    return render(request, 'core/dashboard.html', {'tasks': tasks})



def redirect_to_signup(request):
    return redirect('/signup/?signup=true')










@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Assign the task to the logged-in user
            task.save()
            return redirect('dashboard')  # Redirect to the dashboard after saving the task
    else:
        form = TaskForm()

    return render(request, 'core/create_task.html', {'form': form})




@login_required
def edit_task(request, task_id):
    # Your code for editing a task
    pass

@login_required
def delete_task(request, task_id):
    # Your code for deleting a task
    pass
