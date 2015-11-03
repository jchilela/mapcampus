from django.shortcuts import render
from django.db import connection
from .models import ObjectsType,Users,Objects,Camera,ObjectsCoordenates,Servers,MapSettings,Buildings,Floors,Rooms,FloorsCoordinates,RoomsCoordinates


# Create your views here.

def dictfetchall(cursor):
	desc = cursor.description
	return [dict(zip([call[0] for call in desc],raw)) for raw in cursor.fetchall()]

def get_all_buildings():
	con = connection.cursor()
	con.execute('select * from campusuhapp_Buildings')
	return dictfetchall(con)

def get_all_flroors_coodinates(Codbuilding,Codfloor):
	con = connection.cursor()
	con.execute("select * from campusuhapp_FloorsCoordinates where Codbuilding='%s'" %(Codbuilding,Codfloor ));
	return dictfetchall(con)


def home(request):
	template = 'home.html'
	building = get_all_buildings()
	return render(request,template,{'building':building})