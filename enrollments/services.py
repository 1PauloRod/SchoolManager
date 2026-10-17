from .models import Enrollment
from .exceptions import EnrollmentNotFoundError

def getEnrollment(enrollment_id):
    try:
        enrollment = Enrollment.objects.get(id=enrollment_id)
    except Enrollment.DoesNotExist:
        raise EnrollmentNotFoundError()
    
    return enrollment

def deleteEnrollment(enrollment_id):
    try:
        enrollment = Enrollment.objects.get(id=enrollment_id)
    
    except Enrollment.DoesNotExist:
        raise EnrollmentNotFoundError()
    
    enrollment.delete() 
    
    return enrollment       