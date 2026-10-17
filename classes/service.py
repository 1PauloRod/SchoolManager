from .models import Class
from .exceptions import ClassNotFoundError
from accounts.models import User
from students.models import Student
from teachers.models import Teacher

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
    