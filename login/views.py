from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.views import View
from .models import *

# handle sign up page requests
class SignUp(View):
    def get(self,request):
        return render(request,'login/login.html')

    def post(self,request):
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['pass']
        re_password = request.POST['re_pass']

        if password == re_password:
            if not User.objects.filter(username=email).exists():
                if not User.objects.filter(email=email).exists():
                    user = User.objects.create_user(username=email,
                                                    password=password,
                                                    email=email,
                                                    first_name=name,
                                                    )
                                                    
                    user.save()
                    messages.info(request,'Successfully resigtered ..')
                    return redirect('/login/signin')
                else:
                    messages.error(request,'This email is already registered')
                    return redirect('/login/signup')
            else:
                messages.error(request,'Username is already present')
                return redirect('/login/signup')
        else:
            messages.error(request,'Password not matched')
            return redirect('/login/signup')

    

# handle sign in page requets
class SignIn(View):

    def get(self,request):
        return render(request,'login/sign-in.html')

    def post(self,request):
        username = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/dashboard')
        else:
            messages.error(request,'Invalid credientials')
            return redirect('/login/signin')


# handle logout
def logout(request):
    auth.logout(request)
    return redirect('/login/signin')


