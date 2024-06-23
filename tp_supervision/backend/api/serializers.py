from rest_framework import serializers
from .models import *
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.hashers import make_password
# Serializers
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
        return Data.objects.filter(machine=obj).values()


class MachineVariableDataSerializer(serializers.ModelSerializer):
    variableData = serializers.SerializerMethodField()

    class Meta:
        model = VariableData
        fields = '__all__'

    def get_variableData(self, obj):
        return VariableData.objects.filter(machine=obj).values()


class VariableDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariableData
        fields = '__all__'

class MachineSerializer2(serializers.ModelSerializer):
    variabledata_set = VariableDataSerializer(many=True, read_only=True)

    class Meta:
        model = Machine
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userapp
        fields = ['first_name', 'last_name', 'username', 'image', 'date_joined', 'id', 'password', 'active']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = Userapp.objects.create(**validated_data)
        return user

