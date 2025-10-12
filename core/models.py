import uuid
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField

# =========================================================
# ActiveManager – hides soft-deleted objects automatically
# =========================================================
class ActiveManager(models.Manager):
    """Manager that returns only active (non-deleted) objects."""

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

# =========================================================
# BaseModel – reusable abstract base model
# =========================================================
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    objects = ActiveManager() 
    all_objects = models.Manager()  

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def delete(self, using=None, keep_parents=False):
        """Soft delete (marks as deleted instead of removing)."""
        if not self.is_deleted:
            self.is_deleted = True
            self.deleted_at = timezone.now()
            self.save(update_fields=["is_deleted", "deleted_at", "updated_at"])

    def restore(self):
        """Restore a soft-deleted object."""
        if self.is_deleted:
            self.is_deleted = False
            self.deleted_at = None
            self.save(update_fields=["is_deleted", "deleted_at", "updated_at"])

    def hard_delete(self, using=None, keep_parents=False):
        """Permanently delete from database."""
        super().delete(using=using, keep_parents=keep_parents)

    def __str__(self):
        return f"{self.__class__.__name__} ({self.id})"
