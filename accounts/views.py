from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from accounts.models import Company , Instructor
import os

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
                user.save()

                # create the embeddings folder that will contain embeddings for each company
                # it is created with the first company then it checks if exists to make it or not and it should be exits
                basePathToEmbeddings = os.getcwd() + r'/embeddings'
                if not (os.path.isdir( basePathToEmbeddings)):
                    os.mkdir( basePathToEmbeddings )     
                # create the company folder inside the embeddings folder , it will have company name
                # we check if it exist for safety
                companyToPathEmbeddings = basePathToEmbeddings + r'/' +company_name
                if not (os.path.isdir(companyToPathEmbeddings)):
                    os.mkdir(companyToPathEmbeddings)

                    company = Company(user=user, name=company_name, email=email, phone=phone,pathToEmpeddings=companyToPathEmbeddings)
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