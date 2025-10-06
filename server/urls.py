from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/apis/', include('apis.urls')),
    path('api/subscriptions/', include('subscription.urls')),
    path("api/payments/", include("payment.urls")),
]
