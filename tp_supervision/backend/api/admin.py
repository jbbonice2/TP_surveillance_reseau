# Dans admin.py
from django.contrib import admin
from .models import Userapp, MyGroup, MyPermission, MyUserGroup, UserappPermissions, MyGroupPermissions

# Enregistrez vos modèles ici
admin.site.register(Userapp)
admin.site.register(MyGroup)
admin.site.register(MyPermission)
admin.site.register(MyUserGroup)
admin.site.register(MyGroupPermissions) 
admin.site.register(UserappPermissions)
