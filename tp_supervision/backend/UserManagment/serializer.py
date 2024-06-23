from rest_framework import serializers
from .models import MyUser

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'username','password', 'email', 'date_of_birth', 'profession', 'full_name', 'phone', 'twitter_profile', 'fb_profile', 'insta_profile', 'linkedin_profile', 'address', 'profile_picture', 'profile_url']
