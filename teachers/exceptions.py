from rest_framework.exceptions import APIException
from rest_framework import status

class TeacherNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Professor não existe."
    default_code = "teacher_not_found"