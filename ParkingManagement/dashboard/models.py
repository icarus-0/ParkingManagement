from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ParkingZone(models.Model):
    id = models.AutoField(primary_key=True)
    parking_zone_title = models.CharField(max_length=100)
    def __str__(self):
         return str(self.id)+'_'+self.parking_zone_title


class ParkingSpace(models.Model):
    id = models.AutoField(primary_key=True)
    parking_space_title = models.CharField(max_length=100)
    parking_zone = models.ForeignKey(ParkingZone,on_delete=models.CASCADE)
    status = models.CharField(max_length=15,default='Vacant')
    vehicle_parked = models.CharField(max_length=50,null=True)
    def __str__(self):
         return str(self.id)+'_'+self.parking_space_title

class VehicleParking(models.Model):
    id = models.AutoField(primary_key=True)
    parking_zone = models.ForeignKey(ParkingZone,on_delete=models.CASCADE)
    parking_space = models.ForeignKey(ParkingSpace,on_delete=models.CASCADE)
    booking_date_time = models.DateTimeField(auto_now_add=True)
    release_date_time = models.DateTimeField(auto_now=True)
    vehicle_registration_number = models.CharField(max_length=50)
    status = models.CharField(max_length=15,default='Parked')
    
    def __str__(self):
         return str(self.id)+'_'+self.vehicle_registration_number

class ReportData:
    parking_space :str
    booking_numbers : str
    vehicle_parked : str