from django.contrib import admin
from .models import ObjectsType,Users,Objects,Camera,ObjectsCoordenates,Servers,MapSettings,Buildings,Floors,Rooms,FloorsCoordinates,RoomsCoordinates


# Register your models here.
admin.site.register(ObjectsType)
admin.site.register(Users)
admin.site.register(Objects)
admin.site.register(Camera)
admin.site.register(ObjectsCoordenates)
admin.site.register(Servers)
admin.site.register(MapSettings)
admin.site.register(Buildings)
admin.site.register(Floors)
admin.site.register(Rooms)
admin.site.register(FloorsCoordinates)
admin.site.register(RoomsCoordinates)