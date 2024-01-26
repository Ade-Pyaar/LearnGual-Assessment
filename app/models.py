import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class BaseModelClass(models.Model):
    id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False, db_index=True
    )
    created_by = models.CharField(max_length=1024, null=True, blank=True)
    last_edited_by = models.CharField(max_length=1024, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class CustomUser(AbstractUser, BaseModelClass):
    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS = ["username"]

    # overriding username field so as to make it optional
    username = models.CharField(
        max_length=64, null=True, blank=True, default=None, unique=False
    )

    email = models.EmailField(
        max_length=1024, null=True, blank=True, unique=True, db_index=True
    )
    phone_number = models.CharField(
        max_length=15, null=True, blank=True, unique=True, db_index=True
    )
    password = models.CharField(
        max_length=2048, null=False, blank=False, editable=False
    )

    device_token = models.CharField(max_length=1024, null=True, blank=True)

    ws_token = models.CharField(max_length=1024, null=True, blank=True)


class Group(BaseModelClass):
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]


class GroupMessage(BaseModelClass):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="chatmessage_group",
    )

    author = models.ForeignKey(
        CustomUser, related_name="author_messages", on_delete=models.CASCADE
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]


class GroupMembership(BaseModelClass):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="group_memberships"
    )

    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="group_members"
    )
    last_read_message = models.ForeignKey(
        GroupMessage, null=True, blank=True, on_delete=models.SET_NULL
    )
    unread = models.BooleanField(default=False)
    unread_count = models.IntegerField(default=0)

    

    class Meta:
        ordering = ["-created_at"]
