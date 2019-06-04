from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from accounts.models import Company , Instructor


def manage(request):
    if request.method == 'POST':
        manageType = request.POST['manageType']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        
        company_user = request.user.company
        
        if manageType == 'addInstructor' :
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
    else:
        print('rendering manage')
        return render(request, 'manager/manage.html')

