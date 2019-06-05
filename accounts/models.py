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
  pathToEmpeddings = models.CharField(max_length=200,default="")
  def __str__(self):
    return self.name

class Instructor(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,primary_key=True, related_name='instructor')
  idfk_Company = models.ForeignKey(Company, on_delete=models.CASCADE, db_index = False)
  name = models.CharField(max_length=200)
  email = models.CharField(max_length=200)
  def __str__(self):
    return self.name
