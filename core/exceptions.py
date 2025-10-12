from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .utils import api_error

def custom_exception_handler(exc, context):
    """Custom DRF exception handler that returns standardized API error responses."""
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, ValidationError):
            return api_error(
                errors=exc.detail,
                message="Validation failed",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        return api_error(
            errors=getattr(response, 'data', None),
            message=str(exc),
            status_code=response.status_code
        )

    return api_error(
        message="Internal server error",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
