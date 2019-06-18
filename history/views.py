from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from accounts.models import Company , Instructor
from manager.models import Grade , Student , Course ,Lecture , Attendance
import os ,json , pickle
from django.http import HttpResponse
import re
from binascii import a2b_base64
from datetime import date

# Create your views here.

def history(request):
    if request.user.is_authenticated:
        instructor_user = request.user.instructor
        company_user = instructor_user.idfk_company
        
        if request.method == 'POST':
            lectureName = request.POST['lecture']
            lecture = Lecture.objects.get(name=lectureName)

            allStudentsAttendance = Attendance.objects.filter(idfk_lecture=lecture) 

            context = {
                'allStudentsAttendance':allStudentsAttendance,
                'lectureName' :lectureName,
                'counter' : 0,
            }

            return render(request, 'history/sheet.html',context)


        if request.method == 'GET':
            lectures =  Lecture.objects.filter(idfk_course__idfk_instructor__idfk_company=company_user)
            context = {
                'lectures' : lectures,
            }
            return render(request, 'history/history.html',context)
    
    else:
        return HttpResponse('<h1>You need to log in as instructor !</h1>')
    