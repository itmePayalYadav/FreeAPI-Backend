from django.db import models
from django.conf import settings
from accounts.models import User
from core.models import BaseModel
from subscription.models import SubscriptionPlan

class Payment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    subscription = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[("razorpay", "Razorpay"), ("paypal", "Paypal")])
    status = models.CharField(max_length=20, choices=[("pending","Pending"),("completed","Completed"),("failed","Failed")])

    def __str__(self):
        return f"{self.user.username} - {self.transaction_id}"

    def update_status(self, new_status):
        if new_status in ["pending", "completed", "failed"]:
            self.status = new_status
            self.save()

