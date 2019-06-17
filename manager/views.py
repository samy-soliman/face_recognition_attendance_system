from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from accounts.models import Company , Instructor
from manager.models import Grade , Student , Course
import os ,json , pickle
from django.http import HttpResponse
import re
from binascii import a2b_base64
from .encodefaces import encodeFaces

def manage(request):
    if request.user.is_authenticated:
        company_user = request.user.company

        if request.method == 'POST':
            manageType = request.POST['manageType']
            
            
            if manageType == 'addInstructor' :
                email = request.POST['email']
                username = request.POST['username']
                password = request.POST['password']

                print('managing instructor')
                if User.objects.filter(username=username).exists():
                    print('filter 1')
                    return redirect('manage')
                else:
                    if User.objects.filter(email=email).exists():
                        print('filter 2')
                        return redirect('manage')
                    else:
                        instructor_user = User.objects.create_user(username=username, password=password,email=email)
                        instructor_user.save()

                        instructor = Instructor(user=instructor_user, idfk_company=company_user , name=username, email=email)
                        instructor.save()
                        print('instructor was added')
                        return redirect('manage')

            elif manageType == 'addGrade' :
                grade_Name = request.POST['gradeName']

                if Grade.objects.filter(idfk_company=company_user).filter(name=grade_Name).exists():
                    return redirect('manage')
                else :
                    companyEmbeddingsPath = company_user.embeddingsPath
                    companyPhotosPath = company_user.photosPath

                    gradeEmbeddingsPath = companyEmbeddingsPath + r'/' + grade_Name
                    gradephotosPath = companyPhotosPath + r'/' + grade_Name

                    if  not (os.path.isdir( gradeEmbeddingsPath)):
                        os.mkdir( gradeEmbeddingsPath )
                        if  not (os.path.isdir( gradephotosPath)):
                            os.mkdir( gradephotosPath )

                            initialknownEncodings = []
                            initialknownNames = []
                            initialEmbeddings = {"encodings": initialknownEncodings, "names": initialknownNames}
                            gradeEmbeddingsPath = gradeEmbeddingsPath + r'/' + grade_Name + '.pickle'
                            f = open(gradeEmbeddingsPath, "wb")
                            f.write(pickle.dumps(initialEmbeddings))
                            f.close()

                            grade = Grade(idfk_company = company_user, name = grade_Name, embeddingsPath = gradeEmbeddingsPath,photosPath=gradephotosPath)
                            grade.save()
                            return redirect('manage')
                    else:
                        return redirect('manage')

            elif manageType == 'addStudent':
                user_name = request.POST['username']
                grade_name = request.POST['grade']
                dataUrlsJson = request.POST['dataUrls']
                data_Urls = json.loads(dataUrlsJson)

                if Student.objects.filter(idfk_company=company_user).filter(name=user_name).exists():
                    return redirect('manage')
                else :
                    studentGrade = Grade.objects.filter(idfk_company=company_user).get(name=grade_name)
                    studentPhotosPath = studentGrade.photosPath + r'/' + user_name
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
                    return redirect('manage')

            elif manageType == 'addCourse':
                name = request.POST['name']
                grade_name = request.POST['grade']
                instructor_name = request.POST['instructor']
                
                if Course.objects.filter(idfk_company=company_user).filter(name=name).exists():
                    return redirect('manage')
                else :
                    grade = Grade.objects.filter(idfk_company = company_user).get(name=grade_name)
                    instructor = Instructor.objects.filter(idfk_company = company_user).get(name=instructor_name)
                    
                    course = Course(idfk_instructor=instructor,name=name,idfk_grade=grade)
                    course.save()

                    return redirect('manage')
        
        else:

            companyGrades = Grade.objects.filter(idfk_company=company_user)
            comapnyInstructors = Instructor.objects.filter(idfk_company=company_user)
            context = {
                'companyGrades':companyGrades,
                'comapnyInstructors':comapnyInstructors,
            }
            return render(request, 'manager/manage.html',context)
    else:
        return HttpResponse('<h1>You need to log in as admin !</h1>')

