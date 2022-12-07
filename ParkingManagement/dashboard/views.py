from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User, auth
from django.views import View
from .models import *
from login.models import *
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime,timedelta,date

class HomePage(View):
    def get(self,request):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)

            ins = BookingCounterAgent.objects.all().filter(user=user)

            if len(ins) != 0:
                user_data = ins[0]
                logged_user = 'BookingCounterAgent'
            else:
                user_data = ins[0]
                logged_user = 'ParkingZoneAssitant'
            
            parking_zone_data = ParkingZone.objects.all()
            space_a = ParkingSpace.objects.all().filter(parking_zone=parking_zone_data[0])
            space_b = ParkingSpace.objects.all().filter(parking_zone=parking_zone_data[1])
            space_c = ParkingSpace.objects.all().filter(parking_zone=parking_zone_data[2])
            #vehicle_registration_data = VehicleParking.objects.all()

            data = {
                'user' : user_data,
                'logged_user' : logged_user,
                'parking_zones' : parking_zone_data,
                'parking_spaces_a' : space_a,
                'parking_spaces_b' : space_b,
                'parking_spaces_c': space_c
                
            }

            return render(request,'dashboard/home.html',data)
        return redirect('/signin')

    def post(self,request):
        pass

class InitializeParkingData(View):
    def post(self,request):
        parking_zone_data = ['Parking Zone A','Parking Zone B','Parking Zone C']
        bulk_query_zone = []

        for i in parking_zone_data:
            ins = ParkingZone(
                parking_zone_title = i
            )
            bulk_query_zone.append(ins)
        
        ParkingZone.objects.bulk_create(bulk_query_zone)
       

        bulk_query_space = []

        for i in ParkingZone.objects.all():
            for j in range(1,11):
                ins = ParkingSpace(
                    parking_space_title = 'Parking Space '+str(j),
                    parking_zone = i
                )
                bulk_query_space.append(ins)
        ParkingSpace.objects.bulk_create(bulk_query_space)
        

        return redirect('/dashboard/home')

class BookParkingSpace(View):
    def post(self,request):
        parking_space_id = request.POST['parking_space_id']
        vehicle_number = request.POST['vehicle_number']

        parking_space_ins = ParkingSpace.objects.get(pk=parking_space_id)
        parking_space_ins.status = "Occupied"
        parking_space_ins.vehicle_parked = vehicle_number

        parking_space_ins.save()

        ins = VehicleParking(
            parking_zone = parking_space_ins.parking_zone,
            parking_space = parking_space_ins,
            vehicle_registration_number = vehicle_number,

        )

        ins.save()

        return redirect('/dashboard/home')

class ReleaseParkingSpace(View):
    def post(self,request):
        parking_space_id = request.POST['parking_space_id']

        parking_space_ins = ParkingSpace.objects.get(pk=parking_space_id)
        parking_space_ins.status = "Vacant"
        parking_space_ins.vehicle_parked = None

        parking_space_ins.save()

        ins = VehicleParking.objects.all().filter(parking_space = parking_space_ins).get()
        ins.status = "Released"

        ins.save()

        return redirect('/dashboard/home')