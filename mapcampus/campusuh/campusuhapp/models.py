from django.contrib.gis.db import models
#from django.db import models
from django.contrib.gis import admin
from smart_selects.db_fields import ChainedForeignKey 

# Create your models here
# We need to have informations about the person who is inserting, updating or deleting objects in database(Buildings,  sensors, conditional air, ect)
class ObjectsType(models.Model):
    TypeObj = models.CharField(max_length=50, null=True, blank=True)
    def __unicode__(self):
        return unicode(self.TypeObj)


class Users(models.Model):
    Name = models.CharField(max_length=100)
    UserName = models.CharField(max_length=100, null=True, blank=True)
    Password = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return unicode(self.Name)
# Just buldings at this table
class Buildings(models.Model):
    Name = models.CharField(max_length=300, null=True, blank=True)
    Description = models.CharField(max_length=5000, null=True, blank=True)
    url = models.FileField(upload_to='fotos/%Y/%m/%d', null=True, blank=True)
   # Value = models.FloatField(null=True, blank=True)
    Date = models.DateTimeField(auto_now_add=True, blank=True)
    UserId = models.ForeignKey(Users)
   # Password = models.CharField(max_length=45, null=True,
                               # blank=True)  # TO ACTIVATE, DEACTIVATE, OR CHANGE THE VALUE OF OBJECT WE NEED TO INSERT THE OBJECT PASSWORD. Imagine someone switching off your Conditional Air!.. :)
    Floors = models.IntegerField(null=True, blank=True)  # To use in pop-up of the object
    # As Entity.
    Picture = models.ImageField(upload_to='fotos/%Y/%m/%d', null=True, blank=True)  # Pop-Up image
    MaterialImage = models.ImageField(upload_to='fotos/%Y/%m/%d', null=True, blank=True)  # Material image
    MaterialColor = models.CharField(max_length=45, null=True, blank=True,help_text='Press "Tab" to refresh the map')
    location = models.PointField()
    objects = models.GeoManager()

    def __unicode__(self):
        return unicode(self.Name)
# Rooms represent the rooms. Every room is part of one floor
class Rooms(models.Model):
    
    Building = models.ForeignKey(Buildings)
    #Floors = ChainedForeignKey(Floors, 
    #    chained_field="Building",
    #    chained_model_field="codBuilding", 
     #   show_all=False, 
     #   auto_choose=True
    #)
    floors_choices = ((1,'First Floor'),(2,'Second Floor'),(3,'Third Floor'),(4,'Fourth Floor'),(5,'Fifth Floor'),(5,'Sixth Floor'),(5,'Seventh Floor'),(5,'Eighth Floor'),(5,'Ninth Floor'),(5,'Tenth Floor'))
    Floors = models.IntegerField(choices=floors_choices)
    RoomName = models.CharField(max_length=50)
    Description = models.CharField(max_length=5000, null=True, blank=True)
    url = models.FileField(upload_to='fotos/%Y/%m/%d', null=True, blank=True)
    Password = models.CharField(max_length=45, null=True,
                                blank=True)  # TO ACTIVATE, DEACTIVATE, OR CHANGE THE VALUE OF OBJECT WE NEED TO INSERT THE OBJECT PASSWORD. Imagine someone switching off your Conditional Air!.. :)
    # As Entity.
    Picture = models.ImageField(upload_to='fotos/%Y/%m/%d', null=True, blank=True)  # Pop-Up image
    MaterialImage = models.ImageField(upload_to='fotos/%Y/%m/%d', null=True, blank=True)  # Material image
    UserId = models.ForeignKey(Users)
    Date = models.DateTimeField(auto_now_add=True, blank=True)
    Altitude = models.FloatField(null=True, blank=True)
    MaterialColor = models.CharField(max_length=45, null=True, blank=True, help_text='Press "Tab" to refresh the map')
    location = models.PointField(null=True, blank=True) # The location is the  left botton corner of the building
    geometry = models.PolygonField() # The exactly geometry of the Room
    search_fields = ('location', 'geometry' )
    objects = models.GeoManager()
    def __unicode__(self):
        return unicode(self.RoomName)

# Every objects will be in the same table (Buildings, Sensors, Conditional air and others objects that we can manipulate by CLICKING)
class Objects(models.Model):
    Buildings = models.ForeignKey(Buildings)
    Rooms = ChainedForeignKey(Rooms, 
        chained_field="Buildings",
        chained_model_field="Building", 
        show_all=False, 
        auto_choose=True
    )
    #Floors = models.ForeignKey(Floors)

    TypeObj = models.ForeignKey(ObjectsType)
    Name = models.CharField(max_length=300, null=True, blank=True)
    Description = models.CharField(max_length=5000, null=True, blank=True)
    url = models.FileField(upload_to='fotos/%Y/%m/%d', null=True, blank=True)
    Value = models.FloatField(null=True, blank=True)
    UserId = models.ForeignKey(Users)
    Password = models.CharField(max_length=45, null=True,
                                blank=True)  # TO ACTIVATE, DEACTIVATE, OR CHANGE THE VALUE OF OBJECT WE NEED TO INSERT THE OBJECT PASSWORD. Imagine someone switching off your Conditional Air!.. :)
    Floors = models.IntegerField(null=True, blank=True)  # To use in pop-up of the object
    # As Entity.
    Picture = models.ImageField(upload_to='fotos/%Y/%m/%d', null=True, blank=True)  # Pop-Up image
    MaterialImage = models.ImageField(upload_to='fotos/%Y/%m/%d', null=True, blank=True)  # Material image
    MaterialColor = models.CharField(max_length=45, null=True, blank=True, help_text='Press "Tab" to refresh the map')
    Date = models.DateTimeField(auto_now_add=True, blank=True)
    location = models.PointField(null=True, blank=True)
    latitude = models.CharField(max_length=45, null=True, blank=True)
    longitude = models.CharField(max_length=45, null=True, blank=True)
    #IF IS A RASPBERRYPI:
    Ip = models.CharField(max_length=45, null=True, blank=True)
    UserName = models.CharField(max_length=45, null=True, blank=True)
    Password = models.CharField(max_length=45, null=True, blank=True)
    Port = models.IntegerField(null=True, blank=True)
    Date = models.DateTimeField(auto_now_add=True, blank=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return unicode(self.Name)


# This table saves the Camera configuration. Each object will have his own camera configuration. If we want to see a sensor in floor 5 of building #1, the camera needs to be closer in that object.
# Will be possible to define which camera is default. We will have 3 global camera(Code 1,100,100) One of them will be the pre-defined
class Camera(models.Model):
    CodObject = models.ForeignKey(Objects)
    
    Altitude = models.FloatField(null=True, blank=True)
    yaw = models.FloatField(null=True, blank=True)
    Pitch = models.FloatField(null=True, blank=True)
    Roll = models.FloatField(null=True, blank=True)
    Date = models.DateTimeField(auto_now_add=True, blank=True)
    Default = models.NullBooleanField(null=True, blank=True)  # Default camera when we open the map for the first time
    location = models.PointField()
    objects = models.GeoManager()

    def __unicode__(self):
        return unicode(self.CodCamera)


# This table saves the objects coordinates. If we have one object in form of square, we will need 4 points to complete the object design. Each point is made by 2 numbers(Lat,Long) (Graph theory).
# The altitude is not very important.
#class ObjectsCoordenates(models.Model):
 #   CodObject = models.ForeignKey(Objects)
  #  Latitude = models.FloatField(null=True, blank=True)
  #  Longitude = models.FloatField(null=True, blank=True)
  #  Altitude = models.FloatField(null=True, blank=True)
  #  Extrude = models.FloatField(null=True, blank=True)
  #  Date = models.DateTimeField(auto_now_add=True, blank=True)

   # def __unicode__(self):
   #     return unicode(self.CodCoordinate)


# We will need to know who is the user that is making changes in the databese(date,time, hour and which change he performed)
class InsertDeleteUpdate(models.Model):
    IdObject = models.BigIntegerField(null=True, blank=True)
    UserId = models.BigIntegerField(null=True, blank=True)
    PerformedActivity = models.CharField(max_length=50, null=True, blank=True)
    Date = models.DateTimeField(auto_now_add=True, blank=True)

    def __unicode__(self):
        return unicode(self.IdObject)


# This table will save all login informations for raspberryPi that we have in network. For easy SSH Connection
class Servers(models.Model):
    CodServer = models.ForeignKey(Objects)
    Ip = models.CharField(max_length=45, null=True, blank=True)
    UserName = models.CharField(max_length=45, null=True, blank=True)
    Password = models.CharField(max_length=45, null=True, blank=True)
    Port = models.IntegerField(null=True, blank=True)
    Date = models.DateTimeField(auto_now_add=True, blank=True)
    geometry = models.PolygonField() # The exactly geometry of the server
    def __unicode__(self):
        return unicode(self.CodServer)


# Default configurations. First map
class MapSettings(models.Model):
    ImageryProvider = models.CharField(max_length=300, null=True, blank=True)
    Url = models.CharField(max_length=300, null=True, blank=True)
    BaseLayerPick = models.NullBooleanField()

    def __unicode__(self):
        return unicode(self.ImageryProvider)




# TblFloors represent the building floors. Every floor is part of one building
class Floors(models.Model):
    codBuilding = models.ForeignKey(Buildings)
    FloorName = models.CharField(max_length=50)
    Description = models.CharField(max_length=5000, null=True, blank=True)
    #Password = models.CharField(max_length=45, null=True,
   #                             blank=True)  # TO ACTIVATE, DEACTIVATE, OR CHANGE THE VALUE OF OBJECT WE NEED TO INSERT THE OBJECT PASSWORD. Imagine someone switching off your Conditional Air!.. :)
    # As Entity.
    Picture = models.ImageField(upload_to='fotos/%Y/%m/%d', null=True, blank=True)  # Pop-Up image
    MaterialImage = models.ImageField(upload_to='fotos/%Y/%m/%d', null=True, blank=True)  # Material image
    MaterialColor = models.CharField(max_length=45, null=True, blank=True)
    UserId = models.ForeignKey(Users)
    Date = models.DateTimeField(auto_now_add=True, blank=True)
    Altitude = models.FloatField(null=True, blank=True)
    location = models.PointField() # The location is the  left botton corner of the building
    geometry = models.PolygonField() # The exactly geometry of the floor
    search_fields = ('location', 'geometry' )
    objects = models.GeoManager()
    def __unicode__(self):
        return unicode(self.FloorName)





# Configuring the geoadmin default data
class GeoModelAdmin(admin.GeoModelAdmin):
    admin.GeoModelAdmin.default_zoom = 5
    admin.GeoModelAdmin.default_lon = 95.58
    admin.GeoModelAdmin.default_lat = 80.52
    admin.GeoModelAdmin.map_template = 'admin/openlayers.html'
    admin.GeoModelAdmin.openlayers_url= 'http://dev.openlayers.org/OpenLayers.js'



# Each floor has a lot os coordinates that are a part of them. we need the coordinates to design the floor
#class FloorsCoordinates(models.Model):
 #   Building = models.ForeignKey(Buildings)
  #  Floor = models.ForeignKey(Floors)
  #  Latitude = models.FloatField(null=True, blank=True)
  #  Longitude = models.FloatField(null=True, blank=True)
  #  Altitude = models.FloatField(null=True, blank=True)
  #  Extrude = models.FloatField(null=True, blank=True)
  #  Date = models.DateTimeField(auto_now_add=True, blank=True)

   # def __unicode__(self):
   #     return unicode(self.Floor)


# Every floor has rooms
#class RoomsCoordinates(models.Model):
#    Building = models.ForeignKey(Buildings)
#    Floor = models.ForeignKey(Floors)
#    RoomName = models.ForeignKey(Rooms)
#    Latitude = models.FloatField(null=True, blank=True)
#    Longitude = models.FloatField(null=True, blank=True)
 #   Altitude = models.FloatField(null=True, blank=True)
#    Extrude = models.FloatField(null=True, blank=True)
 #   Date = models.DateTimeField(auto_now_add=True, blank=True)

#    def __unicode__(self):
#        return unicode(self.RoomName)
