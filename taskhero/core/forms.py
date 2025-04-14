from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Task

from django import forms
from .models import CustomUser
from .models import UserProfile
import datetime


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2







class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'status', 'priority']
        
    due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    priority = forms.ChoiceField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])

    # Validate date
    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date < datetime.date.today():
            raise forms.ValidationError("Due date cannot be in the past.")
        return due_date




class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'})
        }
