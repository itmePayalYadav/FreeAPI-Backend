from rest_framework import serializers
from logs.models import APIRequestLog
from apis.serializers import APISerializer
from accounts.serializers import UserSerializer

class APIRequestLogSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source="user.id", read_only=True)
    user_name = serializers.CharField(source="user.username", read_only=True)
    api_id = serializers.CharField(source="api.id", read_only=True)
    api_name = serializers.CharField(source="api.name", read_only=True)
    api_category = serializers.CharField(source="api.category_name", read_only=True)
    api_method = serializers.CharField(source="api.method", read_only=True)
    api_is_premium = serializers.BooleanField(source="api.is_premium", read_only=True)

    class Meta:
        model = APIRequestLog
        fields = [
            "id",
            "user_id",
            "user_name",
            "api_id",
            "api_name",
            "api_category",
            "api_method",
            "api_is_premium",
            "request_time",
            "status_code",
            "path_params",
            "query_params",
            "response",
            "created_at",
            "updated_at"
        ]
        read_only_fields = fields
