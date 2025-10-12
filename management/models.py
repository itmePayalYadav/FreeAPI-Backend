import uuid
from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from accounts.models import User
from core.models import BaseModel, ActiveManager
from core.utils import generate_unique_slug

# =========================================================
# Category Model
# =========================================================
class Category(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = RichTextUploadingField(blank=True, help_text="Rich formatted category description")
    icon = models.CharField(max_length=100, blank=True, help_text="Icon name or URL")

    objects = ActiveManager()
    all_objects = models.Manager()
    
    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = generate_unique_slug(Category, self.name)
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        """Soft delete category and cascade delete to related APIs"""
        super().delete(using, keep_parents)
        for api in self.apis.all():
            api.delete(using, keep_parents)

    def __str__(self):
        return self.name

# =========================================================
# API Model → renamed to Endpoint
# =========================================================
class Endpoint(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="apis")
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    method = models.CharField(
        max_length=10,
        choices=[("GET", "GET"), ("POST", "POST"), ("PATCH", "PATCH"), ("DELETE", "DELETE")]
    )
    url = models.URLField()
    description = RichTextUploadingField(blank=True, help_text="Rich formatted API documentation")
    path_params = models.JSONField(default=list, blank=True)
    query_params = models.JSONField(default=list, blank=True)
    is_premium = models.BooleanField(default=False)

    objects = ActiveManager()
    all_objects = models.Manager()
    
    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = generate_unique_slug(Endpoint, self.name)
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        """Soft delete Endpoint and cascade to related entities"""
        super().delete(using, keep_parents)

        for example in self.examples.all():
            example.delete(using, keep_parents)

        for response in self.responses.all():
            response.delete(using, keep_parents)

        for media in self.media.all():
            media.delete(using, keep_parents)

        for sub in self.user_access.all():
            sub.delete(using, keep_parents)

    def __str__(self):
        return f"{self.name} ({self.method})"

# =========================================================
# Example Model
# =========================================================
class Example(BaseModel):
    api = models.ForeignKey(Endpoint, on_delete=models.CASCADE, related_name="examples")
    language = models.CharField(max_length=50)
    request_type = models.CharField(max_length=50, help_text="Library or method (Requests, Axios, Fetch etc.)")
    code_snippet = models.TextField(help_text="Example code snippet for this request type")

    objects = ActiveManager()
    all_objects = models.Manager()

    class Meta:
        unique_together = ("api", "language", "request_type")

    def __str__(self):
        return f"{self.api.name} [{self.language} - {self.request_type}]"

# =========================================================
# Response Model
# =========================================================
class ResponseModel(BaseModel):
    api = models.ForeignKey(Endpoint, on_delete=models.CASCADE, related_name="responses")
    status_code = models.IntegerField(default=200)
    media_type = models.CharField(max_length=100, default="application/json")
    headers = models.JSONField(default=dict, blank=True)
    body = models.JSONField(default=dict, blank=True)

    objects = ActiveManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ["status_code"]

    def __str__(self):
        return f"{self.api.name} - {self.status_code} {self.media_type}"

# =========================================================
# Subscription Model
# =========================================================
class Subscription(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="api_access")
    api = models.ForeignKey(Endpoint, on_delete=models.CASCADE, related_name="user_access")
    accessed_at = models.DateTimeField(auto_now=True)
    usage_count = models.IntegerField(default=0)

    objects = ActiveManager()
    all_objects = models.Manager()

    class Meta:
        unique_together = ("user", "api")

    def delete(self, using=None, keep_parents=False):
        """Soft delete subscription and its usage records"""
        super().delete(using, keep_parents)
        for usage in self.usage_records.all():
            usage.delete(using, keep_parents)

    def __str__(self):
        return f"{self.user.username} -> {self.api.name}"

# =========================================================
# Usage / Rate Limit Tracker
# =========================================================
class Usage(BaseModel):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="usage_records")
    request_time = models.DateTimeField(auto_now_add=True)
    status_code = models.IntegerField(default=200)
    method = models.CharField(max_length=10, default="GET")
    request_body = models.JSONField(default=dict, blank=True)
    query_params = models.JSONField(default=dict, blank=True)

    objects = ActiveManager()
    all_objects = models.Manager()

    def __str__(self):
        return f"{self.subscription.user.username} -> {self.subscription.api.name} at {self.request_time}"

# =========================================================
# Media / Attachments
# =========================================================
class Media(BaseModel):
    api = models.ForeignKey(Endpoint, on_delete=models.CASCADE, related_name="media")
    file = models.FileField(upload_to="api_media/")
    description = RichTextUploadingField(blank=True, help_text="Rich formatted Media documentation")
    
    objects = ActiveManager()
    all_objects = models.Manager()

    def __str__(self):
        return f"{self.api.name} Media: {self.file.name}"
