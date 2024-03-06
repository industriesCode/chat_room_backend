from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Room(models.Model):
    """
    JSON Structure for message field
        {
            "message":"Hi",
            "sent_at":"12:30"
        }
    """
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING
    )
    messages = models.JSONField(
        default=dict
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name
