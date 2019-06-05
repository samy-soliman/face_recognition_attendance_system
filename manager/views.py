from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from accounts.models import Company , Instructor
from manager.models import Grade
import os

def manage(request):
    if request.method == 'POST':
        manageType = request.POST['manageType']

        company_user = request.user.company
        
        
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

                    instructor = Instructor(user=instructor_user, idfk_Company=company_user , name=username, email=email)
                    instructor.save()
                    print('instructor was added')
                    return redirect('manage')

        elif manageType == 'addGrade' :
            grade_Name = request.POST['gradeName']

            if Grade.objects.filter(idfk_company=company_user).filter(name=grade_Name).exists():
                return redirect('manage')
            else :
                companyToPathEmbeddings = company_user.pathToEmpeddings
                gradePathToEmbeddings = companyToPathEmbeddings + r'/' + grade_Name
                if  not (os.path.isdir( gradePathToEmbeddings)):
                    os.mkdir( gradePathToEmbeddings )

                    grade = Grade(idfk_company = company_user, name = grade_Name, pathToEmpeddings = gradePathToEmbeddings)
                    grade.save()
                    return redirect('manage')
                else:
                    return redirect('manage')

    else:
        print('rendering manage')
        return render(request, 'manager/manage.html')

