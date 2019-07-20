from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from accounts.models import Company , Instructor
from manager.models import Grade , Student , Course
import os ,json , pickle
from django.http import HttpResponse ,JsonResponse
import re
from binascii import a2b_base64
from .encodefaces import encodeFaces

def manage(request):
    if request.user.is_authenticated:
        try:
            company_user = request.user.company
        except:
            return render(request, 'error/error.html')

        if request.method == 'POST':
            manageType = request.POST['manageType']
            
            
            if manageType == 'addInstructor' :
                email = request.POST['email']
                username = request.POST['username']
                password = request.POST['password']

                if (not email) or (not username) or (not password):
                    return JsonResponse({
                        'message':"please fill in the form",
                        'type':"error",
                    })

                if User.objects.filter(username=username).exists():
                    return JsonResponse({
                        'message':"name already used",
                        'type':"error",
                    })
                else:
                    if User.objects.filter(email=email).exists():
                        return JsonResponse({
                        'message':"email already used",
                        'type':"error",
                    })
                    else:
                        instructor_user = User.objects.create_user(username=username, password=password,email=email)
                        instructor_user.save()

                        instructor = Instructor(user=instructor_user, idfk_company=company_user , name=username, email=email)
                        instructor.save()
                        return JsonResponse({
                        'type':"success",
                    })

            elif manageType == 'addGrade' :
                grade_Name = request.POST['gradeName']
                if not grade_Name :
                    return JsonResponse({
                        'message':"please fill in the form",
                        'type':"error",
                    })
                
                if Grade.objects.filter(idfk_company=company_user).filter(name=grade_Name).exists():
                    return JsonResponse({
                        'message':"Grade already exist",
                        'type':"error",
                    })
                else :
                    companyEmbeddingsPath = company_user.embeddingsPath
                    companyStudentsPhotosPath = company_user.studentsPhotosPath
                    companyLecturesPhotosPath = company_user.lecturesPhotosPath

                    gradeEmbeddingsPath = companyEmbeddingsPath + r'/' + grade_Name
                    gradeStudentsPhotosPath = companyStudentsPhotosPath + r'/' + grade_Name
                    gradeLecturesPhotosPath = companyLecturesPhotosPath + r'/' + grade_Name

                    if  not (os.path.isdir( gradeEmbeddingsPath)):
                        os.mkdir( gradeEmbeddingsPath )
                        if  not (os.path.isdir( gradeStudentsPhotosPath)):
                            os.mkdir( gradeStudentsPhotosPath )
                            if  not (os.path.isdir( gradeLecturesPhotosPath)):
                                os.mkdir( gradeLecturesPhotosPath )

                                initialknownEncodings = []
                                initialknownNames = []
                                initialEmbeddings = {"encodings": initialknownEncodings, "names": initialknownNames}
                                gradeEmbeddingsPath = gradeEmbeddingsPath + r'/' + grade_Name + '.pickle'
                                f = open(gradeEmbeddingsPath, "wb")
                                f.write(pickle.dumps(initialEmbeddings))
                                f.close()

                                grade = Grade(idfk_company = company_user, name = grade_Name,
                                embeddingsPath = gradeEmbeddingsPath,studentsPhotosPath=gradeStudentsPhotosPath,
                                lecturesPhotosPath=gradeLecturesPhotosPath)
                                
                                grade.save()
                                return JsonResponse({
                                    'type':"success"
                                    })
                    else:
                        return JsonResponse({
                        'message':"Error !!!",
                        'type':"error",
                    })

            elif manageType == 'addStudent':
                user_name = request.POST['username']
                grade_name = request.POST['grade']
                dataUrlsJson = request.POST['dataUrls']
                if (not user_name) or (not grade_name) or (not dataUrlsJson):
                    return JsonResponse({
                        'message':"please fill in the form",
                        'type':"error",
                    })

                data_Urls = json.loads(dataUrlsJson)

                studentGrade = Grade.objects.filter(idfk_company=company_user).get(name=grade_name)

                if Student.objects.filter(idfk_company=company_user).filter(idfk_grade=studentGrade).filter(name=user_name).exists():
                    return JsonResponse({
                        'message':"name already taken",
                        'type':"error",
                    })
                else :
                    
                    studentPhotosPath = studentGrade.studentsPhotosPath + r'/' + user_name
                    if  not (os.path.isdir( studentPhotosPath)):
                        os.mkdir( studentPhotosPath )

                        count = 0 
                        for dataurl in data_Urls:
                            count = count + 1
                            imgstr = re.search(r'base64,(.*)', dataurl).group(1)
                            binary = a2b_base64(imgstr)
                            output = open(studentPhotosPath + r'/' + str(count) + '.png', 'wb')

                            output.write(binary)
                            output.close()
                    
                        encodeFaces(studentPhotosPath,studentGrade.embeddingsPath)

                        student = Student(idfk_company=company_user,name=user_name,idfk_grade=studentGrade,photosPath=studentPhotosPath)
                        student.save()

                        return JsonResponse({
                            'type':"success",
                        })

            elif manageType == 'addCourse':
                name = request.POST['name']
                grade_name = request.POST['grade']
                instructor_name = request.POST['instructor']
                if (not name) or (grade_name == "Choose Grade...") or (instructor_name =="Choose instructor..."):
                    return JsonResponse({
                        'message':"please fill in the form",
                        'type':"error",
                    })
                

                instructor = Instructor.objects.filter(idfk_company = company_user).get(name=instructor_name)

                if Course.objects.filter(idfk_instructor__idfk_company=company_user).filter(name=name).exists():
                    return JsonResponse({
                        'message':"course already exist",
                        'type':"error",
                    })
                else :
                    grade = Grade.objects.filter(idfk_company = company_user).get(name=grade_name)
                                        
                    course = Course(idfk_instructor=instructor,name=name,idfk_grade=grade)
                    course.save()

                    return JsonResponse({
                        'type':"success",
                    })
        
        elif request.method == 'GET':

            companyGrades = Grade.objects.filter(idfk_company=company_user)
            comapnyInstructors = Instructor.objects.filter(idfk_company=company_user)
            context = {
                'companyGrades':companyGrades,
                'comapnyInstructors':comapnyInstructors,
            }
            return render(request, 'manager/manage.html',context)
    else:
        return render(request, 'error/error.html')

