from .models import Teacher
from .exceptions import TeacherNotFoundError

def getTeacher(teacher_id):
    try:
        teacher = Teacher.objects.get(id=teacher_id)
    
    except Teacher.DoesNotExist:
        raise TeacherNotFoundError()
    
    return teacher
    
    
def deleteTeacher(teacher_id):
    try:
        teacher = Teacher.objects.get(id=teacher_id)
        
    except Teacher.DoesNotExist:
        raise TeacherNotFoundError()
    
    teacher.delete()
        
    return teacher
        