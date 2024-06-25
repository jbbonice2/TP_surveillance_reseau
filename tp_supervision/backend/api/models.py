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
    system = models.CharField(max_length=50)
    node_name = models.CharField(max_length=100)
    machine_architecture = models.CharField(max_length=20)
    processor = models.CharField(max_length=100)
    cores = models.IntegerField()
    logical_cores = models.IntegerField()
    cpu_frequency = models.FloatField()
    total_memory = models.BigIntegerField()
    total_disk = models.BigIntegerField()
    version = models.CharField(max_length=100)
    releases = models.CharField(max_length=200)
    collected_at = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mac_address


class Data(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    used_memory = models.BigIntegerField()
    memory_percentage = models.FloatField()
    cached_memory = models.BigIntegerField()
    swap_total = models.BigIntegerField()
    swap_used = models.BigIntegerField()
    swap_percentage = models.FloatField()
    used_disk = models.BigIntegerField()
    disk_percentage = models.FloatField()
    cpu_load_per_core = models.JSONField()
    net_bytes_sent = models.BigIntegerField()
    net_bytes_recv = models.BigIntegerField()
    active_processes = models.IntegerField()
    gpu_usage_percentage = models.FloatField()
    cpu_temperature = models.FloatField()
    collected_at = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now=True)
    internet_enabled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.machine.mac_address} - {self.collected_at}"


class VariableData(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    mac_address = models.CharField(max_length=17)
    battery_percentage = models.FloatField()
    uptime = models.BigIntegerField()
    boot_time = models.DateTimeField()
    shutdown_time = models.DateTimeField(null=True, blank=True)
    collected_at = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)
    ip = models.CharField(max_length=17, null=True, blank=True)

    def __str__(self):
        return f"{self.mac_address} - {self.collected_at}"


class MyGroup(models.Model):
    # Définition des champs de votre modèle MyGroup
    group_name = models.CharField(max_length=100)
    # Autres champs ...

    def __str__(self):
        return self.group_name