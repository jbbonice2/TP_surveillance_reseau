from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from .models import Data, Machine, MyPermission, Userapp, UserappPermissions, VariableData
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from .serializers import  MachineDataSerializer, MachineSerializer, MachineVariableDataSerializer, UserSerializer
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@api_view(['GET'])
def user_list_view(request,token):
    if request.method == 'GET':
        try:
            token_obj = Token.objects.get(key=token)
            user = token_obj.user
        except Userapp.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Filtrer les utilisateurs seulement si l'utilisateur est authentifié
        search_text = request.query_params.get('s', None)
        is_paginated = request.query_params.get('ip', 'no').lower() == 'yes'
        page_number = request.query_params.get('pn', 1)
        page_size = request.query_params.get('ps', 10)

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

        serializer = UserSerializer(users, many=is_paginated)

        if is_paginated:
            return Response({
                'count': paginator.count,
                'num_pages': paginator.num_pages,
                'current_page': page_number,
                'users': serializer.data
            })
        else:
            return Response(serializer.data)  # Retourner directement les données sans pagination


@api_view(['GET'])
def user_detail_view(request, user_id,token):
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Userapp.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Vérifier si l'utilisateur est authentifié
    if not request.user.is_authenticated:
        return Response({'error': 'User must be logged in'}, status=403)

    # Récupérer l'utilisateur correspondant à l'ID donné
    user = get_object_or_404(Userapp, pk=user_id)

    # Serializer l'utilisateur
    serializer = UserSerializer(user)

    # Retourner les détails de l'utilisateur
    return JsonResponse(serializer.data)







@api_view(['PUT'])
def change_password(request, token):
    if request.method == 'PUT':
        # Récupérer l'utilisateur à mettre à jour
        try:
            token_obj = Token.objects.get(key=token)
            user = token_obj.user
        except Userapp.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Vérifier si le mot de passe actuel est correct
        current_password = request.data.get('currentpassword')
        if not user.check_password(current_password):
            return JsonResponse({"error": "Current password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        new_password = request.data.get('newpassword')
        hashed_password = make_password(new_password)
        user.password = hashed_password
        user.save()

        return JsonResponse({"message": "Password updated successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def register_user(request,token):
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Userapp.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Récupération des données de la requête
    last_name = request.data.get('last_name')
    first_name = request.data.get('first_name')
    username = request.data.get('username')
    password = request.data.get('password')
   

    # Vérification si les champs obligatoires sont fournis
    if not last_name or not first_name or not password or not username:
        return JsonResponse({'error': 'Mandatory fields are not provided'}, status=status.HTTP_400_BAD_REQUEST)

    # Vérification si l'utilisateur avec le même nom d'utilisateur existe déjà
    if Userapp.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists'}, status=status.HTTP_409_CONFLICT)

    # Création de l'utilisateur
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

@api_view(['POST'])
def set_user_permissions(request, user_id,token):
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Userapp.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user = Userapp.objects.get(id=user_id)
    except Userapp.DoesNotExist:
        return Response({'error': 'User with the given ID does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserPermissionsSerializer(data=request.data)
    if serializer.is_valid():
        permission_ids = serializer.validated_data['permissionIds']

        # Vérification des permissions existantes
        existing_permissions = MyPermission.objects.filter(id__in=permission_ids)
        if len(existing_permissions) != len(permission_ids):
            return Response({'error': 'One or more permissions do not exist'}, status=status.HTTP_400_BAD_REQUEST)

        # Révoquer toutes les permissions actuelles de l'utilisateur
        UserappPermissions.objects.filter(user=user).delete()

        # Assigner les nouvelles permissions
        for perm in existing_permissions:
            UserappPermissions.objects.create(user=user, permission=perm)

        # Retourner la liste des permissions actuelles de l'utilisateur
        updated_permissions = UserappPermissions.objects.filter(user=user)
        permission_list = [perm.permission.id for perm in updated_permissions]

        return Response({'permissions': permission_list}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_user(request, token):
    if request.method == 'DELETE':
        # Récupérer l'utilisateur à mettre à jour
        try:
            token_obj = Token.objects.get(key=token)
            user = token_obj.user
        except Userapp.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return JsonResponse({'status':"sucess"}, status=status.HTTP_200_OK)
    return JsonResponse({'message':"Non allowed  method "}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
def update_user(request, id):
    try:
        user = Userapp.objects.get(id=id)
    except Userapp.DoesNotExist:
        return JsonResponse({'error': 'User with the given ID does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    # Vérification de l'authentification (vérifier le token)
    token_key = request.headers.get('Authorization')
    if not token_key:
        return JsonResponse({'error': 'Authorization token is missing'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        token = Token.objects.get(key=token_key)
        if token.user != user:
            return JsonResponse({'error': 'You are not authorized to update this user'}, status=status.HTTP_403_FORBIDDEN)
    except Token.DoesNotExist:
        return JsonResponse({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

    # Récupération des données de la requête
    last_name = request.data.get('last_name')
    first_name = request.data.get('first_name')
    username = request.data.get('username')
    password = request.data.get('password')
    active = request.data.get('active', user.active)  # Par défaut, conserver l'état actuel de l'utilisateur

    # Vérification si les champs obligatoires sont fournis
    if not last_name or not first_name or not username:
        return JsonResponse({'error': 'Mandatory fields are not provided'}, status=status.HTTP_400_BAD_REQUEST)

    # Mise à jour des champs de l'utilisateur
    user.last_name = last_name
    user.first_name = first_name
    user.username = username
    user.active = active

    if password:
        user.password = make_password(password)

    user.save()

    # Sérialisation des données de l'utilisateur mis à jour
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
def logout_user(request,token):
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Userapp.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        request.user.auth_token.delete()
    except:
        pass
    return JsonResponse({'message': 'Logout successful'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_permission_to_user(request, user_id, permission_id,token):
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Userapp.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        # Vérifier si l'utilisateur existe
        user = Userapp.objects.get(id=user_id)
    except Userapp.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        # Vérifier si la permission existe
        permission = MyPermission.objects.get(id=permission_id)
    except MyPermission.DoesNotExist:
        return Response({'error': 'Permission not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Ajouter la permission à l'utilisateur
    user_permission, created = UserappPermissions.objects.get_or_create(user=user, permission=permission)
    
    if created:
        return Response({'message': 'Permission added successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': 'Permission already exists for this user'}, status=status.HTTP_200_OK)


@api_view(['PUT'])
def disable_permission_for_user(request, user_id, permission_id,token):
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Userapp.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        # Vérifier si l'utilisateur existe
        user = Userapp.objects.get(id=user_id)
    except Userapp.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        # Vérifier si la permission existe
        permission = MyPermission.objects.get(id=permission_id)
    except MyPermission.DoesNotExist:
        return Response({'error': 'Permission not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Vérifier si la permission est déjà désactivée pour l'utilisateur
    try:
        user_permission = UserappPermissions.objects.get(user=user, permission=permission)
    except UserappPermissions.DoesNotExist:
        return Response({'error': 'Permission is not assigned to this user'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Désactiver la permission pour l'utilisateur
    user_permission.active = False
    user_permission.save()
    
    return Response({'message': 'Permission disabled for user successfully'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def register_admin(request):
   
    # Récupération des données de la requête
    last_name = request.data.get('last_name')
    first_name = request.data.get('first_name')
    username = request.data.get('username')
    password = request.data.get('password')
   

    # Vérification si les champs obligatoires sont fournis
    if not last_name or not first_name or not password or not username:
        return JsonResponse({'error': 'Mandatory fields are not provided'}, status=status.HTTP_400_BAD_REQUEST)

    # Vérification si l'utilisateur avec le même nom d'utilisateur existe déjà
    if Userapp.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists'}, status=status.HTTP_409_CONFLICT)

    # Création de l'utilisateur
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
        return JsonResponse({"error": "Invalid token"}, status=404)

    # Vérifier si l'utilisateur est authentifié
    if not user.is_authenticated:
        return Response({'error': 'User must be logged in'}, status=403)
    machines = Machine.objects.all()
    serializer = MachineSerializer(machines, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def machine_detail(request, pk, token):
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Token.DoesNotExist:
        return JsonResponse({"error": "Invalid token"}, status=404)

    # Vérifier si l'utilisateur est authentifié
    if not user.is_authenticated:
        return Response({'error': 'User must be logged in'}, status=403)
    machine = get_object_or_404(Machine, pk=pk)
    serializer = MachineDataSerializer(machine)
    variable_data = MachineVariableDataSerializer(machine)
    return JsonResponse({"data":serializer.data, "variable_data":variable_data.data})



@api_view(['GET'])
def variable_data_list(request, pk, token):
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Token.DoesNotExist:
        return JsonResponse({"error": "Invalid token"}, status=404)

    # Vérifier si l'utilisateur est authentifié
    if not user.is_authenticated:
        return Response({'error': 'User must be logged in'}, status=403)
    machine = get_object_or_404(Machine, pk=pk)
    serializer = MachineVariableDataSerializer(machine)
    return JsonResponse(serializer.data, safe=False)

