from django.contrib import admin
from .models import UniqUser

@admin.register(UniqUser)
class AdminUniqUser(admin.ModelAdmin) :
    list_display = ('username' , 'email')

