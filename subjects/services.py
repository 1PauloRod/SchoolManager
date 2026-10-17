from .models import Subject
from .exceptions import SubjectNotFoundError

def getSubject(subject_id):
    try:
        subject = Subject.objects.get(id=subject_id)
    except Subject.DoesNotExist:
        raise SubjectNotFoundError
    
    return subject

def deleteSubject(subject_id):
    try:
        subject = Subject.objects.get(id=subject_id)
    except Subject.DoesNotExist:
            raise SubjectNotFoundError
        
    subject.delete()
    
    return subject