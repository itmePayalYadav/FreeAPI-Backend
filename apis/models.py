import uuid
import itertools
from django.db import models
from django.utils.text import slugify
from core.models import BaseModel
from accounts.models import User

# ----------------------------
# Helper function for unique slug
# ----------------------------
def generate_unique_slug(model, name, slug_field='slug'):
    base_slug = slugify(name)
    slug = base_slug
    for i in itertools.count(1):
        if not model.objects.filter(**{slug_field: slug}).exists():
            return slug
        slug = f"{base_slug}-{i}"

# ----------------------------
# API Category Model
# ----------------------------
class APICategory(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True, help_text="Icon name or URL")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(APICategory, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# ----------------------------
# API Model
# ----------------------------
class API(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(APICategory, on_delete=models.CASCADE, related_name="apis")
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    method = models.CharField(
        max_length=10,
        choices=[("GET", "GET"), ("POST", "POST"), ("PATCH", "PATCH"), ("DELETE", "DELETE")]
    )
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
            self.slug = generate_unique_slug(API, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.method})"

# ----------------------------
# Subscription Model
# ----------------------------
class Subscription(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="api_access")
    api = models.ForeignKey(API, on_delete=models.CASCADE, related_name="user_access")
    accessed_at = models.DateTimeField(auto_now=True)
    usage_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ("user", "api")

    def __str__(self):
        return f"{self.user.username} -> {self.api.name}"
