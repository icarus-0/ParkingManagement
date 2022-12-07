from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User, auth
from django.views import View
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime,timedelta,date

class HomePage(View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request,'dashboard/home.html')
        return redirect('/signin')

    def post(self,request):
        pass
