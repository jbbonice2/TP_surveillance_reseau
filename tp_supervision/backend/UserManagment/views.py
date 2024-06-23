import json
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from rest_framework import status
from django.contrib.auth import login, logout
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import AllowAny
from .serializer import MyUserSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import *
from django.contrib.auth.hashers import check_password
@api_view(['POST'])
# @permission_classes([AllowAny])
def user_registration_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Assuming the data is sent as JSON
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        # Créer un nouvel utilisateur
        print(data)
        user = MyUser.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name= last_name)
        user.save()
        return JsonResponse({'message':'Ok'}, status=status.HTTP_201_CREATED)
    return JsonResponse( status=status.HTTP_400_BAD_REQUEST)



# @permission_classes([AllowAny])
@api_view(['POST'])
def user_login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body) 
        email = data.get('email')
        password = data.get('password')
        print({
            'email':email,
            'password':  password
        })
        
        
        try:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                myuser = MyUser.objects.get(user_ptr=user)
                login(request, myuser)
                return JsonResponse({'success': True, 'user': {'username': myuser.username, 'id':myuser.pk, 'name': myuser.first_name + " " + myuser.last_name, 'profile_url': myuser.profile_url if myuser.profile_picture else ""}})
            else:
                return JsonResponse({'success': False, 'error': 'user is none'}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            return JsonResponse({'success': False, 'error': e.__str__()})