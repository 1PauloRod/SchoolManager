from rest_framework.exceptions import APIException
from rest_framework import status

class ClassNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Turma não existe."
    default_code = "class_not_found"
    
class ScheduleNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Grade horária não existe."
    default_code = "schedule_not_found"