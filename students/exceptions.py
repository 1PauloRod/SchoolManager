from rest_framework.exceptions import APIException
from rest_framework import status

class StudentNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Estudante não existe.'
    default_code = 'student_not_found'