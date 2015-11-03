from django.db import models

# Create your models here
#We need to have informations about the person who is inserting, updating or deleting objects in database(Buildings,  sensors, conditional air, ect)
class ObjectsType(models.Model):
	TypeObj = models.CharField(max_length = 50,null=True,blank=True)
	def __unicode__(self):
		return unicode(self.TypeObj)

class Users(models.Model):
	Name = models.CharField(max_length=100)
	UserName = models.CharField(max_length = 100,null=True,blank=True)
	Password = models.CharField(max_length = 100,null=True,blank=True)
	def __unicode__(self):
		return unicode(self.Name)

# Every objects will be in the same table (Buildings, Sensors, Conditional air and others objects that we can manipulate by CLICKING) 
class Objects(models.Model):
	TypeObj = models.ForeignKey(ObjectsType)
	Name = models.CharField(max_length = 300,null=True,blank=True)
	Description = models.CharField(max_length=5000,null=True,blank=True)
	url = models.FileField(upload_to = 'fotos/%Y/%m/%d',null=True,blank=True)
	Value = models.FloatField(null=True,blank=True)
	UserId = models.ForeignKey(Users)
	Password = models.CharField(max_length = 45,null=True,blank=True) #TO ACTIVATE, DEACTIVATE, OR CHANGE THE VALUE OF OBJECT WE NEED TO INSERT THE OBJECT PASSWORD. Imagine someone switching off your Conditional Air!.. :)
	Floors = models.IntegerField(null=True,blank=True) # To use in pop-up of the object
	#As Entity.
	PositionLat = models.FloatField(null=True,blank=True)
	PositionLong = models.FloatField(null=True,blank=True)
	Picture = models.ImageField(upload_to = 'fotos/%Y/%m/%d',null=True,blank=True) #Pop-Up image
	MaterialImage = models.ImageField(upload_to = 'fotos/%Y/%m/%d',null=True,blank=True) # Material image
	MaterialColor = models.CharField(max_length = 45,null=True,blank=True)
	Date = models.DateTimeField(auto_now_add=True,blank=True)
	

	def __unicode__(self):
		return unicode(self.Name)



#This table saves the Camera configuration. Each object will have his own camera configuration. If we want to see a sensor in floor 5 of building #1, the camera needs to be closer in that object.
# Will be possible to define which camera is default. We will have 3 global camera(Code 1,100,100) One of them will be the pre-defined
class Camera(models.Model):
	CodObject = models.ForeignKey(Objects)
	Latitude = models.FloatField(null=True,blank=True)
	Longitude = models.FloatField(null=True,blank=True)
	Altitude = models.FloatField(null=True,blank=True)
	yaw = models.FloatField(null=True,blank=True)
	Pitch = models.FloatField(null=True,blank=True)
	Roll = models.FloatField(null=True,blank=True)
	Date = models.DateTimeField(auto_now_add=True,blank=True)
	Default = models.NullBooleanField(null=True,blank=True) #Default camera when we open the map for the first time
	def __unicode__(self):
		return unicode(self.CodCamera)

#This table saves the objects coordinates. If we have one object in form of square, we will need 4 points to complete the object design. Each point is made by 2 numbers(Lat,Long) (Graph theory).
# The altitude is not very important.
class ObjectsCoordenates(models.Model):
	CodObject = models.ForeignKey(Objects)
	Latitude = models.FloatField(null=True,blank=True)
	Longitude = models.FloatField(null=True,blank=True)
	Altitude = models.FloatField(null=True,blank=True)
	Extrude = models.FloatField(null=True,blank=True)
	Date = models.DateTimeField(auto_now_add=True,blank=True)
	def __unicode__(self):
		return unicode(self.CodCoordinate)

# We will need to know who is the user that is making changes in the databese(date,time, hour and which change he performed)
class InsertDeleteUpdate(models.Model):
	IdObject = models.BigIntegerField(null=True,blank=True)
	UserId = models.BigIntegerField(null=True,blank=True)
	PerformedActivity = models.CharField(max_length = 50,null=True,blank=True)
	Date = models.DateTimeField(auto_now_add=True,blank=True)
	def __unicode__(self):
		return unicode(self.IdObject)

#This table will save all login informations for raspberryPi that we have in network. For easy SSH Connection
class Servers(models.Model):
	CodServer = models.ForeignKey(Objects)
	Ip = models.CharField(max_length = 45,null=True,blank=True)
	UserName = models.CharField(max_length = 45,null=True,blank=True)
	Password = models.CharField(max_length = 45,null=True,blank=True)
	Port = models.IntegerField(null=True,blank=True)
	Date = models.DateTimeField(auto_now_add=True,blank=True)
	def __unicode__(self):
		return unicode(self.CodServer)

#Default configurations. First map
class MapSettings(models.Model):
	ImageryProvider = models.CharField(max_length=300,null=True,blank=True)
	Url = models.CharField(max_length=300,null=True,blank=True)
	BaseLayerPick = models.NullBooleanField()
	def __unicode__(self):
		return unicode(self.ImageryProvider)


# Just buldings in this table
class Buildings(models.Model):
	Name = models.CharField(max_length = 300,null=True,blank=True)
	Description = models.CharField(max_length=5000,null=True,blank=True)
	url = models.FileField(upload_to = 'fotos/%Y/%m/%d',null=True,blank=True)
	Value = models.FloatField(null=True,blank=True)
	Date = models.DateTimeField(auto_now_add=True,blank=True)
	UserId = models.ForeignKey(Users)
	Password = models.CharField(max_length = 45,null=True,blank=True) #TO ACTIVATE, DEACTIVATE, OR CHANGE THE VALUE OF OBJECT WE NEED TO INSERT THE OBJECT PASSWORD. Imagine someone switching off your Conditional Air!.. :)
	Floors = models.IntegerField(null=True,blank=True) # To use in pop-up of the object
	#As Entity.
	PositionLat = models.FloatField(null=True,blank=True)
	PositionLong = models.FloatField(null=True,blank=True)
	Picture = models.ImageField(upload_to = 'fotos/%Y/%m/%d',null=True,blank=True) #Pop-Up image
	MaterialImage = models.ImageField(upload_to = 'fotos/%Y/%m/%d',null=True,blank=True) # Material image
	MaterialColor = models.CharField(max_length = 45,null=True,blank=True)

	def __unicode__(self):
		return unicode(self.Name)


#TblFloors represent the building floors. Every floor is part of one building
class Floors(models.Model):
	codBuilding = models.ForeignKey(Buildings)
	FloorName= models.CharField(max_length=50)
	Description = models.CharField(max_length=5000,null=True,blank=True)
	Password = models.CharField(max_length = 45,null=True,blank=True) #TO ACTIVATE, DEACTIVATE, OR CHANGE THE VALUE OF OBJECT WE NEED TO INSERT THE OBJECT PASSWORD. Imagine someone switching off your Conditional Air!.. :)
	#As Entity.
	PositionLat = models.FloatField(null=True,blank=True)
	PositionLong = models.FloatField(null=True,blank=True)
	Picture = models.ImageField(upload_to = 'fotos/%Y/%m/%d',null=True,blank=True) #Pop-Up image
	MaterialImage = models.ImageField(upload_to = 'fotos/%Y/%m/%d',null=True,blank=True) # Material image
	MaterialColor = models.CharField(max_length = 45,null=True,blank=True)
	UserId = models.ForeignKey(Users)
	Date = models.DateTimeField(auto_now_add=True,blank=True)
	def __unicode__(self):
		return unicode(self.FloorName)

#Rooms represent the rooms. Every room is part of one floor
class Rooms(models.Model):
	codBuilding = models.ForeignKey(Buildings)
	codBuilding = models.ForeignKey(Floors)
	RoomName= models.CharField(max_length=50)
	Description = models.CharField(max_length=5000,null=True,blank=True)
	url = models.FileField(upload_to = 'fotos/%Y/%m/%d',null=True,blank=True)
	Password = models.CharField(max_length = 45,null=True,blank=True) #TO ACTIVATE, DEACTIVATE, OR CHANGE THE VALUE OF OBJECT WE NEED TO INSERT THE OBJECT PASSWORD. Imagine someone switching off your Conditional Air!.. :)
	#As Entity.
	PositionLat = models.FloatField(null=True,blank=True)
	PositionLong = models.FloatField(null=True,blank=True)
	Picture = models.ImageField(upload_to = 'fotos/%Y/%m/%d',null=True,blank=True) #Pop-Up image
	MaterialImage = models.ImageField(upload_to = 'fotos/%Y/%m/%d',null=True,blank=True) # Material image
	MaterialColor = models.CharField(max_length = 45,null=True,blank=True)
	UserId = models.ForeignKey(Users)
	Date = models.DateTimeField(auto_now_add=True,blank=True)
	def __unicode__(self):
		return unicode(self.RoomName)
#Each floor has a lot os coordinates that are a part of them. we need the coordinates to design the floor
class FloorsCoordinates(models.Model):
	Building = models.ForeignKey(Buildings)
	Floor = models.ForeignKey(Floors)
	Latitude = models.FloatField(null=True,blank=True)
	Longitude = models.FloatField(null=True,blank=True)
	Altitude = models.FloatField(null=True,blank=True)
	Extrude = models.FloatField(null=True,blank=True)
	Date = models.DateTimeField(auto_now_add=True,blank=True)
	def __unicode__(self):
		return unicode(self.Floor)

#Every floor has rooms
class RoomsCoordinates(models.Model):
	Building = models.ForeignKey(Buildings)
	Floor = models.ForeignKey(Floors)
	RoomName = models.ForeignKey(Rooms)
	Latitude = models.FloatField(null=True,blank=True)
	Longitude = models.FloatField(null=True,blank=True)
	Altitude = models.FloatField(null=True,blank=True)
	Extrude = models.FloatField(null=True,blank=True)
	Date = models.DateTimeField(auto_now_add=True,blank=True)
	def __unicode__(self):
		return unicode(self.CodFloors)


















