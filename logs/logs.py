from django.urls import path
from . import views

urlpatterns = [
    # ----------------------------
    # USER API LOGS
    # ----------------------------
    path("user/api-logs/", views.UserAPIRequestLogListView.as_view(), name="user-api-log-list"),
    path("user/api-usage-count/", views.UserAPIUsageCountView.as_view(), name="user-api-usage-count"),

    # ----------------------------
    # ADMIN API LOGS
    # ----------------------------
    path("admin/api-logs/", views.AdminAPIRequestLogListView.as_view(), name="admin-api-log-list"),
    path("admin/api-logs/<int:pk>/", views.AdminAPIRequestLogDetailView.as_view(), name="admin-api-log-detail"),
    path("admin/api-logs/<int:pk>/delete/", views.AdminAPIRequestLogDeleteView.as_view(), name="admin-api-log-delete"),
]
