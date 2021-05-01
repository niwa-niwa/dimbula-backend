from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from task.models import(
    Task, TaskFolder, TaskSection, SubTask
)
from person.models import Person
from v1.serializers.person_serializers import PersonSerializer


class _PersonInfo():
    '''
        This is private class. 
        the class should be super class and then child class have syntax
        person_info = SerializerMethodField() 
        fields = [
            ...etc,
            'person_info',
        ]
    '''
    def get_person_info(self, obj):
        person = PersonSerializer(Person.objects.get(id=obj.person.id)).data
        return person


class TaskFolderSerializer(serializers.ModelSerializer, _PersonInfo):
    person_info = SerializerMethodField()
    task_count = SerializerMethodField()

    class Meta:
        model = TaskFolder
        fields = [
            'id',
            'name',
            'person',
            'person_info',
            'created_at',
            'updated_at',
            'task_count',
        ]
        extra_kwargs = {
            'person': {'write_only':True},
        }

    def get_task_count(self, obj):
        task_count = Task.objects.filter(taskFolder=obj.id).count()
        return task_count


class TaskFolderDetailSerializer(serializers.ModelSerializer, _PersonInfo):
    person_info = SerializerMethodField()
    tasks = SerializerMethodField()
    taskSections = SerializerMethodField()

    class Meta:
        model = TaskFolder
        fields = [
            'id',
            'name',
            'person',
            'person_info',
            'created_at',
            'updated_at',
            'tasks',
            'taskSections',
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
            'default',
            'taskFolder',
            'person',
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
            'taskSection',
            'taskFolder',
            'subTasks',
            'person',
            'start_date',
            'due_date',
            'is_star'
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
            'person'
        ]
