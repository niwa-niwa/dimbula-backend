from django.contrib import admin
from .models import (
    TaskFolder,
    TaskSection,
    Task,
    SubTask
)

admin.site.register(TaskFolder)
admin.site.register(TaskSection)
admin.site.register(Task)
admin.site.register(SubTask)
