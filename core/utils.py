import uuid
from django.db import models
from django.utils.text import slugify
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

# -------------------------------
# Standardized API Responses
# -------------------------------
def api_success(data=None, message="Success", status_code=status.HTTP_200_OK):
    """Returns a standardized success response."""
    return Response({"success": True,"message": message,"data": data,},status=status_code)

def api_error(errors=None, message=None, status_code=status.HTTP_400_BAD_REQUEST):
    """ Returns a standardized error response with only the first error message."""
    if message is None:
        message = "Something went wrong"
        if errors:
            if isinstance(errors, dict):
                first_field, first_error_list = next(iter(errors.items()))
                first_error = first_error_list[0]
                if isinstance(first_error, ErrorDetail):
                    first_error = str(first_error)
                message = first_error 
            elif isinstance(errors, list):
                first_error = errors[0]
                if isinstance(first_error, ErrorDetail):
                    first_error = str(first_error)
                message = first_error
            elif isinstance(errors, ErrorDetail):
                message = str(errors)
            elif isinstance(errors, str):
                message = errors
    return Response({"success": False,"message": message, "errors": errors},status=status_code)

# -------------------------------
# Generate Unique Slug
# -------------------------------
def generate_unique_slug(model: models.Model, name: str = None, slug_field: str = 'slug') -> str:
    """Generates a unique slug for a model instance."""
    if name:
        base_slug = slugify(name)
        slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
    else:
        slug = uuid.uuid4().hex[:8]
    while model.objects.filter(**{slug_field: slug}).exists():
        slug = f"{slugify(name) if name else ''}-{uuid.uuid4().hex[:8]}"
    return slug
