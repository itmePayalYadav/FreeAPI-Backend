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
    AdminUpdateSubscriptionView,
    AdminDeleteSubscriptionView,
    SubscriptionPlanListByIdAdminView
)

app_name = "subscription"

urlpatterns = [
    # ----------------------------
    # General / Premium Users
    # ----------------------------
    path("plans/active/", ActiveSubscriptionPlanListView.as_view(), name="active_subscription_plans"),
    path("subscribe/", SubscribeToPlanCreateView.as_view(), name="subscribe_to_plan"),
    path("usage/", UserSubscriptionUsageView.as_view(), name="user_subscription_usage"),

    # ----------------------------
    # Admin Only
    # ----------------------------
    path("plans/", SubscriptionPlanListAdminView.as_view(), name="subscription_plan_list_admin"),
    path("plans/create/", SubscriptionPlanCreateAdminView.as_view(), name="subscription_plan_create_admin"),
    path("plans/<uuid:pk>/list/", SubscriptionPlanListByIdAdminView.as_view(), name="subscription_plan_update_admin"),
    path("plans/<uuid:pk>/update/", SubscriptionPlanUpdateAdminView.as_view(), name="subscription_plan_update_admin"),
    path("plans/<uuid:pk>/delete/", SubscriptionPlanDeleteAdminView.as_view(), name="subscription_plan_delete_admin"),
    path("", AdminUserSubscriptionListView.as_view(), name="admin_user_subscription_list"),
    path("<uuid:pk>/update/", AdminUpdateSubscriptionView.as_view(), name="admin_update_subscription"),
    path("<uuid:pk>/delete/", AdminDeleteSubscriptionView.as_view(), name="admin_delete_subscription"),
]
