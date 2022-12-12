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
                user_data = ParkingZoneAssitant.objects.all().filter(user=user)[0]
                logged_user = 'ParkingZoneAssitant'
            
            parking_zone_data = ParkingZone.objects.all()

            if len(parking_zone_data) > 0:
                space_a = ParkingSpace.objects.all().filter(parking_zone=parking_zone_data[0])
                space_b = ParkingSpace.objects.all().filter(parking_zone=parking_zone_data[1])
                space_c = ParkingSpace.objects.all().filter(parking_zone=parking_zone_data[2])
            #vehicle_registration_data = VehicleParking.objects.all()
            else:
                space_a,space_b,space_c = [],[],[]

            data = {
                'user' : user_data,
                'logged_user' : logged_user,
                'parking_zones' : parking_zone_data,
                'parking_spaces_a' : space_a,
                'parking_spaces_b' : space_b,
                'parking_spaces_c': space_c
                
            }

            return render(request,'dashboard/home.html',data)
        return redirect('/login/signin')

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

        ins = VehicleParking.objects.all().filter(parking_space = parking_space_ins).order_by('-id')[0]
        ins.status = "Released"

        ins.save()

        return redirect('/dashboard/home')


class Reports(View):
    def get(self,request):
        if request.user.is_authenticated:
            #user = User.objects.get(username=request.user)  
            html_date = ''
            searched_date = request.GET.get('date')
            if searched_date != None:
                filter_data = VehicleParking.objects.all().filter(booking_date_time__date=searched_date)
                html_date = searched_date
            else:
                today = str(date.today())
                filter_data = VehicleParking.objects.all().filter(booking_date_time__date=today)
                html_date = today
            
            parking_zones = ParkingZone.objects.all()

            zone_a_data = []
            for space in ParkingSpace.objects.all().filter(parking_zone=parking_zones[0]):
                vehicle_registations = filter_data.filter(parking_space=space)
                ins = ReportData()
                ins.parking_space = space.parking_space_title
                ins.booking_numbers = len(vehicle_registations)
                if space.status == 'Vacant':
                    ins.vehicle_parked = '0'
                else:
                    ins.vehicle_parked = '1'
                zone_a_data.append(ins)
            
            zone_b_data = []
            for space in ParkingSpace.objects.all().filter(parking_zone=parking_zones[1]):
                vehicle_registations = filter_data.filter(parking_space=space)
                ins = ReportData()
                ins.parking_space = space.parking_space_title
                ins.booking_numbers = len(vehicle_registations)
                if space.status == 'Vacant':
                    ins.vehicle_parked = '0'
                else:
                    ins.vehicle_parked = '1'
                zone_b_data.append(ins)

            zone_c_data = []
            for space in ParkingSpace.objects.all().filter(parking_zone=parking_zones[2]):
                vehicle_registations = filter_data.filter(parking_space=space)
                ins = ReportData()
                ins.parking_space = space.parking_space_title
                ins.booking_numbers = len(vehicle_registations)
                if space.status == 'Vacant':
                    ins.vehicle_parked = '0'
                else:
                    ins.vehicle_parked = '1'
                zone_c_data.append(ins)



            data = {
                'filter_data' : filter_data,
                'zone_a_data' : zone_a_data,
                'zone_b_data' : zone_b_data,
                'zone_c_data' :zone_c_data,
                'html_date' : html_date
            }

            return render(request,'dashboard/reports.html',data)
        return redirect('/signin')