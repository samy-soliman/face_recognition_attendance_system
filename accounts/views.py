from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from accounts.models import Company , Instructor
import os
from django.http import HttpResponse,JsonResponse

def register(request):
    
    if request.method == 'POST':
        # Get form values
        company_name = request.POST['company_name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        
        if (not company_name) or (not email) or (not phone) or (not password):
            return JsonResponse({
                        'message':"please fill in the form",
                        'type':"error",
                    })
        
        # Check username
        if User.objects.filter(username=company_name).exists():
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
                # create companiesRelatedFiles which will containg embeddings folder and photos
                companiesRelatedFilesPath = os.getcwd() + r'/companiesRelatedFiles'
                # create the embeddings folder that will contain embeddings for each company
                # it is created with the first company then it checks if exists to make it or not and it should be exits
                embeddingsPath = companiesRelatedFilesPath + r'/embeddings'
                # create the students photos folder that will contain photos for each company
                # it is created with the first company then it checks if exists to make it or not and it should be exits
                studentsPhotosPath = companiesRelatedFilesPath + r'/studentsPhotos'
                # create the lectures photos folder that will contain photos for each company
                # it is created with the first company then it checks if exists to make it or not and it should be exits
                lecturesPhotosPath = companiesRelatedFilesPath + r'/lecturesPhotos'
                # create the company folder inside the embeddings , photos folder , it will have company name
                # we check if the folders exist for safety
                companyEmbeddingsPath = embeddingsPath + r'/' +company_name
                companyStudentsPhotosPath = studentsPhotosPath + r'/' +company_name
                companyLecturesPhotosPath = lecturesPhotosPath + r'/' +company_name
                try:
                    if not (os.path.isdir( companiesRelatedFilesPath)):
                        os.mkdir( companiesRelatedFilesPath )
                        if not (os.path.isdir( embeddingsPath)):
                            os.mkdir( embeddingsPath )
                            if not (os.path.isdir( studentsPhotosPath)):
                                os.mkdir( studentsPhotosPath )
                                if not (os.path.isdir( lecturesPhotosPath)):
                                    os.mkdir( lecturesPhotosPath )

                    if not (os.path.isdir(companyEmbeddingsPath)):
                        os.mkdir(companyEmbeddingsPath)
                        if not (os.path.isdir(companyStudentsPhotosPath)):
                            os.mkdir(companyStudentsPhotosPath)
                            if not (os.path.isdir(companyLecturesPhotosPath)):
                                os.mkdir(companyLecturesPhotosPath)
                                
                                # Looks good
                                user = User.objects.create_user(username=company_name, password=password,email=email)
                                user.save()

                                company = Company(user=user, name=company_name, email=email, phone=phone,
                                embeddingsPath=companyEmbeddingsPath,studentsPhotosPath=companyStudentsPhotosPath,
                                lecturesPhotosPath=companyLecturesPhotosPath)

                                company.save()

                                return JsonResponse({
                                    'type':"success",
                                    'url':"login", 
                                })
                except:
                    # get user and company objects if exist to delete them in case of an error 
                    user = User.objects.get(username=company_name, password=password,email=email)
                    company = Company.objects.get(user=user, name=company_name, email=email, phone=phone)

                    if user is not None:
                        user.delete()
                    if company is not None:
                        company.delete()
                        # delete company associated filess
                        shutil.rmtree(companyEmbeddingsPath, ignore_errors=False, onerror=None)
                        shutil.rmtree(companyStudentsPhotosPath, ignore_errors=False, onerror=None)
                        shutil.rmtree(companyLecturesPhotosPath, ignore_errors=False, onerror=None)
                    
                    return render(request, 'error/error.html')
    else:
        return render(request, 'accounts/register.html')



def login(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if (not email) or (not password):
            return JsonResponse({
                        'message':"please fill in the form",
                        'type':"error",
                    })

        if User.objects.filter(email=email).exists():
            user_name= (User.objects.get(email=email)).username
            
        else:
            return JsonResponse({
                            'message':"information in not valid",
                            'type':"error",
                        })

        if User.objects.filter(username=user_name).exists():
            user = auth.authenticate(username=user_name, password=password) 
            if user is not None:
                auth.login(request, user)
                return JsonResponse({
                            'url':"index",
                            'type':"success",
                        })
            else:
                return JsonResponse({
                            'message':"information in not valid",
                            'type':"error",
                        })
        else:
            return JsonResponse({
                            'message':"please register in first",
                            'type':"error",
                        })

    else:
        return render(request, 'accounts/login.html')


def logout(request):
  if request.method == 'POST':
    auth.logout(request)
    return redirect('index')