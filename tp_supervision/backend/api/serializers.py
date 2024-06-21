from rest_framework import serializers
from .models import *
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import MyPermission
from django.contrib.auth.hashers import make_password




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userapp
        fields = ['first_name', 'last_name', 'username', 'image' , 'date_joined', 'id', 'password', 'active']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Hacher le mot de passe avant de créer l'utilisateur
        validated_data['password'] = make_password(validated_data['password'])
        user = Userapp.objects.create(**validated_data)
        return user


class GroupSerializer(serializers.ModelSerializer):
    users_count = serializers.SerializerMethodField()
    users = UserSerializer(many=True, source='myusergroup_set.user', read_only=True)

    class Meta:
        model = MyGroup
        fields = ['name', 'description', 'created_by', 'created_at', 'modified_at', 'id', 'users_count', 'users']

    def get_users_count(self, obj):
        return obj.myusergroup_set.count()



class MyPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyPermission
        fields = ['id', 'name', 'description', 'created_at', 'modified_at', 'active']

    def create_custom_permissions(self):
        # Créer des permissions personnalisées en utilisant le modèle MyPermission
        for permission_data in [
            {"name": "Creer un utilisateur", "description": "Permission pour créer un utilisateur"},
            {"name": "Supprimer un utilisateur", "description": "Permission pour supprimer un utilisateur"},
            {"name": "Ajouter un utilisateur à un groupe", "description": "Permission pour ajouter un utilisateur à un groupe"},
            {"name": "Modifier les informations d'un utilisateur", "description": "Permission pour modifier les informations d'un utilisateur"},
            {"name": "Voir la liste des utilisateurs", "description": "Permission pour voir la liste des utilisateurs"},
            {"name": "Retirer un utilisateur d'un groupe", "description": "Permission pour retirer un utilisateur d'un groupe"},
            {"name": "Désactiver une permission d'un utilisateur", "description": "Permission pour désactiver une permission d'un utilisateur"},
            {"name": "Ajouter une permission à un utilisateur", "description": "Permission pour ajouter une permission à un utilisateur"},
            {"name": "Ajouter une permission à un groupe", "description": "Permission pour ajouter une permission à un groupe"},
            {"name": "Désactiver une permission à un groupe", "description": "Permission pour désactiver une permission à un groupe"},
            {"name": "Se connecter", "description": "Permission pour se connecter"},
        ]:
            MyPermission.objects.create(**permission_data)

        # Associer les permissions au modèle approprié (ici, MyPermission)
        content_type = ContentType.objects.get_for_model(MyPermission)
        for permission in MyPermission.objects.all():
            Permission.objects.create(
                name=permission.name,
                content_type=content_type,
                codename=permission.name.lower().replace(" ", "_")
            )
