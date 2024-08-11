from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
#ajout du model personnaliser sur la page admin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ["username", 'email','first_name','last_name','is_staff',]
    
    fieldsets = (
        (None, {'fields': ('username','password')}),
        ('Personal info', {'fields': ('first_name', 'last_name','email', 'phone_number',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('username','email','phone_number', 'password1', 'password2')}),
       
    )
admin.site.site_header='InMarket Administration'

