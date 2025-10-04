import uuid
from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    """Abstract base model that adds created_at, updated_at, and soft delete support"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """Override delete to perform soft delete"""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self, using=None, keep_parents=False):
        """Actually delete from database"""
        super().delete(using=using, keep_parents=keep_parents)
