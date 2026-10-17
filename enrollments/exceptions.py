from rest_framework.exceptions import APIException
from rest_framework import status

class EnrollmentNotFoundError(APIException):
    status = status.HTTP_404_NOT_FOUND
    default_detail = 'Matrícula não encontrada.'
    default_code = 'enrollment_not_found'