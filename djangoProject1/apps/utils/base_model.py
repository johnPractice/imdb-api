from django.db import models
import uuid
from django.utils import timezone


class BaseModel(models.Model):
    id = models.UUIDField(
        unique=True,
        db_index=True,
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    created_at = models.DateTimeField(
        auto_created=True, default=timezone.now())
    updated_at = models.DateTimeField(auto_created=True,
                                      auto_now_add=True)

    # is_deleted=models.BooleanField(default=False) ## for no delete policy
    class Meta:
        abstract = True
