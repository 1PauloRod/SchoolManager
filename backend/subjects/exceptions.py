from rest_framework.exceptions import APIException
from rest_framework import status

class SubjectNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Matéria não existe."
    default_code = "subject_not_found"