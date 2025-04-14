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

]
