from django.contrib import admin
from .models import (
    TaskFolder,
    TaskStatus,
    Task,
    TaskStep
)

admin.site.register(TaskFolder)
admin.site.register(TaskStatus)
admin.site.register(Task)
admin.site.register(TaskStep)
