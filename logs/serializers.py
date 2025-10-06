from rest_framework import serializers
from .models import APIRequestLog
from apis.serializers import APISerializer
from accounts.serializers import UserSerializer

class APIRequestLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    api = APISerializer(read_only=True)
    
    class Meta:
        model = APIRequestLog
        fields = [
            "id",
            "user",
            "api",
            "request_time",
            "status_code",
            "path_params",
            "query_params",
            "response",
            "created_at",
            "updated_at"
        ]
        read_only_fields = [
            "id",
            "user",
            "api",
            "request_time",
            "created_at",
            "updated_at"
        ]
