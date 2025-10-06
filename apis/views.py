from rest_framework import generics, permissions, status, serializers
from core.utils import api_success, api_error
from .models import APICategory, API, Subscription
from .serializers import APISerializer, APICategorySerializer, SubscriptionSerializer

# ----------------------------
# --- APICategory Public Views ---
# ----------------------------
class APICategoryListView(generics.ListAPIView):
    queryset = APICategory.objects.prefetch_related("apis").all()
    serializer_class = APICategorySerializer
    permission_classes = [permissions.AllowAny]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return api_success(data=serializer.data, message="Successfully fetched API categories")


class APICategoryDetailView(generics.RetrieveAPIView):
    queryset = APICategory.objects.prefetch_related("apis").all()
    serializer_class = APICategorySerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_success(data=serializer.data, message="Successfully fetched API category details")


# ----------------------------
# --- APICategory Admin Views ---
# ----------------------------
class APICategoryListAdminView(generics.ListAPIView):
    queryset = APICategory.objects.prefetch_related("apis").all()
    serializer_class = APICategorySerializer
    permission_classes = [permissions.IsAdminUser]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return api_success(data=serializer.data, message="Successfully fetched API categories (admin)")


class APICategoryCreateAdminView(generics.CreateAPIView):
    serializer_class = APICategorySerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return api_success(data=serializer.data, message="API category created successfully", status_code=status.HTTP_201_CREATED)


class APICategoryRetrieveAdminView(generics.RetrieveAPIView):
    queryset = APICategory.objects.prefetch_related("apis").all()
    serializer_class = APICategorySerializer
    permission_classes = [permissions.IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_success(data=serializer.data, message="Successfully fetched API category details (admin)")


class APICategoryUpdateAdminView(generics.RetrieveUpdateAPIView):
    queryset = APICategory.objects.all()
    serializer_class = APICategorySerializer
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return api_success(data=serializer.data, message="API category updated successfully")


class APICategoryDeleteAdminView(generics.DestroyAPIView):
    queryset = APICategory.objects.all()
    serializer_class = APICategorySerializer
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.hard_delete()
        return api_success(message="API category deleted successfully", status_code=status.HTTP_204_NO_CONTENT)


# ----------------------------
# --- API Public Views ---
# ----------------------------
class APIListView(generics.ListAPIView):
    queryset = API.objects.all()
    serializer_class = APISerializer
    permission_classes = [permissions.AllowAny]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return api_success(data=serializer.data, message="Successfully fetched APIs list")


class APIDetailView(generics.RetrieveAPIView):
    queryset = API.objects.all()
    serializer_class = APISerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_success(data=serializer.data, message="Successfully fetched API details")


# ----------------------------
# --- API Admin Views ---
# ----------------------------
class APIListAdminView(generics.ListAPIView):
    queryset = API.objects.all()
    serializer_class = APISerializer
    permission_classes = [permissions.IsAdminUser]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return api_success(data=serializer.data, message="Successfully fetched APIs list (admin)")


class APICreateAdminView(generics.CreateAPIView):
    serializer_class = APISerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return api_success(data=serializer.data, message="API created successfully", status_code=status.HTTP_201_CREATED)


class APIRetrieveAdminView(generics.RetrieveAPIView):
    queryset = API.objects.all()
    serializer_class = APISerializer
    permission_classes = [permissions.IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_success(data=serializer.data, message="Successfully fetched API details (admin)")


class APIUpdateAdminView(generics.RetrieveUpdateAPIView):
    queryset = API.objects.all()
    serializer_class = APISerializer
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return api_success(data=serializer.data, message="API updated successfully")


class APIDeleteAdminView(generics.DestroyAPIView):
    queryset = API.objects.all()
    serializer_class = APISerializer
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.hard_delete()
        return api_success(message="API deleted successfully", status_code=status.HTTP_204_NO_CONTENT)


# ----------------------------
# --- User Subscription Public Views ---
# ----------------------------
class UserSubscriptionListView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["api__name"]
    ordering_fields = ["accessed_at", "usage_count"]
    ordering = ["-accessed_at"]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user).select_related("api")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return api_success(data=serializer.data, message="Successfully fetched your subscriptions")


class SubscribeToAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        api_id = self.request.data.get("api")
        try:
            api_instance = API.objects.get(id=api_id)
        except API.DoesNotExist:
            raise serializers.ValidationError("API not found")

        if Subscription.objects.filter(user=self.request.user, api=api_instance).exists():
            raise serializers.ValidationError("You are already subscribed to this API")

        serializer.save(user=self.request.user, api=api_instance)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return api_success(data=response.data, message="Subscribed to API successfully", status_code=status.HTTP_201_CREATED)


# ----------------------------
# --- Subscription Admin Views ---
# ----------------------------
class SubscriptionListAdminView(generics.ListAPIView):
    queryset = Subscription.objects.select_related("api", "user").all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAdminUser]
    search_fields = ["user__username", "api__name"]
    ordering_fields = ["accessed_at", "usage_count"]
    ordering = ["-accessed_at"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return api_success(data=serializer.data, message="Successfully fetched all subscriptions (admin)")
    
class SubscriptionRetrieveAdminView(generics.RetrieveAPIView):
    queryset = Subscription.objects.select_related("api", "user").all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_success(data=serializer.data, message="Successfully fetched subscription details (admin)")


class SubscriptionUpdateAdminView(generics.RetrieveUpdateAPIView):
    queryset = Subscription.objects.select_related("api", "user").all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return api_success(data=serializer.data, message="Subscription updated successfully")

class SubscriptionDeleteAdminView(generics.DestroyAPIView):
    queryset = Subscription.objects.select_related("api", "user").all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.hard_delete()
        return api_success(message="Subscription deleted successfully", status_code=status.HTTP_204_NO_CONTENT)
