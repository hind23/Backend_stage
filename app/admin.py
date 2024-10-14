from django.contrib import admin
from .models import Client , Admin
# Register your models here .
@admin.register(Client,Admin)

class UserAdmin(admin.ModelAdmin):
    list_display = ("nom","prenom") 