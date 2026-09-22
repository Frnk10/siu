from django.contrib import admin

# Register your models here.
from Aplicaciones.user.models import User

admin.site.register(User)