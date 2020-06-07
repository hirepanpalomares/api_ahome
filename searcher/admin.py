from django.contrib import admin

# Register your models here.

from .models import Property, ImageProperty

admin.site.register(Property)
admin.site.register(ImageProperty)