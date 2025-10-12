from rest_framework import serializers
from .models import SubscriptionPlan, UserSubscription
from management.serializers import EndpointSerializer

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    endpoint = EndpointSerializer(many=True, read_only=True)
    
    class Meta:
        model = SubscriptionPlan
        fields = ["id", "name", "description", "price", "duration_days", "is_active", "apis"]

class UserSubscriptionSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    plan_name = serializers.CharField(source="plan.name", read_only=True)

    class Meta:
        model = UserSubscription
        fields = [
            "id",
            "user",
            "username",
            "plan",
            "plan_name",
            "start_date",
            "end_date",
            "active",
            "payment_id",
            "created_at",
        ]
        read_only_fields = ["end_date", "created_at", "user", "plan_name"]
