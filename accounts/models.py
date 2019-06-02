from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

 
class Company(models.Model):
  user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
  name = models.CharField(max_length=200)
  email = models.CharField(max_length=200)
  phone = models.CharField(max_length=100)
  def __str__(self):
    return self.name

class Instructor(models.Model):
  user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
  idfk_Company = models.ForeignKey(Company, on_delete=models.CASCADE, db_index = False)
  name = models.CharField(max_length=200)
  email = models.CharField(max_length=200)
  def __str__(self):
    return self.name

class Student(models.Model):
  idfk_Company = models.ForeignKey(Company, on_delete=models.CASCADE, db_index =False)
  name = models.CharField(max_length=200)
  def __str__(self):
    return self.name
