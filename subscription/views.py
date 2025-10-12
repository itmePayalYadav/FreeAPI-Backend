from rest_framework import generics, permissions, serializers, status
from rest_framework.response import Response
from django.utils import timezone
from .models import SubscriptionPlan, UserSubscription
from .serializers import SubscriptionPlanSerializer, UserSubscriptionSerializer
from accounts.permissions import IsAdminUser, IsPremiumUser, IsAuthenticatedUser
from core.utils import api_success, api_error
from apis.models import Subscription as APISubscription  
from apis.models import API

# ----------------------------
# List all active subscription plans
# ----------------------------
class ActiveSubscriptionPlanListView(generics.ListAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.AllowAny]
    
    search_fields = ["name", "description"]
    ordering_fields = ["price", "duration_days", "created_at"]
    ordering = ["-created_at"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return api_success(data=serializer.data, message="Active subscription plans")

# ----------------------------
# List all subscription plans (Admin)
# ----------------------------
class SubscriptionPlanListAdminView(generics.ListAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAdminUser]
    search_fields = ["name", "description"]
    ordering_fields = ["price", "duration_days", "created_at"]
    ordering = ["-created_at"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return api_success(data=serializer.data, message="All subscription plans")


# ----------------------------
# Retrieve subscription plan by ID (Admin)
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
# Create a new subscription plan (Admin)
# ----------------------------
class SubscriptionPlanCreateAdminView(generics.CreateAPIView):
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return api_success(data=serializer.data, message="Subscription plan created", status_code=status.HTTP_201_CREATED)


# ----------------------------
# Update a subscription plan (Admin)
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
# Delete a subscription plan (Admin)
# ----------------------------
class SubscriptionPlanDeleteAdminView(generics.DestroyAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAdminUser]

    def delete(self, request, *args, **kwargs):
        plan = self.get_object()
        plan.hard_delete()
        return api_success(message="Subscription plan deleted", status_code=status.HTTP_204_NO_CONTENT)


# ----------------------------
# Subscribe to a plan (User)
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
        user_subscription = serializer.save(user=user, end_date=end_date, active=True)

        for api in plan.apis.all():
            APISubscription.objects.get_or_create(user=user, api=api)


    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return api_success(data=response.data, message="Subscribed successfully", status_code=status.HTTP_201_CREATED)


# ----------------------------
# Show current user’s subscriptions / usage
# ----------------------------
class UserSubscriptionUsageView(generics.ListAPIView):
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAuthenticatedUser]
    search_fields = ["plan__name"]
    ordering_fields = ["start_date", "end_date"]
    ordering = ["-start_date"]

    def get_queryset(self):
        return UserSubscription.objects.filter(user=self.request.user, active=True)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return api_success(data=serializer.data, message="Your active subscriptions")


# ----------------------------
# Admin: View all user subscriptions
# ----------------------------
class AdminUserSubscriptionListView(generics.ListAPIView):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAdminUser]
    search_fields = ["user__username", "user__email", "plan__name"]
    ordering_fields = ["start_date", "end_date", "active"]
    ordering = ["-start_date"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return api_success(data=serializer.data, message="All user subscriptions")


# ----------------------------
# Admin: Subscription detail
# ----------------------------
class AdminDetailSubscriptionView(generics.RetrieveAPIView):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        subscription = self.get_object()
        serializer = self.get_serializer(subscription)
        return api_success(
            data=serializer.data,
            message=f"Details for subscription {subscription.id}"
        )


# ----------------------------
# Admin: Update subscription
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
# Admin: Delete subscription
# ----------------------------
class AdminDeleteSubscriptionView(generics.DestroyAPIView):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAdminUser]

    def delete(self, request, *args, **kwargs):
        subscription = self.get_object()
        subscription.hard_delete()
        return api_success(message="Subscription deleted", status_code=status.HTTP_204_NO_CONTENT)
