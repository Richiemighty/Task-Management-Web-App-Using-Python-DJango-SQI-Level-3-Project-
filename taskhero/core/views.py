from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .forms import TaskForm, ProfilePictureForm, SignupForm
from .models import Task, UserProfile
from datetime import date





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
    profile = UserProfile.objects.get(user=request.user)
    tasks_to_do = Task.objects.filter(user=request.user, status='to_do')
    tasks_in_progress = Task.objects.filter(user=request.user, status='in_progress')
    tasks_completed = Task.objects.filter(user=request.user, status='completed')
    
    return render(request, 'core/dashboard.html', {
        'tasks_to_do': tasks_to_do,
        'tasks_in_progress': tasks_in_progress,
        'tasks_completed': tasks_completed,
        'profile': profile,
        'today': date.today()  
    })



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
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to the task list after updating
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'core/edit_task.html', {'form': form, 'task': task})


@login_required
def task_list(request):
    # logic here
    return render(request, 'core/task_list.html', {'tasks': []})


# Delete task view
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)  # Ensure the task belongs to the logged-in user
    
    if request.method == 'POST':
        task.delete()
        return redirect('dashboard')  # Redirect back to the dashboard after deletion
    
    return render(request, 'core/delete_task.html', {'task': task})







@login_required
def settings_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = ProfilePictureForm(instance=profile)

    return render(request, 'core/settings.html', {'form': form, 'profile': profile})





@login_required
def start_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.status = 'in_progress'
        task.save()
    return redirect('dashboard')

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.status = 'completed'
        task.save()
    return redirect('dashboard')




