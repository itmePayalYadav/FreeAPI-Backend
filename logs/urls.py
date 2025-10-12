from django.urls import path
from . import views

urlpatterns = [
    # ----------------------------
    # USER API LOGS
    # ----------------------------
    path("user/", views.UserAPIRequestLogListView.as_view(), name="user-api-log-list"),
    path("user/count/", views.UserAPIUsageCountView.as_view(), name="user-api-usage-count"),

    # ----------------------------
    # ADMIN API LOGS
    # ----------------------------
    path("admin/", views.AdminAPIRequestLogListView.as_view(), name="admin-api-log-list"),
    path("admin/<uuid:pk>/", views.AdminAPIRequestLogDetailView.as_view(), name="admin-api-log-detail"),
    path("admin/<uuid:pk>/delete/", views.AdminAPIRequestLogDeleteView.as_view(), name="admin-api-log-delete"),
]
