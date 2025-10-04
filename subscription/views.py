from rest_framework import generics, permissions, serializers
from rest_framework.response import Response
from django.utils import timezone
from .models import SubscriptionPlan, UserSubscription
from .serializers import SubscriptionPlanSerializer, UserSubscriptionSerializer
from accounts.permissions import IsAdminUser, IsPremiumUser, IsAuthenticatedUser
from core.utils import api_success, api_error

# ----------------------------
# List all active subscription plans (general/premium users)
# ----------------------------
class ActiveSubscriptionPlanListView(generics.ListAPIView):
    queryset = SubscriptionPlan.objects.filter(is_active=True)
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAuthenticatedUser]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return api_success(data=serializer.data, message="Active subscription plans")

# ----------------------------
# List all subscription plans
# ----------------------------
class SubscriptionPlanListAdminView(generics.ListAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return api_success(data=serializer.data, message="All subscription plans")

# ----------------------------
# List By Id subscription plans
# ----------------------------
class SubscriptionPlanListByIdAdminView(generics.RetrieveAPIView):
    queryset = SubscriptionPlan.objects.filter(is_deleted=False)
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAdminUser]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()  
        serializer = self.get_serializer(instance)
        return api_success(data=serializer.data, message="Subscription plan details")

# ----------------------------
# Create a new subscription plan
# ----------------------------
class SubscriptionPlanCreateAdminView(generics.CreateAPIView):
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return api_success(data=serializer.data, message="Subscription plan created")

# ----------------------------
# Update a subscription plan
# ----------------------------
class SubscriptionPlanUpdateAdminView(generics.RetrieveUpdateAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAdminUser]

    def patch(self, request, *args, **kwargs):
        plan = self.get_object()
        serializer = self.get_serializer(plan, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return api_success(data=serializer.data, message="Subscription plan updated")

# ----------------------------
#  Delete a subscription plan (soft delete)
# ----------------------------
class SubscriptionPlanDeleteAdminView(generics.DestroyAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAdminUser]

    def delete(self, request, *args, **kwargs):
        plan = self.get_object()
        plan.hard_delete()
        return api_success(message="Subscription plan deleted")

# ----------------------------
# Subscribe to a plan
# ----------------------------
class SubscribeToPlanCreateView(generics.CreateAPIView):
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAuthenticatedUser]

    def perform_create(self, serializer):
        user = self.request.user
        plan = serializer.validated_data.get("plan")

        if not plan.is_active:
            raise serializers.ValidationError("This subscription plan is not active.")
        if UserSubscription.objects.filter(user=user, plan=plan, active=True).exists():
            raise serializers.ValidationError("You already have an active subscription for this plan.")

        end_date = timezone.now() + timezone.timedelta(days=plan.duration_days) if plan.duration_days else None
        serializer.save(user=user, end_date=end_date, active=True)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return api_success(data=response.data, message="Subscribed successfully")

# ----------------------------
# Show current user’s subscriptions / usage
# ----------------------------
class UserSubscriptionUsageView(generics.ListAPIView):
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAuthenticatedUser]

    def get_queryset(self):
        return UserSubscription.objects.filter(user=self.request.user, active=True)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return api_success(data=serializer.data, message="Your active subscriptions")

# ----------------------------
# View all user subscriptions
# ----------------------------
class AdminUserSubscriptionListView(generics.ListAPIView):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return api_success(data=serializer.data, message="All user subscriptions")

# ----------------------------
#  Update subscription (extend/expire)
# ----------------------------
class AdminUpdateSubscriptionView(generics.RetrieveUpdateAPIView):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAdminUser]

    def patch(self, request, *args, **kwargs):
        subscription = self.get_object()
        serializer = self.get_serializer(subscription, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return api_success(data=serializer.data, message="Subscription updated")

# ----------------------------
# Delete subscription (soft delete)
# ----------------------------
class AdminDeleteSubscriptionView(generics.DestroyAPIView):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAdminUser]

    def delete(self, request, *args, **kwargs):
        subscription = self.get_object()
        subscription.delete()
        return api_success(message="Subscription deleted (soft delete)")
