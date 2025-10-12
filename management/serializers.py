from rest_framework import serializers
from accounts.models import User
from management.models import Category, Endpoint, Example, ResponseModel, Media, Usage, Subscription

# ----------------------------
# Category Serializer
# ----------------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon']
        read_only_fields = ['id', 'slug']

# ----------------------------
# Endpoint Serializer (basic for list/create)
# ----------------------------
class EndpointSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True,
        source='category'
    )

    class Meta:
        model = Endpoint
        fields = [
            'id', 'name', 'slug', 'method', 'url',
            'category', 'category_id', 'description',
            'is_premium', 'path_params', 'query_params'
        ]
        read_only_fields = ['id', 'slug']

# ----------------------------
# Example Serializer
# ----------------------------
class ExampleSerializer(serializers.ModelSerializer):
    api = EndpointSerializer(read_only=True)
    api_id = serializers.PrimaryKeyRelatedField(
        queryset=Endpoint.objects.all(),
        write_only=True,
        source='api'
    )
    
    class Meta:
        model = Example
        fields = ['id', 'language', 'api', 'api_id', 'request_type', 'code_snippet']
        read_only_fields = ['id']

# ----------------------------
# Response Serializer
# ----------------------------
class ResponseSerializer(serializers.ModelSerializer):
    api = EndpointSerializer(read_only=True)
    api_id = serializers.PrimaryKeyRelatedField(
        queryset=Endpoint.objects.all(),
        write_only=True,
        source='api'
    )
    
    class Meta:
        model = ResponseModel
        fields = ['id', 'status_code', 'api', 'api_id', 'media_type', 'headers', 'body']
        read_only_fields = ['id']

# ----------------------------
# Subscription Serializer
# ----------------------------
class SubscriptionSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    api_name = serializers.CharField(source='api.name', read_only=True)
    api_slug = serializers.CharField(source='api.slug', read_only=True)
    
    # For creation (write) and update
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user'
    )
    api_id = serializers.PrimaryKeyRelatedField(
        queryset=Endpoint.objects.all(),
        source='api'
    )

    class Meta:
        model = Subscription
        fields = [
            'id', 'user_id', 'api_id', 'user_username',
            'api_name', 'api_slug', 'accessed_at', 'usage_count'
        ]
        read_only_fields = ['id', 'user_username', 'api_name', 'api_slug', 'accessed_at']
    
# ----------------------------
# Usage Serializer
# ----------------------------
class UsageSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='subscription.user.username', read_only=True)
    api_name = serializers.CharField(source='subscription.api.name', read_only=True)
    api_slug = serializers.CharField(source='subscription.api.slug', read_only=True)

    class Meta:
        model = Usage
        fields = [
            'id', 'user', 'api_name', 'api_slug',
            'method', 'status_code', 'request_body',
            'query_params', 'request_time'
        ]
        read_only_fields = fields

# ----------------------------
# Media Serializer
# ----------------------------
class MediaSerializer(serializers.ModelSerializer):
    api_id = serializers.PrimaryKeyRelatedField(
        queryset=Endpoint.objects.all(),
        source='api' 
    )
    api = serializers.StringRelatedField(read_only=True)
    file = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Media
        fields = ['id', 'api', 'api_id', 'file', 'description']
        read_only_fields = ['id', 'api']


# ----------------------------
# Endpoint Detail Serializer (for retrieve)
# ----------------------------
class EndpointDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    examples = ExampleSerializer(many=True, read_only=True)
    responses = ResponseSerializer(many=True, read_only=True)
    media = MediaSerializer(many=True, read_only=True)

    class Meta:
        model = Endpoint
        fields = [
            'id', 'name', 'slug', 'method', 'url', 'description',
            'category', 'is_premium', 'path_params', 'query_params',
            'examples', 'responses', 'media'
        ]
        read_only_fields = ['id', 'slug', 'examples', 'responses', 'media']
