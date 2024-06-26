# Generated by Django 4.2.11 on 2024-06-26 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='active_processes',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='cached_memory',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='collected_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='cpu_load_per_core',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='cpu_temperature',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='disk_percentage',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='gpu_usage_percentage',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='memory_percentage',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='net_bytes_recv',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='net_bytes_sent',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='swap_percentage',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='swap_total',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='swap_used',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='timestamp',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='used_disk',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='used_memory',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='collected_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='cores',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='cpu_frequency',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='logical_cores',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='machine_architecture',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='node_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='processor',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='releases',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='system',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='timestamp',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='total_disk',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='total_memory',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='version',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='variabledata',
            name='battery_percentage',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='variabledata',
            name='boot_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='variabledata',
            name='collected_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='variabledata',
            name='mac_address',
            field=models.CharField(blank=True, max_length=17, null=True),
        ),
        migrations.AlterField(
            model_name='variabledata',
            name='timestamp',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='variabledata',
            name='uptime',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
