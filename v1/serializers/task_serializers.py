from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from task.models import(
    Task, TaskFolder, TaskSection, SubTask
)
from v1.serializers.person_serializers import PersonSerializer


class TaskFolderSerializer(serializers.ModelSerializer):
    task_count = SerializerMethodField()

    class Meta:
        model = TaskFolder
        fields = [
            'id',
            'name',
            'person',
            'task_count',
            'updated_at',
            'created_at',
        ]

    def get_task_count(self, obj):
        task_count = Task.objects.filter(taskFolder=obj.id).count()
        return task_count


class TaskFolderDetailSerializer(serializers.ModelSerializer):
    person = PersonSerializer()
    tasks = SerializerMethodField()
    taskSections = SerializerMethodField()

    class Meta:
        model = TaskFolder
        fields = [
            'id',
            'name',
            'person',
            'tasks',
            'taskSections',
            'updated_at',
            'created_at',
        ]
        extra_kwargs = {
            'person': {'write_only':True},
        }

    def get_tasks(self, obj):
        tasks = TaskSerializer(
            Task.objects.filter(taskFolder=obj.id)
            , many=True
        ).data
        return tasks

    def get_taskSections(self, obj):
        taskSections = TaskSectionSerializer(
            TaskSection.objects
                .filter(taskFolder=obj.id)
            , many=True
        ).data
        return taskSections


class TaskSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSection
        fields = [
            'id',
            'name',
            'taskFolder',
            'person',
            'updated_at',
            'created_at',
        ]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'name',
            'memo',
            'is_done',
            'is_star',
            'start_date',
            'due_date',
            'taskSection',
            'taskFolder',
            'person',
            'updated_at',
            'created_at',
        ]


class TaskDetailSerializer(serializers.ModelSerializer):
    person = PersonSerializer()
    taskSection = TaskSectionSerializer()
    taskFolder = TaskFolderSerializer()
    subTasks = SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id',
            'name',
            'memo',
            'is_done',
            'is_star',
            'start_date',
            'due_date',
            'taskSection',
            'taskFolder',
            'subTasks',
            'person',
            'updated_at',
            'created_at',
        ]

    def get_subTasks(self, obj):
        sub_tasks = SubTaskSerializer(
            SubTask.objects.filter(task=obj.id)
            , many=True
        ).data
        return sub_tasks


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = [
            'id',
            'name',
            'is_done',
            'task',
            'person',
            'updated_at',
            'created_at',
        ]
