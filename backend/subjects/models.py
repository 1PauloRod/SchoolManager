from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=100)
    #description = models.CharField(max_length=300)
    code = models.CharField(unique=True, max_length=20)
    workload_hour = models.PositiveIntegerField(null=True, default=1)
    
