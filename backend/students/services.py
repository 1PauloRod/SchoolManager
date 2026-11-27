from .models import Student
from .exceptions import StudentNotFoundError

def getStudent(student_id):
    try: 
        student = Student.objects.get(id=student_id)
        
    except Student.DoesNotExist():
        raise StudentNotFoundError()
    
    return student


def deleteStudent(student_id):
    try: 
        student = Student.objects.get(id=student_id)
            
    except Student.DoesNotExist():
        raise StudentNotFoundError()
    
    student.delete()
        
    return student 
         