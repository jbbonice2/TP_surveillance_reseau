from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from .models import Data, Machine, Userapp, VariableData
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from .serializers import  MachineDataSerializer, MachineSerializer, MachineVariableDataSerializer, UserSerializer
from django.contrib.auth.hashers import make_password

@api_view(['GET'])
def user_list_view(request, token):
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Token.DoesNotExist:
        return JsonResponse({"error": "Invalid token"}, status=status.HTTP_404_NOT_FOUND)

    search_text = request.query_params.get('s', None)
    is_paginated = request.query_params.get('ip', 'no').lower() == 'yes'
    page_number = int(request.query_params.get('pn', 1))
    page_size = int(request.query_params.get('ps', 10))

    users = Userapp.objects.all()
    if search_text:
        users = users.filter(username__icontains=search_text) | \
                users.filter(first_name__icontains=search_text) | \
                users.filter(last_name__icontains=search_text)

    if is_paginated:
        paginator = Paginator(users, page_size)
        try:
            users = paginator.page(page_number)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        serializer = UserSerializer(users, many=True)
        return Response({
            'count': paginator.count,
            'num_pages': paginator.num_pages,
            'current_page': page_number,
            'users': serializer.data
        })
    else:
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def user_detail_view(request, user_id, token):
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Token.DoesNotExist:
        return JsonResponse({"error": "Invalid token"}, status=status.HTTP_404_NOT_FOUND)

    user = get_object_or_404(Userapp, pk=user_id)
    serializer = UserSerializer(user)
    return JsonResponse(serializer.data)


@api_view(['PUT'])
def change_password(request, token):
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Token.DoesNotExist:
        return JsonResponse({"error": "Invalid token"}, status=status.HTTP_404_NOT_FOUND)

    current_password = request.data.get('currentpassword')
    if not user.check_password(current_password):
        return JsonResponse({"error": "Current password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
    
    new_password = request.data.get('newpassword')
    user.password = make_password(new_password)
    user.save()
    return JsonResponse({"message": "Password updated successfully"}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_user(request, token):
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Token.DoesNotExist:
        return JsonResponse({"error": "Invalid token"}, status=status.HTTP_404_NOT_FOUND)

    user.delete()
    return JsonResponse({'status': "success"}, status=status.HTTP_200_OK)


@api_view(['PUT'])
def update_user(request, id):
    try:
        user = Userapp.objects.get(id=id)
    except Userapp.DoesNotExist:
        return JsonResponse({'error': 'User with the given ID does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    token_key = request.headers.get('Authorization')
    if not token_key:
        return JsonResponse({'error': 'Authorization token is missing'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        token = Token.objects.get(key=token_key)
        if token.user != user:
            return JsonResponse({'error': 'You are not authorized to update this user'}, status=status.HTTP_403_FORBIDDEN)
    except Token.DoesNotExist:
        return JsonResponse({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

    last_name = request.data.get('last_name')
    first_name = request.data.get('first_name')
    username = request.data.get('username')
    password = request.data.get('password')
    active = request.data.get('active', user.active)

    if not last_name or not first_name or not username:
        return JsonResponse({'error': 'Mandatory fields are not provided'}, status=status.HTTP_400_BAD_REQUEST)

    user.last_name = last_name
    user.first_name = first_name
    user.username = username
    user.active = active

    if password:
        user.password = make_password(password)

    user.save()
    serializer = UserSerializer(user)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return JsonResponse({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        user_data = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'token': token.key
        }
        return JsonResponse(user_data, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def logout_user(request, token):
    try:
        token_obj = Token.objects.get(key=token)
        token_obj.delete()
    except Token.DoesNotExist:
        return JsonResponse({"error": "Invalid token"}, status=status.HTTP_404_NOT_FOUND)
    
    return JsonResponse({'message': 'Logout successful'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def register_admin(request):
    last_name = request.data.get('last_name')
    first_name = request.data.get('first_name')
    username = request.data.get('username')
    password = request.data.get('password')

    if not last_name or not first_name or not password or not username:
        return JsonResponse({'error': 'Mandatory fields are not provided'}, status=status.HTTP_400_BAD_REQUEST)

    if Userapp.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists'}, status=status.HTTP_409_CONFLICT)

    user_data = {
        'last_name': last_name,
        'first_name': first_name,
        'username': username,
        'password': password,
    }
    serializer = UserSerializer(data=user_data)
    if serializer.is_valid():
        user = serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def machine_list(request, token):
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Token.DoesNotExist:
        return JsonResponse({"error": "Invalid token"}, status=status.HTTP_404_NOT_FOUND)

    if not user.is_authenticated:
        return Response({'error': 'User must be logged in'}, status=status.HTTP_403_FORBIDDEN)
    
    machines = Machine.objects.all()
    serializer = MachineSerializer(machines, many=True)
    return JsonResponse(serializer.data, safe=False)

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Machine, VariableData
from .serializers import MachineVariableDataSerializer, MachineSerializer2
from rest_framework.authtoken.models import Token


# @api_view(['GET'])
# def variable_data_list(request, pk, token):
#     try:
#         token_obj = Token.objects.get(key=token)
#         user = token_obj.user
#     except Token.DoesNotExist:
#         return JsonResponse({"error": "Invalid token"}, status=status.HTTP_404_NOT_FOUND)

#     if not user.is_authenticated:
#         return Response({'error': 'User must be logged in'}, status=status.HTTP_403_FORBIDDEN)
    
#     machine = get_object_or_404(Machine, pk=pk)
#     variable_data = VariableData.objects.filter(machine=machine)
#     serializer = MachineVariableDataSerializer(variable_data, many=True)
#     return Response(serializer.data, safe=False)



@api_view(['GET'])
def variable_data_list(request, pk, token):
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Token.DoesNotExist:
        return JsonResponse({"error": "Invalid token"}, status=status.HTTP_404_NOT_FOUND)

    if not user.is_authenticated:
        return Response({'error': 'User must be logged in'}, status=status.HTTP_403_FORBIDDEN)

    machine = get_object_or_404(Machine, pk=pk)
    serializer = MachineSerializer2(machine)
    return Response(serializer.data)

@api_view(['GET'])
def machine_detail(request, pk, token):
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Token.DoesNotExist:
        return Response({"error": "Invalid token"}, status=status.HTTP_404_NOT_FOUND)

    # Vérifier si l'utilisateur est authentifié
    if not user.is_authenticated:
        return Response({'error': 'User must be logged in'}, status=status.HTTP_403_FORBIDDEN)

    machine = get_object_or_404(Machine, pk=pk)
    serializer = MachineDataSerializer(machine)
    return Response(serializer.data, status=status.HTTP_200_OK)