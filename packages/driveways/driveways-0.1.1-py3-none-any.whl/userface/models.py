from django.contrib.gis.db import models
from django.contrib.auth.models import User
# Create your models here.




class Vehicle(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    plateNum = models.CharField(max_length=6, default=' ')

    def __str__(self):
        return self.make + " " + self.model

class ParkingSpot(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.PointField()
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.address


class Destination(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    location = models.PointField()
    city = models.CharField(max_length=50)


class UserLocation(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.PointField()

class UserDetails(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length = 20)