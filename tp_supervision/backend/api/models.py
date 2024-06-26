from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Models
class Userapp(AbstractUser):
    username = models.CharField(unique=True, max_length=100)
    image = models.ImageField(upload_to='user_images', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.username


class Machine(models.Model):
    machine_type = models.CharField(max_length=50)
    mac_address = models.CharField(max_length=17, unique=True)
    system = models.CharField(max_length=50,  null=True, blank=True)
    node_name = models.CharField(max_length=100, null=True, blank=True)
    machine_architecture = models.CharField(max_length=20, null=True, blank=True)
    processor = models.CharField(max_length=100, null=True, blank=True)
    cores = models.IntegerField( null=True, blank=True)
    logical_cores = models.IntegerField( null=True, blank=True)
    cpu_frequency = models.FloatField( null=True, blank=True)
    total_memory = models.BigIntegerField( null=True, blank=True)
    total_disk = models.BigIntegerField( null=True, blank=True)
    version = models.CharField(max_length=100, null=True, blank=True)
    releases = models.CharField(max_length=200, null=True, blank=True)
    collected_at = models.DateTimeField(auto_now_add=True,  null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True,  null=True, blank=True)

    def __str__(self):
        return self.mac_address


class Data(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    used_memory = models.BigIntegerField( null=True, blank=True)
    memory_percentage = models.FloatField( null=True, blank=True)
    cached_memory = models.BigIntegerField( null=True, blank=True)
    swap_total = models.BigIntegerField( null=True, blank=True)
    swap_used = models.BigIntegerField( null=True, blank=True)
    swap_percentage = models.FloatField( null=True, blank=True)
    used_disk = models.BigIntegerField( null=True, blank=True)
    disk_percentage = models.FloatField(null=True, blank=True)
    cpu_load_per_core = models.JSONField( null=True, blank=True)
    net_bytes_sent = models.BigIntegerField( null=True, blank=True)
    net_bytes_recv = models.BigIntegerField( null=True, blank=True)
    active_processes = models.IntegerField( null=True, blank=True)
    gpu_usage_percentage = models.FloatField( null=True, blank=True)
    cpu_temperature = models.FloatField( null=True, blank=True)
    collected_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True,  null=True, blank=True)
    internet_enabled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.machine.mac_address} - {self.collected_at}"


class VariableData(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    mac_address = models.CharField(max_length=17, null=True, blank=True)
    battery_percentage = models.FloatField( null=True, blank=True)
    uptime = models.BigIntegerField( null=True, blank=True)
    boot_time = models.DateTimeField( null=True, blank=True)
    shutdown_time = models.DateTimeField(null=True, blank=True)
    collected_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True,  null=True, blank=True)
    ip = models.CharField(max_length=17, null=True, blank=True)

    def __str__(self):
        return f"{self.mac_address} - {self.collected_at}"


class MyGroup(models.Model):
    # Définition des champs de votre modèle MyGroup
    group_name = models.CharField(max_length=100)
    # Autres champs ...

    def __str__(self):
        return self.group_name
