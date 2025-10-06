from rest_framework import serializers
from .models import APICategory, API, Subscription

class APISerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    
    class Meta:
        model = API
        fields = [
            "id",
            "category",
            "category_name",
            "name",
            "slug",
            "method",
            "url",
            "description",
            "path_params",
            "query_params",
            "languages",
            "example_requests",
            "example_response",
            "is_premium",
        ]
        
    def get_category_name(self, obj):
        return obj.category.name
        
class APICategorySerializer(serializers.ModelSerializer):
    apis = APISerializer(many=True, read_only=True) 

    class Meta:
        model = APICategory
        fields = ["id", "name", "slug", "description", "apis", "icon"]

class SubscriptionSerializer(serializers.ModelSerializer):
    api = APISerializer(read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    
    class Meta:
        model = Subscription
        fields = ["id", "username", "api", "accessed_at", "usage_count"]
