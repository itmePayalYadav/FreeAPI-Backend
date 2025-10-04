from django.db import models
from django.conf import settings
from accounts.models import User
from core.models import BaseModel
from apis.models import API

class APIRequestLog(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="api_logs")
    api = models.ForeignKey(API, on_delete=models.CASCADE, related_name="logs")
    request_time = models.DateTimeField(auto_now_add=True)
    status_code = models.IntegerField()
    path_params = models.JSONField(default=dict, blank=True)
    query_params = models.JSONField(default=dict, blank=True)
    response = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.api.name} - {self.status_code}"

    @staticmethod
    def usage_count(user, api, days=30):
        from django.utils import timezone
        start = timezone.now() - timezone.timedelta(days=days)
        return APIRequestLog.objects.filter(user=user, api=api, request_time__gte=start).count()
