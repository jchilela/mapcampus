from django.shortcuts import render
from django.db import connection
from django.http import  HttpResponse,HttpResponseRedirect
from .models import ObjectsType, Users, Objects, Camera, Servers, MapSettings, Buildings, Floors, \
    Rooms,VGI
from .forms import *
import json

# Create your views here.

def dictfetchall(cursor):
    desc = cursor.description
    return [dict(zip([call[0] for call in desc], raw)) for raw in cursor.fetchall()]


def get_all_buildings():
    con = connection.cursor()
    con.execute('SELECT id, "Name", "Description", url, "Date", "UserId_id", "Floors", "Picture", "MaterialImage", "MaterialColor", st_X(location), st_Y(location) FROM campusuhapp_buildings')
    return dictfetchall(con)


def get_all_flroors_coodinates(buildingid):
    con = connection.cursor()
    con.execute('SELECT id, "codBuilding_id", "FloorName", "Description", "Picture", "MaterialImage", "MaterialColor", "UserId_id", "Date", "Altitude" , st_X(location),st_Y(location), ST_AsGeoJSON(geometry) FROM campusuhapp_floors where "codBuilding_id" =%s' % (buildingid))
    return dictfetchall(con)

def get_all_rooms_coodinates(buildingid, floorNumber):
    con = connection.cursor()
    con.execute('SELECT id, "Building_id", "RoomName", "Description", url, "Password", "Picture", "MaterialImage", "MaterialColor", "UserId_id", "Date", "Altitude", st_X(location) as x ,st_Y(location) as y,  ST_AsGeoJSON(geometry) FROM campusuhapp_rooms where "Building_id" =%s and "Floors" = %s' % (
    buildingid,floorNumber))
    return dictfetchall(con)


def get_objects(roomID):
    con = connection.cursor()
    con.execute('SELECT id, "Buildings_id", "Rooms_id", "TypeObj_id", "Name", "Description", url, "Value", "UserId_id", "Floors", "Picture", "MaterialImage","MaterialColor", "latitude", "longitude", "Ip", "UserName","Password", "Port", "Date", st_X(location) as x ,st_Y(location) as y FROM campusuhapp_objects where "Rooms_id"=%s ' % (
    roomID))
    return dictfetchall(con)

def get_objects_search(search):
    query = connection.cursor()
    query.execute('SELECT id, "Buildings_id", "Rooms_id", "TypeObj_id", "Name", "Description", url, "Value", "UserId_id", "Floors", "Picture", "MaterialImage","MaterialColor", "latitude", "longitude", "Ip", "UserName","Password", "Port", "Date", st_X(location) as x ,st_Y(location) as y FROM campusuhapp_objects where "Name" like %s',("%" + search +"%",));
    return dictfetchall(query)





def home(request):
    if request.method == 'POST':
        form = HomeSearch(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']
            Objects= get_objects_search(search)
            template = 'rooms.html'

            return render(request,template,{'Objects':Objects})
    else:
        template = 'home.html'
        building = get_all_buildings()
        return render(request, template, {'building': building})
def convGeo_to_List_Coordnates(geogenson,roomname):
    count = 0
    lista = []
    listatemp= []
    temp = {}
    temp2 = {}
    dictfinal= {}
    for r in range(len(geogenson)):
        first = geogenson[r]['st_asgeojson'] # get the geogeson field in geral dictionary
        second = eval(first) # converte the geogeson to a dictionario
        third = second['coordinates'] # get the value of key coordenates. Is a list
        forth = third[0] # get the first element of the list
        for j in range(len(forth)):
            for i in range (1):
                temp['longitude'] = forth[j][0] 
                temp['latitude'] = forth[j][1]
                temp['id']=geogenson[r]['id']
                try:
                    temp['RoomName'] = geogenson[r]['RoomName']
                    
                except Exception, e:
                    temp['RoomName'] = geogenson[r]['FloorName']
                    
                else:
                    pass
                finally:
                    pass
                listatemp.append(temp)
                temp = {}
        lista.append(listatemp)
        listatemp = []

    return lista


    


def floors(request):
    template = 'floors.html'
    buildingid = request.GET.get('buildingid')
    floorNumber = request.GET.get('floorNumber')
    floors = get_all_flroors_coodinates(buildingid)
    rooms = get_all_rooms_coodinates(buildingid, floorNumber)
    print'Rooms---------\n\n\n\n', rooms

    try:
        coordenadas = convGeo_to_List_Coordnates(rooms,rooms[0]['RoomName'])
    except Exception, e:
        coordenadas = []
    else:
        pass
    finally:
        pass
    
    try:
        floors = convGeo_to_List_Coordnates(floors,floors[0]['FloorName'])
    except Exception, e:
        floors = []
    else:
        pass
    finally:
        pass

    return render(request, template, {'floors': floors,'coordesfinal':coordenadas})



def rooms(request):
    template = 'rooms.html'
    roomID = request.GET.get('roomID')
    Objects=get_objects(roomID)
    print Objects

    #floors = get_all_flroors_coodinates(buildingid)
    #rooms = get_all_rooms_coodinates(buildingid, floorNumber)
    #coordenadas = convGeo_to_List_Coordnates(rooms,rooms[0]['RoomName'])
    #floors = convGeo_to_List_Coordnates(floors,floors[0]['FloorName'])
    return render(request, template, {'Objects': Objects})

#------------------------------ OBJECTS WITH PICK TYPE-------------------------------------
def get_typeOfObjects():
    con = connection.cursor()
    con.execute('SELECT id, "TypeObj" FROM public.campusuhapp_objectstype')
    return dictfetchall(con)

def get_objects_per_type(search):
    query = connection.cursor()
    query.execute('SELECT id, "Buildings_id", "Rooms_id", "TypeObj_id", "Name", "Description", url, "Value", "UserId_id", "Floors", "Picture", "MaterialImage","MaterialColor", "latitude", "longitude", "Ip", "UserName","Password", "Port", "Date", st_X(location) as x ,st_Y(location) as y FROM campusuhapp_objects where "TypeObj_id"= %s',(str(search),));
    return dictfetchall(query)

#Function to search for objects in objects form

def search_objects(search):
    query = connection.cursor()
    query.execute('SELECT id, "Buildings_id", "Rooms_id", "TypeObj_id", "Name", "Description", url, "Value", "UserId_id", "Floors", "Picture", "MaterialImage","MaterialColor", "latitude", "longitude", "Ip", "UserName","Password", "Port", "Date", st_X(location) as x ,st_Y(location) as y FROM campusuhapp_objects where "Name" like %s',("%" + search +"%",));
    return dictfetchall(query)

#This function takes all elements that belong in the same class, and order it. 
def get_all_similar_elements(vector):
    a = {}
    b = []
    objects_list = []
    objects_temp = {}
    for i in range(len(vector)):
        a['TypeObj'] = vector[i]['TypeObj']
        a['id'] = vector[i]['id']
        temp= get_objects_per_type(vector[i]['id'])
        objects_list.append(temp)
        b.append(a)
        a={}
    return b,objects_list



def objects(request):
    if request.method == 'POST':
        print "\n\n\n\n\n entra"
        form = ObjectsSearch(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']
            
            return HttpResponseRedirect('/home/')
    else:
        template = 'objects.html'
        typeOfObjects= get_typeOfObjects()
        objects,objects_list = get_all_similar_elements(typeOfObjects)
        return render(request,template,{'objects':objects,'objects_list':objects_list})

def camera(request):
    template = 'camera.html'
    return render(request,template)


def advancedsearchrr(request):
    template = 'advancedsearch.html'
    typeOfObjects=''
    if request.method == 'POST':
        form = ObjectsSearchAdvanced(request.POST)
        if form.is_valid():
            search = form.cleaned_data['ObjectType']
            typeOfObjects= Objects.objects.filter(TypeObj_id=search)
            print 'typeofobjects POST ---\n\n\n',typeOfObjects,'\n\n'
            return render(request,template,{'typeofobjects':typeOfObjects})
    else:
        typeOfObjects= ObjectsType.objects.all()
        #print 'typeofobjects ---\n\n\n',typeOfObjects,'\n\n'
        template = 'advancedsearch.html'
        return render(request,template,{'typeofobjects':typeOfObjects})


def get_objects_search_advance(search, name):
    query = connection.cursor()
    query.execute('SELECT id, "Buildings_id", "Rooms_id", "TypeObj_id", "Name", "Description", url, "Value", "UserId_id", "Floors", "Picture", "MaterialImage","MaterialColor", "latitude", "longitude", "Ip", "UserName","Password", "Port", "Date", st_X(location) as x ,st_Y(location) as y FROM campusuhapp_objects where "Name" like %s and "TypeObj_id"=%s', ("%" + name + "%",search));
    return dictfetchall(query)


def get_all_objects_search_advance():
    query = connection.cursor()
    query.execute('SELECT id, "Buildings_id", "Rooms_id", "TypeObj_id", "Name", "Description", url, "Value", "UserId_id", "Floors", "Picture", "MaterialImage","MaterialColor", "latitude", "longitude", "Ip", "UserName","Password", "Port", "Date", st_X(location) as x ,st_Y(location) as y FROM campusuhapp_objects');
    return dictfetchall(query)




def advancedsearch(request):
    if request.method == 'POST':
        form = ObjectsSearchAdvanced(request.POST)
        if form.is_valid():
            search = form.cleaned_data['ObjectType']
            name = form.cleaned_data['search']


            typjects = get_objects_search_advance(search,name)
            print 'procura--- \n ',search,'\n\n'
            print 'objectos--- desc\n ',typjects,name,'\n\n'
            typeOfObjects= ObjectsType.objects.all()
            template = 'advancedsearchs.html'
            return render(request,template,{'Objects':typjects,'typeofobjects':typeOfObjects})
    else:
        template = 'advancedsearchs.html'
        building = get_all_buildings()
        typjects = get_all_objects_search_advance()
        typeOfObjects= ObjectsType.objects.all()
        return render(request, template, {'Objects':typjects,'typeofobjects':typeOfObjects})


def experiencia(request):
    template = 'experiencia.html'
    return render(request,template)



def graphics(request):
    template = 'graphics.html'
    return render(request,template)



def ssh(request):
    template = 'framesSSH.html'
    return render(request,template)

def sshmain(request):
    template = 'chrome-extension://pnhechapfaindjhompbnflcldabbghjo/html/nassh.html'
    return render(request,template)

#______________________VGI_________________________________________
def get_typeOfObjects_vgi():
    con = connection.cursor()
    con.execute('SELECT id, "Type_VGI" FROM public.campusuhapp_vgi_type')
    return dictfetchall(con)




def get_objects_per_type_vgi(search):
    query = connection.cursor()
    query.execute('SELECT id, "Type_VGI_id", "Description" , "User_ID", "Picture","MaterialColor", "latitude", "longitude", st_X(location) as x ,st_Y(location) as y FROM campusuhapp_vgi where "Type_VGI_id"= %s',(str(search),));
    return dictfetchall(query)



def get_all_similar_elements_vgi(vector):
    a = {}
    b = []
    objects_list = []
    objects_temp = {}
    for i in range(len(vector)):
        a['Type_VGI'] = vector[i]['Type_VGI']
        a['id'] = vector[i]['id']
        temp= get_objects_per_type_vgi(vector[i]['id'])
        objects_list.append(temp)
        b.append(a)
        a={}
    return b,objects_list





def vgi(request):
    if request.method == 'POST':
        print "\n\n\n\n\n entra"
        form = ObjectsSearch(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']
            
            return HttpResponseRedirect('/home/')
    else:
        template = 'vgi.html'
        typeOfObjects= get_typeOfObjects_vgi()
        objects,objects_list = get_all_similar_elements_vgi(typeOfObjects)
        return render(request,template,{'objects':objects,'objects_list':objects_list})

#________________________Sensors_________________________
def get_objects_per_type_sensors(search):
    query = connection.cursor()
    query.execute('SELECT campusuhapp_objects.id, campusuhapp_objectstype."TypeObj", campusuhapp_objects."Buildings_id", campusuhapp_objects."Rooms_id", campusuhapp_objects."TypeObj_id", campusuhapp_objects."Name", campusuhapp_objects."Description", campusuhapp_objects.url, campusuhapp_objects."Value", campusuhapp_objects."UserId_id", campusuhapp_objects."Floors", campusuhapp_objects."Picture", campusuhapp_objects."MaterialImage",campusuhapp_objects."MaterialColor", campusuhapp_objects."latitude", campusuhapp_objects."longitude", campusuhapp_objects."Ip", campusuhapp_objects."UserName",campusuhapp_objects."Password", campusuhapp_objects."Port", campusuhapp_objects."Date", st_X(campusuhapp_objects.location) as x ,st_Y(campusuhapp_objects.location) as y FROM public.campusuhapp_objects, public.campusuhapp_objectstype WHERE campusuhapp_objects."TypeObj_id" = campusuhapp_objectstype.id and campusuhapp_objectstype."TypeObj"=%s',(str(search),));
    return dictfetchall(query)



def get_all_similar_elements_Sensor(vector):
    a = {}
    b = []
    objects_list = []
    objects_temp = {}
    for i in range(len(vector)):
        a['TypeObj'] = vector[i]['TypeObj']
        a['id'] = vector[i]['id']
        temp= get_objects_per_type_sensors(vector[i]['id'])
        objects_list.append(temp)
        b.append(a)
        a={}
    return b,objects_list




def sensors(request):
    template = 'sensors.html'
    typeOfObjects= get_objects_per_type_sensors("Sensor")
    print typeOfObjects
    return render(request,template,{'objects':typeOfObjects})







#____________________________ALERT when the value is equal  or less than, equal or more than_________________________



def get_objects_per_type_sensors_alert(search):
    Alert_temp_when = 40
    Alert_humidity_when = 40
    Alert_co2_When = 60
    Alert_light_when = 2
    Alert_radiation_When =1
    Alert_sound_When =1
    Alert_resistence_when =1 
    Alert_moviment_when = 1
    Alert_proximity_when =1

    query = connection.cursor()
    query.execute('SELECT campusuhapp_objects.id, campusuhapp_objectstype."TypeObj", campusuhapp_objects."Buildings_id", campusuhapp_objects."Rooms_id", campusuhapp_objects."TypeObj_id", campusuhapp_objects."Name", campusuhapp_objects."Description", campusuhapp_objects.url, campusuhapp_objects."Value", campusuhapp_objects."UserId_id", campusuhapp_objects."Floors", campusuhapp_objects."Picture", campusuhapp_objects."MaterialImage",campusuhapp_objects."MaterialColor", campusuhapp_objects."latitude", campusuhapp_objects."longitude", campusuhapp_objects."Ip", campusuhapp_objects."UserName",campusuhapp_objects."Password", campusuhapp_objects."Port", campusuhapp_objects."Date", st_X(campusuhapp_objects.location) as x ,st_Y(campusuhapp_objects.location) as y FROM public.campusuhapp_objects, public.campusuhapp_objectstype WHERE campusuhapp_objects."TypeObj_id" = campusuhapp_objectstype.id and campusuhapp_objectstype."TypeObj"=%s',(str(search),));
    return dictfetchall(query)



def get_all_similar_elements_Sensor_alert(vector):
    a = {}
    b = []
    objects_list = []
    objects_temp = {}
    for i in range(len(vector)):
        a['TypeObj'] = vector[i]['TypeObj']
        a['id'] = vector[i]['id']
        temp= get_objects_per_type_sensors_alert(vector[i]['id'])
        objects_list.append(temp)
        b.append(a)
        a={}
    return b,objects_list




def alerts(request):
    template = 'alerts.html'
    typeOfObjects= get_objects_per_type_sensors_alert("Sensor")
    print typeOfObjects
    return render(request,template,{'objects':typeOfObjects})














