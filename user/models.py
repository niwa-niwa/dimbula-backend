from django.db import models
from django.utils import timezone


class User(models.Model):

    class Meta:
        db_table = 'user'
        ordering = ('created_at',)
        verbose_name = 'user'
        verbose_name_plural = 'users'

    # firebase uid is not editable
    id = models.UUIDField(
        verbose_name="id",
        primary_key=True,
        unique=True
    )
    
    # firebase displayName is editable
    name = models.CharField(
        verbose_name="name",
        max_length=30,
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

    created_at = models.DateTimeField(
        verbose_name="created at",
        default=timezone.now
    )

    updated_at = models.DateTimeField(
        verbose_name="updated at",
        default=timezone.now
    )


    def __str__(self):
        return self.name
