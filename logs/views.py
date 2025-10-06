from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from .models import APIRequestLog
from apis.models import API
from .serializers import APIRequestLogSerializer
from core.utils import api_success, api_error
from accounts.permissions import IsAdminUser, IsAuthenticatedUser


# ==========================================
# USER API LOG LIST
# ==========================================
class UserAPIRequestLogListView(generics.ListAPIView):
    serializer_class = APIRequestLogSerializer
    permission_classes = [IsAuthenticatedUser]
    search_fields = ["api__name", "status_code"]
    ordering_fields = ["request_time", "status_code"]
    ordering = ["-request_time"]

    def get_queryset(self):
        queryset = APIRequestLog.objects.filter(user=self.request.user)
        api_filter = self.request.query_params.get("api")
        status_filter = self.request.query_params.get("status_code")

        if api_filter:
            queryset = queryset.filter(api__id=api_filter)
        if status_filter:
            queryset = queryset.filter(status_code=status_filter)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return api_success(data=serializer.data, message="User API logs fetched successfully")


# ==========================================
# USER API USAGE COUNT
# ==========================================
class UserAPIUsageCountView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedUser]

    def get(self, request, *args, **kwargs):
        api_id = request.query_params.get("api_id")
        days = int(request.query_params.get("days", 30))

        if not api_id:
            return api_error(message="api_id is required")

        try:
            api_obj = API.objects.get(id=api_id)
        except API.DoesNotExist:
            return api_error(message="API not found", status_code=404)

        count = APIRequestLog.usage_count(user=request.user, api=api_obj, days=days)
        return api_success(data={"usage_count": count}, message=f"API usage count in last {days} days")


# ==========================================
# ADMIN API LOG LIST
# ==========================================
class AdminAPIRequestLogListView(generics.ListAPIView):
    serializer_class = APIRequestLogSerializer
    permission_classes = [IsAdminUser]
    search_fields = ["user__username", "api__name", "status_code"]
    ordering_fields = ["request_time", "status_code"]
    ordering = ["-request_time"]

    def get_queryset(self):
        queryset = APIRequestLog.objects.all()
        user_filter = self.request.query_params.get("user")
        api_filter = self.request.query_params.get("api")
        status_filter = self.request.query_params.get("status_code")

        if user_filter:
            queryset = queryset.filter(user__username__icontains=user_filter)
        if api_filter:
            queryset = queryset.filter(api__id=api_filter)
        if status_filter:
            queryset = queryset.filter(status_code=status_filter)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return api_success(data=serializer.data, message="Admin API logs fetched successfully")


# ==========================================
# ADMIN API LOG DETAIL
# ==========================================
class AdminAPIRequestLogDetailView(generics.RetrieveAPIView):
    serializer_class = APIRequestLogSerializer
    permission_classes = [IsAdminUser]
    queryset = APIRequestLog.objects.all()

    def retrieve(self, request, *args, **kwargs):
        log = self.get_object()
        serializer = self.get_serializer(log)
        return api_success(data=serializer.data, message="API log detail retrieved successfully")


# ==========================================
# ADMIN DELETE API LOG
# ==========================================
class AdminAPIRequestLogDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = APIRequestLog.objects.all()

    def delete(self, request, *args, **kwargs):
        log = self.get_object()
        log.delete()
        return api_success(message="API log deleted successfully", status_code=status.HTTP_204_NO_CONTENT)
