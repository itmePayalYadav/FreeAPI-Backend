from django.urls import path
from . import views

urlpatterns = [
    # ------------------------------------------
    # User Payment
    # ------------------------------------------
    path("user/", views.UserPaymentListView.as_view(), name="user-payment-list"),
    
    # ------------------------------------------
    # Admin Payment
    # ------------------------------------------
    path("admin/", views.AdminPaymentListView.as_view(), name="admin-payment-list"),
    path("admin/<uuid:pk>/", views.AdminPaymentDetailView.as_view(), name="admin-payment-detail"),
    path("admin/<uuid:pk>/update-status/", views.AdminPaymentUpdateStatusView.as_view(), name="admin-payment-update-status"),
    path("admin/<uuid:pk>/delete/", views.AdminPaymentDeleteView.as_view(), name="admin-payment-delete"),
    
    # ------------------------------------------
    # Create & Verify Payment
    # ------------------------------------------
    path("create/", views.CreatePaymentView.as_view(), name="create-payment"),
    path("verify/", views.VerifyPaymentView.as_view(), name="verify-payment"),
]
