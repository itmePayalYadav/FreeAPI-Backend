from django.db import models
from django.conf import settings
from django.utils import timezone
from accounts.models import User
from core.models import BaseModel

class SubscriptionPlan(BaseModel):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class UserSubscription(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    active = models.BooleanField(default=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        unique_together = ("user", "plan")
        
    def save(self, *args, **kwargs):
        if self.end_date and self.end_date < timezone.now():
            self.active = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"
