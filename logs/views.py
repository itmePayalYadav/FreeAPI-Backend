from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from logs.models import APIRequestLog
from apis.models import API
from logs.serializers import APIRequestLogSerializer
from core.utils import api_success, api_error
from django.db.models import Count
from accounts.permissions import IsAdminUser, IsAuthenticatedUser

# ==========================================
# USER API LOG LIST
# ==========================================
class UserAPIRequestLogListView(generics.ListAPIView):
    queryset = APIRequestLog.objects.filter(is_deleted=False)
    serializer_class = APIRequestLogSerializer
    permission_classes = [IsAuthenticatedUser]
    
    search_fields = ["user_name", "api_name", "status_code"]
    ordering_fields = ["request_time", "status_code"]
    ordering = ["-request_time"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return api_success(data=serializer.data, message="API logs fetched successfully")

# ==========================================
# USER API USAGE COUNT
# ==========================================
class UserAPIUsageCountView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        usage_data = (
            APIRequestLog.objects
            .filter(user=request.user, is_deleted=False)
            .values(
                "api__id",
                "api__name",
                "api__category__name",
                "api__method",
                "api__is_premium",
            )
            .annotate(request_count=Count("id"))
            .order_by("-request_count")
        )

        return api_success(
            data=list(usage_data),
            message="User API usage count fetched successfully",
            status_code=status.HTTP_200_OK,
        )

# ==========================================
# ADMIN API LOG LIST
# ==========================================
class AdminAPIRequestLogListView(generics.ListAPIView):
    queryset = APIRequestLog.objects.all()
    serializer_class = APIRequestLogSerializer
    permission_classes = [IsAdminUser]
    search_fields = ["user_name", "api_name", "status_code"]
    ordering_fields = ["request_time", "status_code"]
    ordering = ["-request_time"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return api_success(data=serializer.data, message="Admin API logs fetched successfully")

# ==========================================
# ADMIN API LOG DETAIL
# ==========================================
class AdminAPIRequestLogDetailView(generics.RetrieveAPIView):
    queryset = APIRequestLog.objects.filter(is_deleted=False)
    serializer_class = APIRequestLogSerializer
    permission_classes = [IsAdminUser]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()  
        serializer = self.get_serializer(instance)
        return api_success(data=serializer.data, message=" API logs detail successfully")

# ==========================================
# ADMIN DELETE API LOG
# ==========================================
class AdminAPIRequestLogDeleteView(generics.DestroyAPIView):
    queryset = APIRequestLog.objects.all()
    serializer_class = APIRequestLogSerializer
    permission_classes = [IsAdminUser]

    def delete(self, request, *args, **kwargs):
        log = self.get_object()
        log.hard_delete()
        return api_success(message="API request log deleted", status_code=status.HTTP_204_NO_CONTENT)

