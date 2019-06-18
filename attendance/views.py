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
from .faceRecognition.detect_faces import detectFaces
import datetime

# Create your views here.

def attendance(request):
    if request.user.is_authenticated:
        instructor_user = request.user.instructor
        company_user = instructor_user.idfk_company

        if request.method == 'POST':
            course_name = request.POST['course']
            dataURLJson = request.POST['dataURL']
            dataURL = json.loads(dataURLJson)

            course= Course.objects.filter(idfk_instructor__idfk_company=company_user).get(name=course_name)
            courseGrade = course.idfk_grade
            gradeEmbeddingsPath = courseGrade.embeddingsPath

            today = str(date.today())
            lecturePhotoPath = courseGrade.lecturesPhotosPath + r'/' + ( course_name + today)
            imgstr = re.search(r'base64,(.*)', dataURL).group(1)
            binary = a2b_base64(imgstr)
            output = open(lecturePhotoPath + '.png', 'wb')
            output.write(binary)
            output.close()

            now = datetime.datetime.now()
            lectureName = course_name + str(now.year)+ '-' + str(now.month) + '-' +str(now.day) + '-' + str(now.hour) 
            lecture = Lecture(name=lectureName,idfk_course=course, lecturePhotoPath=lecturePhotoPath)
            lecture.save()

            # starting recognition

            attendantStudentsList = detectFaces(lecturePhotoPath+'.png', gradeEmbeddingsPath)
            attendantStudentsNames = set(attendantStudentsList)
            allStudents = Student.objects.filter(idfk_grade =courseGrade )
    
            for student in allStudents:
                if(student.name in attendantStudentsNames):
                    attendance = Attendance(idfk_lecture=lecture,idfk_student=student,state= True)
                    attendance.save()
                    attendantStudentsNames.remove(student.name)
                else:
                    attendance = Attendance(idfk_lecture=lecture,idfk_student=student,state= False)
                    attendance.save()
            
            return redirect('attendance')


        if request.method == 'GET':
            courses =  Course.objects.filter(idfk_instructor=instructor_user)
            context = {
                'courses' : courses,
            }
            return render(request, 'attendance/attendance.html',context)
    
    else:
        return HttpResponse('<h1>You need to log in as instructor !</h1>')
    