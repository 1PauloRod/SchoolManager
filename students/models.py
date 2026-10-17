from django.db import models
from accounts.models import User

class Student(models.Model):
    student_id = models.OneToOneField(User, 
                                      on_delete=models.CASCADE, 
                                      related_name="student")
    mother_name = models.CharField()
    father_name = models.CharField()
    class_id = models.ForeignKey("classes.Class", 
                                     on_delete=models.CASCADE)
    status = models.CharField() #activate, locked, canceled, completed
    year = models.PositiveIntegerField()
    date_enrollment = models.DateField()