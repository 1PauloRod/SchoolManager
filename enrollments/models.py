from django.db import models
from accounts.models import User

'''
class Enrollment(models.Model):
    student_id = models.ForeignKey(User, 
                                   on_delete=models.CASCADE,
                                 related_name="enrollment")
    class_id = models.ForeignKey("classes.Class", 
                                 on_delete=models.CASCADE)
    status = models.CharField() #activate, locked, canceled, completed
    year = models.PositiveIntegerField()
    date_enrollment = models.DateField()
    '''
    