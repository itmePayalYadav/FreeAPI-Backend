from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/management/', include('management.urls')),
    # path('api/subscriptions/', include('subscription.urls')),
    # path("api/payments/", include("payment.urls")),
    # path("api/logs/", include("logs.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)