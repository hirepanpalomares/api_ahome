from django.db import models

# Create your models here.

class ClientsRegistered(models.Model):
    name = models.CharField(max_length=200, default='')
    phone = models.CharField(max_length=15, default='')
    email = models.CharField(max_length=100, default='')
    message = models.CharField(max_length=500, default='')
