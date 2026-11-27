from rest_framework.exceptions import APIException
from rest_framework import status

class EmailAlreadyExistsError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Este e-mail já está cadastrado."
    default_code = "email_already_exists"
    
class CPFAlreadyExistsError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Este CPF já está cadastrado."
    default_code = "cpf_already_exists"
    
class PasswordDistinctError(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = "Senhas não coincidem."
    default_code = "password_distinct"
    
class InvalidCredentialsError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "E-mail ou senha inválidos."
    default_code = "invalid_credentials"
    
class UserNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Usuário não encontrado."
    default_code = "user_not_found"