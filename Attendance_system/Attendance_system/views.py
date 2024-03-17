from http.client import responses
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from datetime import date
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
import os
import datetime

import cv2



def index(request):
    if request.user.is_authenticated:
           return render(request ,'employeeinfo.html')
    return render(request ,'signup.html')


# def dashboard(request):
#     if request.user.is_authenticated:
#            return redirect("employeeinfo")
#     return render(request ,'signup.html')



def loginemployee(request):
       if request.user.username == 'admin' :
           return redirect("adminpanel")
       if request.user.is_authenticated:
           return redirect('index')  #return

       if request.method =="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not User.objects.filter(email = email).exists():
            messages.error(request,"Email does not exist.")
            return redirect("loginemployee")
        else:
            username = User.objects.get(email=email).username
            employee_id = User.objects.get(email=email).id
            data = {
                'username':username,
                'email':email,
                'employee_id' : employee_id,
            }
            Employee  = User.objects.get(email = email)
            print(password)
            print(Employee.password)

            if(Employee.password  == password ):
                request.session['Employeedata'] = data
                login(request,Employee)
                messages.info( request,'login successfully')
                return redirect("index")
            else : 
                messages.info( request,'Incorect pass word or email')
                return redirect("loginemployee")
            
       return render(request,'login.html')


def signupemployee(request):
    if request.user.is_authenticated:
           return redirect("employeeinfo")
    if request.method =="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword =request.POST.get('cpassword')
        username = request.POST.get('username')
        print(email,password)
        Employee = User.objects.filter(email = email).exists()
        if(Employee):
            messages.warning(request, 'email already exists.')
            return redirect("signupemployee")
        if password == cpassword:
            Employee = User.objects.create(username = username,email =  email,password = password)
            messages.info( request,'signup successfully')
            return redirect("loginemployee")
        else:
            messages.warning(request,'Passwords do not match')
            return redirect("signupemployee")
    return render(request,'signup.html')



def logoutmployee(request):
    logout(request)
    return redirect('index')



def generateframe():
    camera = cv2.Videocapture(0) 
    while  True:
        success , frame = camera.read()
        if not success : 
            break
        else:
            ret,buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n'+frame + b'\r\n')
        


def adminpanel(request):
    return render(request ,'adminsystem.html')

def getframe(request):
    return responses(generateframe, mimetype = 'multipart/x-mixed-replace; boundery= frame')

