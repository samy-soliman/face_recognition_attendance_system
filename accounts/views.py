from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from accounts.models import Company , Instructor

def register(request):
    
    if request.method == 'POST':
        # Get form values
        company_name = request.POST['company_name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']

        # Check username
        if User.objects.filter(username=company_name).exists():
            return redirect('register')
        else:
            if User.objects.filter(email=email).exists():
                return redirect('register')
                
            else:
    
                # Looks good
                user = User.objects.create_user(username=company_name, password=password,email=email)
                # Login after register
                # auth.login(request, user)
                # messages.success(request, 'You are now logged in')
                # return redirect('index')
                user.save()

                company = Company(user=user, name=company_name, email=email, phone=phone)
                company.save()

                return redirect('login')
    else:
        return render(request, 'accounts/register.html')



def login(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user_name= (User.objects.get(email=email)).username
        user = auth.authenticate(username=user_name, password=password)

        if user is not None:
            auth.login(request, user)
            if Company.objects.filter(user_id=user.id).exists():
                print('company related')
            else :
                print('not company related')
            print('success')
            return redirect('index')
        else:
            print('fail')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
  if request.method == 'POST':
    auth.logout(request)
    return redirect('index')