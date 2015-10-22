from django.db import models

# Create your models here
#We need to have informations about the person who is inserting, updating or deleting objects in database(Buildings,  sensors, conditional air, ect)
class Users(Models.model):
	Name = models.CharField(max_lenght=100)
	UserName = models.CharField(max_lenght = 100)
	Password = models.CharField(max_lenght = 100)
	def __unicode__(self):
		return unicode(self.UserId)

# Every objects will be in the same table (Buildings, Sensors, Conditional air and others objects that we can manipulate by CLICKING) 
class Objects(Models.model):
	objectId= models.CharField(max_lenght = 45)
	Type = models.CharField(max_lenght = 50)
	Name = models.CharField(max_lenght = 300)
	Description = models.CharField(max_lenght=5000)
	url = models.CharField(max_lenght=100,null=true,blank=true)
	Color = models.CharField(max_lenght = 45)
	Value = models.FloatField()
	Date = models.DataTimeField()
	UserId = models.ForeignKey(Users)
	Picture = models.ImageField(upload_to = 'fotos/%Y/%m/%d',null=True,blank=True)
	Password = models.CharField(max_lenght = 45) #TO ACTIVATE, DEACTIVATE, OR CHANGE THE VALUE OF OBJECT WE NEED TO INSERT THE OBJECT PASSWORD. Imagine someone switching off your Conditional Air!.. :)
	def __unicode__(self):
		return unicode(self.CodObject)



#This table saves the Camera configuration. Each object will have his own camera configuration. If we want to see a sensor in floor 5 of building #1, the camera needs to be closer in that object.
# Will be possible to define which camera is default. We will have 3 global camera(Code 1,100,100) One of them will be the pre-defined
class Camera(Models.model):
	CodObject = models.ForeignKey(Objects)
	Latitude = models.FloatField()
	Longitude = models.FloatField()
	Altitude = models.FloatField()
	Heading = models.FloatField()
	Pitch = models.FloatField()
	Roll = models.FloatField()
	Date = models.DataTimeField()
	Default = models.NullBooleanField()
	def __unicode__(self):
		return unicode(self.CodCamera)

#This table saves the objects coordinates. If we have one object in form of square, we will need 4 points to complete the object design. Each point is made by 2 numbers(Lat,Long) (Graph theory).
# The altitude is not very important.
class Coordenates(Models.model):
	CodObject = models.ForeignKey(Objects)
	Latitude = models.FloatField()
	Longitude = models.FloatField()
	Altitude = models.FloatField()
	Extrude = models.FloatField()
	Date = models.DataTimeField()
	def __unicode__(self):
		return unicode(self.CodCoordinate)

# We will need to know who is the user that is making changes in the databese(date,time, hour and which change he performed)
class InsertDeleteUpdate(Models.model):
	IdObject = models.BigIntegerField()
	UserId = models.BigIntegerField()
	PerformedActivity = models.CharField()
	Date = models.DataTimeField()
	def __unicode__(self):
		return unicode(self.IdObject)

#This table will save all login informations for raspberryPi that we have in network. For easy SSH Connection
class Servers(Model.models):
	CodServer = models.ForeignKey(Objects)
	Ip = models.CharField()
	UserName = models.CharField()
	Password = models.CharField()
	Port = models.IntegerField()









