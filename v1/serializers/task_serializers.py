from rest_framework import serializers

from task.models import(
    Task, TaskFolder, TaskSection, SubTask
)


class TaskFolderSerializer(serializers.ModelSerializer):
    # person_id = serializers.ReadOnlyField(source='person.id', read_only=True)
    class Meta:
        model = TaskFolder
        fields = [
            'id',
            'name',
            'person',
        ]
        # extra_kwargs = {'person': {'read_only': True}}


class TaskSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskSection
        fields = [
            'id',
            'name',
            'default',
            'taskFolder',
            'person'
        ]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'name',
            'memo',
            'is_done',
            'taskSection',
            'taskFolder',
            'person',
            'start_date',
            'due_date',
            'is_star'
        ]


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = [
            'id',
            'name',
            'is_done',
            'task',
            'person'
        ]
