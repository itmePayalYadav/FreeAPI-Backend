from rest_framework import viewsets, filters, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from core.utils import api_success, api_error
from accounts.permissions import IsAdminUser
from management.models import (
    Category, 
    Endpoint, 
    Example, 
    Media, 
    ResponseModel, 
    Usage, Subscription
)
from management.serializers import (
    CategorySerializer,
    EndpointSerializer,
    EndpointDetailSerializer,
    ExampleSerializer,
    ResponseSerializer,
    MediaSerializer,
    UsageSerializer,
    SubscriptionSerializer
)

# ----------------------------
# Category ViewSet
# ----------------------------
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_deleted=False)
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminUser]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return api_success(
            data=serializer.data,
            message=f"{len(serializer.data)} categories found",
            status_code=status.HTTP_200_OK
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_success(
            data=serializer.data,
            message="Category retrieved successfully",
            status_code=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return api_success(
            data=serializer.data,
            message="Category created successfully",
            status_code=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return api_success(
            data=serializer.data,
            message="Category updated successfully",
            status_code=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return api_success(
            data=None,
            message="Category deleted successfully",
            status_code=status.HTTP_204_NO_CONTENT
        )

# ----------------------------
# Endpoint ViewSet
# ----------------------------
class EndpointViewSet(viewsets.ModelViewSet):
    queryset = Endpoint.objects.filter(is_deleted=False)
    serializer_class = EndpointSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'slug'
    search_fields = ['name', 'url']
    ordering_fields = ['name', 'created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EndpointDetailSerializer
        return EndpointSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return api_success(
            data=serializer.data,
            message=f"{len(serializer.data)} APIs found",
            status_code=status.HTTP_200_OK
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_success(
            data=serializer.data,
            message="API retrieved successfully",
            status_code=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return api_success(
            data=serializer.data,
            message="API created successfully",
            status_code=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return api_success(
            data=serializer.data,
            message="API updated successfully",
            status_code=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return api_success(
            data=None,
            message="API deleted successfully",
            status_code=status.HTTP_204_NO_CONTENT
        )

# ----------------------------
# Example ViewSet
# ----------------------------
class ExampleViewSet(viewsets.ModelViewSet):
    queryset = Example.objects.filter(is_deleted=False)
    serializer_class = ExampleSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'id'
    
    search_fields = ['language']
    ordering_fields = ['language', 'request_type', 'created_at']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return api_success(
            data=serializer.data,
            message=f"{len(serializer.data)} API Examples found",
            status_code=status.HTTP_200_OK
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_success(
            data=serializer.data,
            message="API Examples retrieved successfully",
            status_code=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return api_success(
            data=serializer.data,
            message="API Examples created successfully",
            status_code=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return api_success(
            data=serializer.data,
            message="API Examples updated successfully",
            status_code=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return api_success(
            data=None,
            message="API Examples deleted successfully",
            status_code=status.HTTP_204_NO_CONTENT
        )

# ----------------------------
# Response ViewSet
# ----------------------------
class ResponseViewSet(viewsets.ModelViewSet):
    queryset = ResponseModel.objects.filter(is_deleted=False)
    serializer_class = ResponseSerializer
    lookup_field = 'id'
    search_fields = ['status_code', 'media_type']
    ordering_fields = ['status_code', 'created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page if page else queryset, many=True)
        if page:
            return self.get_paginated_response(serializer.data)
        return api_success(data=serializer.data, message=f"{len(serializer.data)} API Responses found")

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return api_success(data=serializer.data, message="API Response retrieved successfully")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return api_success(data=serializer.data, message="API Response created successfully", status_code=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.pop('partial', False))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return api_success(data=serializer.data, message="API Response updated successfully")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return api_success(data=None, message="API Response deleted successfully", status_code=status.HTTP_204_NO_CONTENT)

# ----------------------------
# Subscription ViewSet
# ----------------------------
class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAdminUser]  
    ordering_fields = ['accessed_at', 'usage_count']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page if page else queryset, many=True)
        if page:
            return self.get_paginated_response(serializer.data)
        return api_success(
            data=serializer.data,
            message=f"{len(serializer.data)} subscriptions found",
            status_code=status.HTTP_200_OK
        )

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return api_success(
            data=serializer.data,
            message="Subscription retrieved successfully",
            status_code=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return api_success(
            data=serializer.data,
            message="Subscription created successfully",
            status_code=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return api_success(
            data=serializer.data,
            message="Subscription updated successfully",
            status_code=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return api_success(
            data=None,
            message="Subscription deleted successfully",
            status_code=status.HTTP_204_NO_CONTENT
        )

# ----------------------------
# Media ViewSet
# ----------------------------
class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.filter(is_deleted=False)
    serializer_class = MediaSerializer
    lookup_field = "id"
    search_fields = ["description"]
    ordering_fields = ["created_at"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()] 
        return [IsAdminUser()]  

    def get_serializer(self, *args, **kwargs):
        if self.request.method == "PATCH":
            kwargs["partial"] = True
        return super().get_serializer(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page or queryset, many=True)
        if page:
            return self.get_paginated_response(serializer.data)
        return api_success(data=serializer.data, message=f"{len(serializer.data)} API Media found")

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return api_success(data=serializer.data, message="API Media retrieved successfully")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return api_success(data=serializer.data, message="API Media created successfully", status_code=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return api_success(data=serializer.data, message="API Media updated successfully")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return api_success(data=None, message="API Media deleted successfully", status_code=status.HTTP_204_NO_CONTENT)

# ----------------------------
# Usage ViewSet
# ----------------------------
class UsageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API for admin/dashboard to see usage records.
    """
    queryset = Usage.objects.select_related('subscription__user', 'subscription__api').all()
    serializer_class = UsageSerializer
    permission_classes = [IsAdminUser]
    search_fields = ['status_code', 'request_time']
    ordering_fields = ['request_time', 'status_code', 'method']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page if page else queryset, many=True)
        if page:
            return self.get_paginated_response(serializer.data)
        return api_success(
            data=serializer.data,
            message=f"{len(serializer.data)} API usage records found",
            status_code=status.HTTP_200_OK
        )

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return api_success(
            data=serializer.data,
            message="API usage record retrieved successfully",
            status_code=status.HTTP_200_OK
        )
