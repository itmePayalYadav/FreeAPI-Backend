from django.urls import path
from . import views

app_name = "apis"

urlpatterns = [
    # ----------------------------
    # --- API Public URLs ---
    # ----------------------------
    path("", views.APIListView.as_view(), name="api-list"),
    path("<uuid:pk>/", views.APIDetailView.as_view(), name="api-detail"),
    
    # ----------------------------
    # --- API Admin URLs ---
    # ----------------------------
    path("admin/", views.APIListAdminView.as_view(), name="admin-api-list"),
    path("admin/create/", views.APICreateAdminView.as_view(), name="admin-api-create"),
    path("admin/<uuid:pk>/detail/", views.APIRetrieveAdminView.as_view(), name="admin-api-detail"),
    path("admin/<uuid:pk>/update/", views.APIUpdateAdminView.as_view(), name="admin-api-update"),
    path("admin/<uuid:pk>/delete/", views.APIDeleteAdminView.as_view(), name="admin-api-delete"),
    
    # ----------------------------
    # --- APICategory Public URLs ---
    # ----------------------------
    path("categories/", views.APICategoryListView.as_view(), name="category-list"),
    path("categories/<uuid:pk>/", views.APICategoryDetailView.as_view(), name="category-detail"),

    # ----------------------------
    # --- APICategory Admin URLs ---
    # ----------------------------
    path("admin/categories/", views.APICategoryListAdminView.as_view(), name="admin-category-list"),
    path("admin/categories/create/", views.APICategoryCreateAdminView.as_view(), name="admin-category-create"),
    path("admin/categories/<uuid:pk>/detail/", views.APICategoryRetrieveAdminView.as_view(), name="admin-category-detail"),
    path("admin/categories/<uuid:pk>/update/", views.APICategoryUpdateAdminView.as_view(), name="admin-category-update"),
    path("admin/categories/<uuid:pk>/delete/", views.APICategoryDeleteAdminView.as_view(), name="admin-category-delete"),

    # ----------------------------
    # --- User Subscription Public URLs ---
    # ----------------------------
    path("subscriptions/", views.UserSubscriptionListView.as_view(), name="user-subscription-list"),
    path("subscriptions/subscribe/", views.SubscribeToAPIView.as_view(), name="subscribe-api"),

    # ----------------------------
    # --- Subscription Admin URLs ---
    # ----------------------------
    path("admin/subscriptions/", views.SubscriptionListAdminView.as_view(), name="admin-subscription-list"),
    path("admin/subscriptions/<uuid:pk>/detail/", views.SubscriptionRetrieveAdminView.as_view(), name="admin-subscription-detail"),
    path("admin/subscriptions/<uuid:pk>/update/", views.SubscriptionUpdateAdminView.as_view(), name="admin-subscription-update"),
    path("admin/subscriptions/<uuid:pk>/delete/", views.SubscriptionDeleteAdminView.as_view(), name="admin-subscription-delete"),
]
