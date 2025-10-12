from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    EndpointViewSet,
    ExampleViewSet,
    ResponseViewSet,
    UsageViewSet,
    MediaViewSet,
    SubscriptionViewSet
)

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('endpoints', EndpointViewSet, basename='endpoint')
router.register('examples', ExampleViewSet, basename='example')
router.register('responses', ResponseViewSet, basename='response')
router.register('subscriptions', SubscriptionViewSet, basename='subscription')
router.register('usages', UsageViewSet, basename='usage')
router.register('media', MediaViewSet, basename='media')

urlpatterns = [
    path('', include(router.urls)),
]
