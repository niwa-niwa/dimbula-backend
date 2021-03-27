from django.db import models
from django.utils import timezone
import uuid


class Person(models.Model):

    class Meta:
        db_table = 'person'
        ordering = ['-created_at']
        verbose_name = 'person'
        verbose_name_plural = 'persons'

    # the id is not based on firebase uid
    id = models.UUIDField(
        verbose_name="id",
        primary_key=True,
        unique=True,
        default=uuid.uuid4
    )

    # firebase uid is not editable
    firebase_id = models.CharField(
        verbose_name="firebase id",
        max_length=64,
        unique=True
    )
    
    # firebase displayName is editable
    name = models.CharField(
        verbose_name="name",
        max_length=30,
    )

    # email is based on firebase email
    email = models.EmailField(
        verbose_name="email",
        max_length=240
    )

    # emailVerified is not editable
    email_verified = models.BooleanField(
        verbose_name="email verified",
        default=False
    )

    # firebase photoURL is editable
    photo_url = models.URLField(
        verbose_name='photo url',
        null=True,
        blank=True
    )

    # firebase prividerId that likes "google.com" is not editable
    provider_id = models.CharField(
        verbose_name="provider id",
        max_length=30
    )

    # the value is for this app
    is_admin = models.BooleanField(
        verbose_name="admin",
        default=False
    )

    # a user is available or not
    is_active = models.BooleanField(
        verbose_name="active",
        default=True
    )

    is_authenticated = models.BooleanField(
        verbose_name="authenticated",
        default=True
    )

    # last login to the app
    last_login = models.DateTimeField(
        verbose_name="last login at",
        default=timezone.now
    )

    created_at = models.DateTimeField(
        verbose_name="created at",
        default=timezone.now
    )

    updated_at = models.DateTimeField(
        verbose_name="updated at",
        auto_now=True
    )

    def __str__(self):
        return self.name
