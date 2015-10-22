from django.db import models

# Create your models here
#We need to have informations about the person who is inserting, updating or deleting objects in database(Buildings,  sensors, conditional air, ect)
class Users(Models.model):
	UserId = models.AutoField()
	Name = models.CharField(max_lenght=100)
	UserName = models.CharField()
	Password = models.CharField()
	def __unicode__(self):
		return unicode(self.UserId)

# Every objects will be in the same table (Buildings, Sensors, Conditional air and others objects that we can manipulate by CLICKING) 
class Objects(Models.model):
	CodObject = models.AutoField()
	objectId= models.CharField(max_lenght = 45)
	Type = models.CharField(max_lenght = 50)
	Name = models.CharField(max_lenght = 300)
	Description = models.CharField(max_lenght=5000)
	url = models.CharField(max_lenght=100,null=true,blank=true)
	Color = models.CharField()
	value = FloatField()
	Picture = models.ImageField(upload_to = 'fotos/', default = 'fotos/no-img.jpg')
	Date = models.DataTimeField()
	UserId = models.ForeignKey(Users)
	def __unicode__(self):
		return unicode(self.CodObject)



#This table saves the Camera configuration. Each object will have his own camera configuration. If we want to see a sensor in floor 5 of building #1, the camera needs to be closer in that object.
# Will be possible to define which camera is default. We will have 3 global camera(Code 1,100,100) One of them will be the pre-defined
class Camera(Models.model):
	CodCamera = models.AutoField()
	CodObject = models.BigIntegerField()
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
	CodCoordinate= models.AutoField()
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








