from rest_framework.response import Response

def api_success(data=None, message="Success", status_code=200):
    """Standard success response"""
    return Response({"success": True,"message": message,"data": data,}, status=status_code)

def api_error(errors=None, message="Something went wrong", status_code=400):
    """Standard error response"""
    return Response({
        "success": False, "message": message, "errors": errors}, status=status_code)
