from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BookingCounterAgent(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
         return str(self.id)+'_'+self.name

class ParkingZoneAssitant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
         return str(self.id)+'_'+self.name