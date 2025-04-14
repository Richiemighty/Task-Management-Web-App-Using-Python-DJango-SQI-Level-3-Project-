from django.contrib import admin

# Register your models here.
from .models import CustomUserManager, CustomUser, UserProfile, Task


admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(Task)
