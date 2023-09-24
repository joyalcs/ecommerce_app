from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']

admin.site.register(User, UserAdmin)
