from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta

class Userapp(AbstractUser):
    username = models.CharField(unique=True,max_length=100)
    image = models.ImageField(upload_to='user_images', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.username

class MyPermission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True)
    active = models.BooleanField(default=True)


    

class MyGroup(models.Model):
    code = models.CharField(max_length=100, unique=True)
    label = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)   
    created_by = models.ForeignKey(Userapp, on_delete=models.CASCADE) 
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.label    

class UserappPermissions(models.Model):
    user = models.ForeignKey(Userapp, on_delete=models.CASCADE)
    permission = models.ForeignKey(MyPermission, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True) 

class MyGroupPermissions(models.Model):
    group = models.ForeignKey(MyGroup, on_delete=models.CASCADE)
    permission = models.ForeignKey(MyPermission, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)     

class MyUserGroup(models.Model):
    user = models.ForeignKey(Userapp, on_delete=models.CASCADE)
    group = models.ForeignKey(MyGroup, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)      





import json

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
    timestamp = models.DateTimeField(auto_now_add=True)

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
    timestamp = models.DateTimeField(auto_now_add=True)
    collected_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.machine.mac_address} - {self.collected_at}"


class VariableData(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, default=1)
    mac_address = models.CharField(max_length=17)
    battery_percentage = models.FloatField()
    uptime = models.BigIntegerField()
    boot_time = models.DateTimeField()
    shutdown_time = models.DateTimeField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    collected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mac_address} - {self.collected_at}"
