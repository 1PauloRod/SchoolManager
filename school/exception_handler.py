from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return response

    is_validation = response.status_code == 400 and isinstance(response.data, dict)
    code = "validation_error" if is_validation else getattr(exc, "default_code", "error")

    if is_validation:
        message = "Erro de validação nos campos enviados."
        error_payload = {"code": code, "message": message, "details": response.data}
    else:
        message = str(exc.detail) if hasattr(exc, "detail") else str(exc)
        error_payload = {"status": response.status_code, "code": code, "message": message}

    response.data = {"error": error_payload}
    return response