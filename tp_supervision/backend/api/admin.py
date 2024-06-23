# Dans api/admin.py

from django.contrib import admin
from .models import Machine, Userapp, MyGroup,  VariableData, Data

# Enregistrement des modèles dans l'interface d'administration
admin.site.register(Machine)
admin.site.register(Userapp)
admin.site.register(MyGroup)
admin.site.register(VariableData)
admin.site.register(Data)
