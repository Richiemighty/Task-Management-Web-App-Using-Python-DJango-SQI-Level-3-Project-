from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.landing, name='landing'),
    path('signup/', views.signup_view, name='signup'),
    # Redirect login to signup page with ?signup=true
    path('login/', views.login_view, name='login'), 
    path('logout/', auth_views.LogoutView.as_view(next_page='landing'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-task/', views.create_task, name='create_task'),  # Create task page
    path('settings/', views.settings_view, name='settings'),
    path('', views.task_list, name='task_list'),  # Make sure this name matches
    path('task/edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('task/<int:task_id>/start/', views.start_task, name='start_task'),
    path('task/<int:task_id>/complete/', views.complete_task, name='complete_task'),
    path('search/', views.search_tasks, name='search_tasks'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),


] 
