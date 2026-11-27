from django.db import models
from accounts.models import User
from django.utils import timezone

class Student(models.Model):
    student_id = models.OneToOneField(User, 
                                      on_delete=models.CASCADE, 
                                      related_name="student")
    mother_name = models.CharField()
    father_name = models.CharField()
    class_id = models.ForeignKey("classes.Class", 
                                     on_delete=models.SET_NULL, 
                                     null=True, 
                                     blank=True)
    status = models.CharField(default='new') #activate, locked, canceled, completed
    year = models.PositiveIntegerField()
    date_enrollment = models.DateField(default=timezone.localdate)