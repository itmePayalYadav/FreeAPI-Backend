from django.db import models
from core.models import BaseModel
from accounts.models import User
from django.utils.text import slugify

class APICategory(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class API(BaseModel):
    category = models.ForeignKey(APICategory, on_delete=models.CASCADE, related_name="apis")
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    method = models.CharField(max_length=10, choices=[("GET","GET"),("POST","POST"),("PATCH","PATCH"),("DELETE","DELETE")])
    url = models.URLField()
    description = models.TextField()
    path_params = models.JSONField(default=dict, blank=True)
    query_params = models.JSONField(default=dict, blank=True)
    languages = models.JSONField(default=list)
    example_requests = models.JSONField(default=dict)
    example_response = models.JSONField(default=dict)
    is_premium = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.method})"

class Subscription(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="api_access")
    api = models.ForeignKey(API, on_delete=models.CASCADE, related_name="user_access")
    accessed_at = models.DateTimeField(auto_now=True)
    usage_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ("user", "api")
