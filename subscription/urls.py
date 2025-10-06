from django.urls import path
from .views import (
    ActiveSubscriptionPlanListView,
    SubscriptionPlanListAdminView,
    SubscriptionPlanCreateAdminView,
    SubscriptionPlanUpdateAdminView,
    SubscriptionPlanDeleteAdminView,
    SubscribeToPlanCreateView,
    UserSubscriptionUsageView,
    AdminUserSubscriptionListView,
    AdminDetailSubscriptionView,
    AdminUpdateSubscriptionView,
    AdminDeleteSubscriptionView,
    SubscriptionPlanListByIdAdminView
)

app_name = "subscription"

urlpatterns = [
    # Plans
    path("plans/active/", ActiveSubscriptionPlanListView.as_view(), name="active-plans"),
    path("plans/", SubscriptionPlanListAdminView.as_view(), name="admin-plans"),
    path("plans/create/", SubscriptionPlanCreateAdminView.as_view(), name="create-plan"),
    path("plans/<uuid:pk>/detail/", SubscriptionPlanListByIdAdminView.as_view(), name="plan-detail"),
    path("plans/<uuid:pk>/update/", SubscriptionPlanUpdateAdminView.as_view(), name="update-plan"),
    path("plans/<uuid:pk>/delete/", SubscriptionPlanDeleteAdminView.as_view(), name="delete-plan"),
    
    # Subscribe
    path("subscribe/", SubscribeToPlanCreateView.as_view(), name="subscribe-plan"),
    path("me/", UserSubscriptionUsageView.as_view(), name="my-subscriptions"),
    path("admin/", AdminUserSubscriptionListView.as_view(), name="all-subscriptions"),
    path("<uuid:pk>/detail/", AdminDetailSubscriptionView.as_view(), name="detail-subscription"),
    path("<uuid:pk>/update/", AdminUpdateSubscriptionView.as_view(), name="update-subscription"),
    path("<uuid:pk>/delete/", AdminDeleteSubscriptionView.as_view(), name="delete-subscription"),
]
