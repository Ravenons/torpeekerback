from django.db import models
import uuid

class Visit(models.Model):
    url = models.URLField(null=False)
    is_ready = models.BooleanField(default=False, null=False)
    screenshot = models.TextField(default="")
    ref = models.UUIDField(null=False, default=uuid.uuid4, db_index=True)
