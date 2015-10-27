from django.contrib import admin
from .models import Users,Objects,Camera,Coordenates,Servers,MapSettings,ObjectsType


# Register your models here.
admin.site.register(Users)
admin.site.register(Objects)
admin.site.register(Camera)
admin.site.register(Coordenates)
admin.site.register(Servers)
admin.site.register(MapSettings)
admin.site.register(ObjectsType)