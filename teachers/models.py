from django.db import models
from accounts.models import User


class Teacher(models.Model):
    teacher_id = models.OneToOneField(User, 
                                   on_delete=models.CASCADE, 
                                   related_name="teacher")
    class_id = models.ForeignKey('classes.Class',
                                 on_delete=models.CASCADE)
    specialty= models.CharField() 
    