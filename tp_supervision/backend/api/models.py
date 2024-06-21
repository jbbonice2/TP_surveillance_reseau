from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta

class Userapp(AbstractUser):
    username = models.CharField(unique=True,max_length=100)
    image = models.ImageField(upload_to='user_images', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.username

class MyPermission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True)
    active = models.BooleanField(default=True)


    

class MyGroup(models.Model):
    code = models.CharField(max_length=100, unique=True)
    label = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)   
    created_by = models.ForeignKey(Userapp, on_delete=models.CASCADE) 
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.label    

class UserappPermissions(models.Model):
    user = models.ForeignKey(Userapp, on_delete=models.CASCADE)
    permission = models.ForeignKey(MyPermission, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True) 

class MyGroupPermissions(models.Model):
    group = models.ForeignKey(MyGroup, on_delete=models.CASCADE)
    permission = models.ForeignKey(MyPermission, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)     

class MyUserGroup(models.Model):
    user = models.ForeignKey(Userapp, on_delete=models.CASCADE)
    group = models.ForeignKey(MyGroup, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)      

