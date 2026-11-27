from .models import Class, ClassSchedule, ClassSubject
from .exceptions import ClassNotFoundError, ScheduleNotFoundError
from accounts.models import User
from students.models import Student
from teachers.models import Teacher
from students.exceptions import StudentNotFoundError
from rest_framework.exceptions import ValidationError
from teachers.exceptions import TeacherNotFoundError
from django.db import transaction


def getClass(class_id):
    try:
        class_details = Class.objects.get(id=class_id)
    except Class.DoesNotExist:
        raise ClassNotFoundError()
    
    return class_details
    
    
def deleteClass(class_id):
    try:
        class_details = Class.objects.get(id=class_id) 
    except Class.DoesNotExist:
        raise ClassNotFoundError() 
    
    class_details.delete()
    
    return class_details

def getStudentsClass(class_id):
    try:
        Class.objects.get(id=class_id)
    except Class.DoesNotExist:
        raise ClassNotFoundError()
    #Colocar mais exception de turma vazia

    return Student.objects.filter(class_id=class_id) 
    '''return User.objects.filter(
        student__class_id=class_id
    )'''
       
def getTeachersClass(class_id):
    try:
        Class.objects.get(id=class_id)
    except Class.DoesNotExist:
            raise ClassNotFoundError()
        #Colocar mais exception de turma vazia
    
    
    return Teacher.objects.filter(class_id=class_id)
    '''return User.objects.filter(
            teacher__class_id=class_id
        )'''
    
    
def addStudentToClass(class_id, student_id):
    
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        raise StudentNotFoundError()
    
    class_obj = getClass(class_id) 
    
    if student.class_id == class_obj:
        raise ValidationError("Aluno já pertence a esta turma.") #padronizar isso aqui
    
    student_count = Student.objects.filter(
        class_id=class_obj
    ).count()
    
    if student_count >= class_obj.capacity:
        raise ValidationError("Turma está cheia.") #padronizar isso aqui
    
    student.class_id = class_obj
    student.status = 'activate'
    class_obj.capacity-=1
    student.save() 
    class_obj.save()
    
    return student
        
        
def deleteStudentClass(student_id, class_id):
    
    try:
        student = Student.objects.get(id=student_id)
    
    except Student.DoesNotExist:
        raise StudentNotFoundError()
    
    class_obj = getClass(class_id)
    
    if not student:
        raise StudentNotFoundError()
    
    student.class_id = None
    class_obj.capacity+=1
    student.save()
    class_obj.save()
    
    return student



def addTeacherToClass(teacher_id, class_id):
    
    try:
        teacher = Teacher.objects.get(id=teacher_id)
    except Teacher.DoesNotExist:
        raise TeacherNotFoundError()
    
    class_obj = getClass(class_id)
    
    if teacher.class_id == class_obj:
        raise ValidationError("Professor já pertence a esta turma.")
    
    teacher.class_id = class_obj
    teacher.status = 'activate'
    teacher.save()
    
    return teacher


def deleteTeacherClass(teacher_id):
    
    try:
        teacher = Teacher.objects.get(id=teacher_id)
    except Teacher.DoesNotExist:
        raise TeacherNotFoundError()
    
    teacher.class_id = None
    teacher.save()
    
    return teacher
        
    
def getSchedules(class_id):
    try:
        schedules = ClassSchedule.objects.filter(
                    class_subject__class_id=class_id
                )
    except ClassSchedule.DoesNotExist:
        raise ScheduleNotFoundError()
    
    return schedules


@transaction.atomic
def addSchedule(class_id, teacher_id, class_subject_id, data):
    
    
    class_obj = getClass(class_id) 
    
    try:
        class_subject = ClassSubject.objects.get(
            id=class_subject_id, 
            class_id=class_obj
        )
    except ClassSubject.DoesNotExist:
        raise ValidationError("Disciplina não cadastrada na turma.")
    
    weekday = data['weekday']
    start_time = data['start_time']
    end_time = data['end_time']
    
    
            #=================================
            #
            #Implementar conflito
            #
            #=================================
            
    
    schedule = ClassSchedule.objects.create(
        class_subject=class_subject, 
        teacher_id=teacher_id, 
        weekday=weekday, 
        start_time=start_time, 
        end_time=end_time
    )
        
    return schedule
    