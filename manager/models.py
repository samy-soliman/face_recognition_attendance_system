from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings
from accounts.models import Company ,Instructor
# Create your models here.
# os.mkdir(os.getcwd()+ r'/embeddings/company')
 
class Grade(models.Model):
    idfk_company = models.ForeignKey(Company, on_delete=models.CASCADE, db_index =False,related_name='grades')
    name = models.CharField(max_length=200)
    embeddingsPath = models.CharField(max_length=200)
    photosPath = models.CharField(max_length=200)
    def __str__(self):
        return self.name


class Course(models.Model):
    idfk_instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, db_index =False)
    name = models.CharField(max_length=200)
    idfk_grade = models.ForeignKey(Grade, on_delete=models.CASCADE, db_index =False)
    def __str__(self):
        return self.name

class Student(models.Model):
    idfk_company = models.ForeignKey(Company, on_delete=models.CASCADE, db_index =False,related_name='students')
    name = models.CharField(max_length=200)
    idfk_grade = models.ForeignKey(Grade, on_delete=models.CASCADE, db_index =False)
    photosPath = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Lecture(models.Model):
    idfk_course = models.ForeignKey(Course, on_delete=models.CASCADE, db_index =False)
    createdAt = models.DateTimeField(auto_now_add=True)

class Attendance(models.Model):
    class Meta:
        unique_together = (('idfk_lecture', 'idfk_student'),)
    idfk_lecture = models.ForeignKey(Lecture,on_delete=models.CASCADE, db_index =False)
    idfk_student = models.ForeignKey(Student, on_delete=models.CASCADE, db_index =False)
    state = models.BooleanField() 

