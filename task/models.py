import uuid
from django.db import models
from django.utils import timezone

from person.models import Person


class TaskFolder(models.Model):
    class Meta:
        db_table = 'task_folder'
        ordering = ['-created_at']
        verbose_name = 'task folder'
        verbose_name_plural = 'task folders'
    
    id = models.UUIDField(
        verbose_name='id',
        primary_key=True,
        unique=True,
        default=uuid.uuid4
    )

    name = models.CharField(
        verbose_name="name",
        max_length=32,
    )

    person = models.ForeignKey(
        Person,
        verbose_name='person',
        db_index=True,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        verbose_name='created at',
        default=timezone.now,
    )

    updated_at = models.DateTimeField(
        verbose_name='updated at',
        auto_now=True
    )

    def __str__(self):
        return self.name


class TaskStatus(models.Model):
    class Meta:
        db_table = 'task_status'
        ordering = ['-created_at']
        verbose_name = 'task status'
        verbose_name_plural = 'task statuses'

    id = models.UUIDField(
        verbose_name="id",
        primary_key=True,
        unique=True,
        default=uuid.uuid4
    )

    name = models.CharField(
        verbose_name="name",
        max_length=32,
    )

    default = models.BooleanField(
        verbose_name="default",
        default=False
    )

    taskFolder = models.ForeignKey(
        TaskFolder,
        verbose_name='task folder',
        db_index=True,
        on_delete=models.CASCADE
    )

    person = models.ForeignKey(
        Person,
        verbose_name='person',
        db_index=True,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        verbose_name='created at',
        default=timezone.now,
    )

    updated_at = models.DateTimeField(
        verbose_name='updated at',
        auto_now=True
    )

    def __str__(self):
        return self.name


class Task(models.Model):
    class Meta:
        db_table = 'task'
        ordering = ['-created_at']
        verbose_name = 'task'
        verbose_name_plural = 'tasks'

    id = models.UUIDField(
        verbose_name='id',
        primary_key=True,
        unique=True,
        default=uuid.uuid4
    )

    name = models.CharField(
        verbose_name='name',
        max_length=32,
    )

    memo = models.TextField(
        verbose_name='memo',
        blank=True,
        null=True
    )

    taskStatus = models.ForeignKey(
        TaskStatus,
        db_index=True,
        on_delete=models.CASCADE
    )

    person = models.ForeignKey(
        Person,
        db_index=True,
        on_delete=models.CASCADE
    )

    start_date = models.DateField(
        verbose_name='start date',
        blank=True,
        null=True,
    )

    due_date = models.DateTimeField(
        verbose_name='due date',
        blank=True,
        null=True
    )

    star = models.BooleanField(
        verbose_name="star",
        default=False
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

class TaskStep(models.Model):
    class Meta:
        db_table = 'task_step'
        ordering = ['-created_at']
        verbose_name = 'task step'
        verbose_name_plural = 'task steps'

    id = models.UUIDField(
        verbose_name="id",
        primary_key=True,
        unique=True,
        default=uuid.uuid4
    )

    name = models.CharField(
        verbose_name="name",
        max_length=32,
    )

    is_done = models.BooleanField(
        verbose_name="is done",
        default=False
    )

    task = models.ForeignKey(
        Task,
        verbose_name="task",
        db_index=True,
        on_delete=models.CASCADE
    )

    person = models.ForeignKey(
        Person,
        verbose_name="person",
        db_index=True,
        on_delete=models.CASCADE
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
