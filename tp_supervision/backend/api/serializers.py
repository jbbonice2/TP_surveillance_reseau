from rest_framework import serializers
from .models import *
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import MyPermission
from django.contrib.auth.hashers import make_password

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'

class MachineDataSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()
    class Meta:
        model = Machine
        fields = '__all__'

    
    def get_data(self, obj):
        return obj.data_set

class MachineVariableDataSerializer(serializers.ModelSerializer):
    variableData = serializers.SerializerMethodField()
    class Meta:
        model = VariableData
        fields = '__all__'

    
    def get_variableData(self, obj):
        return obj.variableData_set

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


