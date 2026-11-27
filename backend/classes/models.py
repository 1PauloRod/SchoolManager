from django.db import models
from subjects.models import Subject

class SchoolLevel(models.Model):
    stage = models.CharField()
    year = models.PositiveIntegerField()
    name = models.CharField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ["stage", "year"], 
                name="unique_school_level"
            )
        ]

"""
SchoolGrade
id: 15
stage: HIGH_SCHOOL
grade: 1
name: "1ª série"

        ↓

Class
id: 42
name: "1º EM A"
school_grade_id: 15
capacity: 35

----------------

SchoolLevel
────────────────────────────────
id   stage          year   name
1    FUNDAMENTAL_1   1     1º ano
2    FUNDAMENTAL_1   2     2º ano
...
5    FUNDAMENTAL_1   5     5º ano
6    FUNDAMENTAL_2   6     6º ano
...
9    FUNDAMENTAL_2   9     9º ano
10   HIGH_SCHOOL     1     1ª série
11   HIGH_SCHOOL     2     2ª série
12   HIGH_SCHOOL     3     3ª série

Class
────────────────────────────
id   name       school_level_id   capacity
1    1º A       1                  30
2    1º B       1                  30
3    2º A       2                  30
4    1º EM A    10                 35
5    2º EM A    11                 35
"""

class Class(models.Model):
    name = models.CharField()
    school_level_id = models.ForeignKey(SchoolLevel, 
                                        on_delete=models.CASCADE, 
                                        related_name="classes")
    capacity = models.PositiveIntegerField()
    
    subjects = models.ManyToManyField(Subject, 
                                      through="ClassSubject", 
                                      related_name="classes")
  
    
class ClassSubject(models.Model):
    
    class_id = models.ForeignKey(Class, 
                                 on_delete=models.CASCADE, 
                                 related_name='class_subject')
    
    subject = models.ForeignKey(Subject, 
                                on_delete=models.PROTECT, 
                                related_name="class_subjects")
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "class_id",
                    "subject"
                ],
                name="unique_class_subject"
            ),
        ]
    

class ClassSchedule(models.Model):
    
    class_subject = models.ForeignKey(
        ClassSubject, 
        on_delete = models.CASCADE, 
        related_name="schedules"
    )
    
    teacher = models.ForeignKey(
        "teachers.Teacher",
        on_delete=models.PROTECT,
        related_name="schedules"
    )
    
    weekday = models.PositiveSmallIntegerField(
        choices=[
            (1, "Segunda-feira"),
            (2, "Terça-feira"),
            (3, "Quarta-feira"),
            (4, "Quinta-feira"),
            (5, "Sexta-feira"),
            (6, "Sábado"),
        ]
    )

    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ["weekday", "start_time"]

        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    end_time__gt=models.F("start_time")
                ),
                name="valid_schedule_time"
            ),
        ]
