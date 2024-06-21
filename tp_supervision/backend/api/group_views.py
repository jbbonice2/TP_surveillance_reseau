from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework import status

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def group_list_view(request,token):
    search_text = request.GET.get('s', '')
    is_paginated = request.GET.get('ip', 'no').lower() == 'yes'
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Token.DoesNotExist:
        return JsonResponse({'error': 'Invalid token'}, status=400)
        page_number = int(request.GET.get('pn', 1))
    except ValueError:
        page_number = 1
    
    try:
        page_size = int(request.GET.get('ps', 10))
    except ValueError:
        page_size = 10

    # Filtrer les groupes en fonction du texte de recherche
    groups = MyGroup.objects.filter(
        Q(code__icontains=search_text) |
        Q(label__icontains=search_text) |
        Q(description__icontains=search_text)
    )

    if is_paginated:
        paginator = Paginator(groups, page_size)
        try:
            groups_page = paginator.page(page_number)
        except PageNotAnInteger:
            groups_page = paginator.page(1)
        except EmptyPage:
            groups_page = paginator.page(paginator.num_pages)
        
        result = {
            'groups': list(groups_page.object_list.values()),
            'page': groups_page.number,
            'pages': paginator.num_pages,
            'total': paginator.count,
        }
    else:
        result = {
            'groups': list(groups.values())
        }

    return JsonResponse(result, status= status.HTTP_201_CREATED)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def group_detail_view(request, group_id,token):
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Token.DoesNotExist:
        return JsonResponse({'error': 'Invalid token'}, status=400)

        # Récupération du groupe
        group = MyGroup.objects.get(pk=group_id)
        serializer = MyGroupSerializer(group)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return JsonResponse({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    except MyGroup.DoesNotExist:
        return JsonResponse({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['POST'])
def create_group(request, token):

    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Token.DoesNotExist:
        return JsonResponse({'error': 'Invalid token'}, status=400)
    # Vérifier si tous les champs requis sont présents dans la requête
    required_fields = ['code', 'label']
    if not all(field in request.data for field in required_fields):
        return JsonResponse({'error': 'Mandatory fields are missing'}, status=status.HTTP_400_BAD_REQUEST)

    # Vérifier si le code du groupe existe déjà
    if MyGroup.objects.filter(code=request.data['code']).exists():
        return JsonResponse({'error': 'Group code already exists'}, status=status.HTTP_409_CONFLICT)

    # Créer un sérialiseur avec les données de la requête
    serializer = GroupSerializer(data=request.data)

    # Valider les données du sérialiseur
    if serializer.is_valid():
        # Sauvegarder le groupe
        serializer.save()
        # Renvoyer les données du groupe créé
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_user_to_group(request, group_id, user_id,token):

    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Token.DoesNotExist:
        return JsonResponse({'error': 'Invalid token'}, status=400)
    # Vérifier si les IDs de groupe et d'utilisateur sont fournis dans la requête
    if not group_id or not user_id:
        return JsonResponse({'error': 'Group ID or User ID is missing'}, status=400)

    # Vérifier si le groupe existe
    group = get_object_or_404(MyGroup, pk=group_id)

    # Vérifier si l'utilisateur existe
    user = get_object_or_404(Userapp, pk=user_id)

    # Ajouter l'utilisateur au groupe
    group.users.add(user)

    # Récupérer la liste des utilisateurs appartenant au groupe après l'ajout
    users_in_group = list(group.users.all().values())

    return JsonResponse(users_in_group,status=200, safe=False)     


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_users_in_group(request, group_id, token):
    # Vérification du token passé en paramètre de l'URL
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Token.DoesNotExist:
        return JsonResponse({'error': 'Invalid token'}, status=400)

    # Vérifier si le group_id est fourni dans la requête
    if not group_id:
        return JsonResponse({'error': 'Group ID is missing'}, status=400)

    # Vérifier si la liste des userIds est fournie dans la requête
    user_ids = request.data.get('userIds', '')
    if not user_ids:
        return JsonResponse({'error': 'User IDs are missing'}, status=400)

    # Convertir la liste des userIds en une liste d'entiers
    try:
        user_ids = [int(uid) for uid in user_ids.split(',')]
    except ValueError:
        return JsonResponse({'error': 'User IDs must be a comma-separated list of integers'}, status=400)

    # Vérifier si le groupe existe
    group = get_object_or_404(MyGroup, pk=group_id)

    # Vérifier si chaque utilisateur existe
    users = []
    for user_id in user_ids:
        try:
            user = Userapp.objects.get(pk=user_id)
            users.append(user)
        except Userapp.DoesNotExist:
            return JsonResponse({'error': f'User with ID {user_id} does not exist'}, status=400)

    # Mettre à jour la liste des utilisateurs du groupe
    group.users.clear()  # Supprimer tous les utilisateurs du groupe
    group.users.add(*users)  # Ajouter les nouveaux utilisateurs

    # Récupérer la liste des utilisateurs appartenant au groupe après la mise à jour
    users_in_group = list(group.users.all().values('id', 'username', 'email'))

    return JsonResponse(users_in_group, safe=False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_group_permissions(request, group_id,token):
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Token.DoesNotExist:
        return JsonResponse({'error': 'Invalid token'}, status=400)

        # Vérification de l'existence du groupe
        group = get_object_or_404(MyGroup, pk=group_id)

        # Récupération des permissionIds
        permission_ids = request.data.get('permissionIds', '')
        if not permission_ids:
            return JsonResponse({'error': 'Permission IDs are missing'}, status=status.HTTP_400_BAD_REQUEST)

        # Convertir la liste des permissionIds en une liste d'entiers
        try:
            permission_ids = [int(pid) for pid in permission_ids.split(',')]
        except ValueError:
            return JsonResponse({'error': 'Permission IDs must be a comma-separated list of integers'}, status=status.HTTP_400_BAD_REQUEST)

        # Vérification de l'existence des permissions
        permissions = []
        for permission_id in permission_ids:
            try:
                permission = MyPermission.objects.get(pk=permission_id)
                permissions.append(permission)
            except MyPermission.DoesNotExist:
                return JsonResponse({'error': f'Permission with ID {permission_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        # Mettre à jour la liste des permissions du groupe
        group.permissions.clear()  # Supprimer toutes les permissions du groupe
        group.permissions.add(*permissions)  # Ajouter les nouvelles permissions

        # Récupérer la liste des permissions appartenant au groupe après la mise à jour
        permissions_in_group = list(group.permissions.all().values('id', 'name', 'description'))

        return JsonResponse(permissions_in_group, safe=False, status=status.HTTP_200_OK)

    except Token.DoesNotExist:
        return JsonResponse({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    except MyGroup.DoesNotExist:
        return JsonResponse({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_group(request, id,token):
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Token.DoesNotExist:
        return JsonResponse({'error': 'Invalid token'}, status=400)
        # Récupération du groupe par son ID
        group = get_object_or_404(MyGroup, pk=id)
        
        # Récupération des données du corps de la requête
        data = request.data
        code = data.get('code')
        label = data.get('label')
        description = data.get('description')
        active = data.get('active')

        # Vérification des champs obligatoires
        if not code or not label:
            return JsonResponse({'error': 'Code and label are required fields'}, status=status.HTTP_400_BAD_REQUEST)

        # Mise à jour des informations du groupe
        group.code = code
        group.label = label
        group.description = description
        group.active = active
        group.save()

        # Sérialisation du groupe mis à jour
        serializer = MyGroupSerializer(group)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    except MyGroup.DoesNotExist:
        return JsonResponse({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_group(request, id,token):
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Token.DoesNotExist:
        return JsonResponse({'error': 'Invalid token'}, status=400)
        # Récupération du groupe par son ID
        group = get_object_or_404(MyGroup, pk=id)
        
        # Vérification s'il y a des utilisateurs liés à ce groupe
        if MyUserGroup.objects.filter(group=group).exists():
            return JsonResponse({'error': 'Cannot delete group with related users'}, status=status.HTTP_400_BAD_REQUEST)

        # Suppression du groupe
        group.delete()
        return JsonResponse({'message': 'Group deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    except MyGroup.DoesNotExist:
        return JsonResponse({'error': 'Group not found'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def remove_user_from_group(request, user_id, group_id,token):
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Token.DoesNotExist:
        return JsonResponse({'error': 'Invalid token'}, status=400)
        # Vérifier si l'utilisateur existe
        user = Userapp.objects.get(id=user_id)
    except Userapp.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        # Vérifier si le groupe existe
        group = MyGroup.objects.get(id=group_id)
    except MyGroup.DoesNotExist:
        return JsonResponse({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Vérifier si l'utilisateur est déjà dans le groupe
    try:
        user_group = MyUserGroup.objects.get(user=user, group=group)
    except MyUserGroup.DoesNotExist:
        return JsonResponse({'error': 'User is not in this group'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Supprimer l'utilisateur du groupe
    user_group.delete()
    
    return JsonResponse({'message': 'User removed from group successfully'}, status=status.HTTP_200_OK)       

@api_view(['PUT'])
def disable_permission_in_group(request, group_id, permission_id,token):
    try:
        token_obj = Token.objects.get(key=token)
        user = token_obj.user
    except Token.DoesNotExist:
        return JsonResponse({'error': 'Invalid token'}, status=400)
        # Vérifier si le groupe existe
        group = MyGroup.objects.get(id=group_id)
    except MyGroup.DoesNotExist:
        return JsonResponse({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        # Vérifier si la permission existe
        permission = MyPermission.objects.get(id=permission_id)
    except MyPermission.DoesNotExist:
        return JsonResponse({'error': 'Permission not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Vérifier si la permission est déjà désactivée dans le groupe
    try:
        group_permission = MyGroupPermissions.objects.get(group=group, permission=permission)
    except MyGroupPermissions.DoesNotExist:
        return JsonResponse({'error': 'Permission is not assigned to this group'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Désactiver la permission dans le groupe
    group_permission.active = False
    group_permission.save()
    
    return JsonResponse({'message': 'Permission disabled in group successfully'}, status=status.HTTP_200_OK)