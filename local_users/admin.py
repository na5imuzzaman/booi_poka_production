from django.contrib import admin
from .models import LocalUser, UserProfile

admin.site.register(LocalUser)
admin.site.register(UserProfile)
