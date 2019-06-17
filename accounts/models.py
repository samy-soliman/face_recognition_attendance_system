from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
 
 
class Company(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,primary_key=True, related_name='company')
  name = models.CharField(max_length=200)
  email = models.CharField(max_length=200)
  phone = models.CharField(max_length=100)
  embeddingsPath = models.CharField(max_length=200,default="")
  studentsPhotosPath = models.CharField(max_length=200,default="")
  lecturesPhotosPath = models.CharField(max_length=200,default="")
  def __str__(self):
    return self.name

class Instructor(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,primary_key=True, related_name='instructor')
  idfk_company = models.ForeignKey(Company, on_delete=models.CASCADE, db_index = False,related_name='instructors')
  name = models.CharField(max_length=200)
  email = models.CharField(max_length=200)
  def __str__(self):
    return self.name
