from django.shortcuts import render
from django.db import connection
from .models import ObjectsType,Users,Objects,Camera,Coordenates,InsertDeleteUpdate,Servers,MapSettings

# Create your views here.

def dictfetchall(cursor):
	desc = cursor.description
	return [dict(zip([call[0] for call in desc],raw)) for raw in cursor.fetchall()]

def get_all_objects():
	con = connection.cursor()
	con.execute('select * from campusuhapp_Objects')
	return dictfetchall(con)

def home(request):
	template = 'home.html'
	obje = get_all_objects()
	print obje
	return render(request,template,{'obje':obje})