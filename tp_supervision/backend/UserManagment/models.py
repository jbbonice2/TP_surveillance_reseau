from django.contrib.auth.models import User
from django.db import models




class MyUser(User):
    date_of_birth = models.DateField(null=True, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    full_name = models.CharField(max_length=500, blank=True)
   
    phone = models.CharField(max_length=500, blank=True)
    twitter_profile = models.CharField(max_length=500, blank=True)
    fb_profile = models.CharField(max_length=500, blank=True)
    insta_profile = models.CharField(max_length=500, blank=True)
    linkedin_profile = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    profile_url = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return "{}".format( self.username)
    

