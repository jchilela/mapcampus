from django.conf import settings 
from django.contrib.gis import admin 
from django.contrib.gis.geos import GEOSGeometry
from .models import ObjectsType,Users,Objects,Camera,Servers,MapSettings,Buildings,Floors,Rooms,GeoModelAdmin

class RoomsAdmin(admin.OSMGeoAdmin):
	#fields = ('RoomName', 'url','geometry')
	search_fields = ['RoomName','Building__Name']
	list_display = ('RoomName', 'Building')
	list_filter = ('RoomName', 'Building')
	g = GEOSGeometry('POINT (9.191884 45.464254)') # Set map center 
	g.set_srid(4326)
	g.transform(900913)
	default_lon = int(g.x) 
	default_lat = int(g.y) 
	default_zoom = 4 
	extra_js = ["http://maps.google.com/maps/api/js?v=3.2&sensor=false"] 
	map_template = 'admin/gmgdav3.html'

class ObjectsAdmin(admin.OSMGeoAdmin):
	#fields = ('RoomName', 'url','geometry')
	search_fields = ['Name','Buildings__Name']
	list_display = ('Name', 'Buildings','Rooms')
	list_filter = ('Name', 'Buildings')



class GoogleAdmin(admin.OSMGeoAdmin): 
	g = GEOSGeometry('POINT (9.191884 45.464254)') # Set map center 
	g.set_srid(4326)
	g.transform(900913)
	default_lon = int(g.x) 
	default_lat = int(g.y) 
	default_zoom = 4 
	extra_js = ["http://maps.google.com/maps/api/js?v=3.2&sensor=false"] 
	map_template = 'admin/gmgdav3.html'



# Register your models here.
admin.site.register(ObjectsType,admin.OSMGeoAdmin)
admin.site.register(Users,admin.OSMGeoAdmin)
admin.site.register(Objects,GoogleAdmin)
admin.site.register(Camera,admin.OSMGeoAdmin)
admin.site.register(Servers,admin.OSMGeoAdmin)
admin.site.register(MapSettings,admin.OSMGeoAdmin)
admin.site.register(Buildings,GoogleAdmin)
admin.site.register(Floors,admin.OSMGeoAdmin)
admin.site.register(Rooms,RoomsAdmin)
