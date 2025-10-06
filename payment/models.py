import uuid
from django.db import models
from core.models import BaseModel
from accounts.models import User
from subscription.models import SubscriptionPlan
from core.constants import PAYMENT_METHODS, STATUS_CHOICES

class Payment(BaseModel):
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    subscription = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    metadata = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_id}"

    def update_status(self, new_status):
        valid_status = [choice[0] for choice in STATUS_CHOICES]
        if new_status in valid_status:
            self.status = new_status
            self.save()
