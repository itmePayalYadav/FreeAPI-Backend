from django.contrib import admin
from .models import SubscriptionPlan, UserSubscription

# --------------------
# SubscriptionPlan Admin
# --------------------
@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "price", "duration_days", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "duration_days", "created_at")
    search_fields = ("name", "description")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

# --------------------
# UserSubscription Admin
# --------------------
@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "plan", "start_date", "end_date", "active", "payment_id", "created_at", "updated_at")
    list_filter = ("active", "start_date", "end_date", "plan")
    search_fields = ("user__username", "plan__name", "payment_id")
    ordering = ("-start_date",)
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "start_date"
