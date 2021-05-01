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


class TaskSectionSerializer(serializers.ModelSerializer, _PersonInfo):
    person_info = SerializerMethodField()
    class Meta:
        model = TaskSection
        fields = [
            'id',
            'name',
            'default',
            'taskFolder',
            'person',
            'person_info'
        ]
        extra_kwargs = {
            'person': {'write_only':True},
        }


class TaskSectionDetailSerializer(serializers.ModelSerializer, _PersonInfo):
    tasks = SerializerMethodField()
    class Meta:
        model = TaskSection
        fields = [
            'id',
            'name',
            'default',
            'taskFolder',
            'person',
            'person_info'
            'tasks',
        ]
        extra_kwargs = {
            'person': {'write_only':True},
        }

    def get_tasks(self, obj):
        tasks = TaskSerializer(
            Task.objects
                .filter(taskSection=obj.id)
            , many=True
            ).data
        return tasks


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

    def get_task_sections(self, obj):
        task_sections = TaskSectionSerializer(
            TaskSection.objects
                .filter(taskFolder=obj.id)
            , many=True
        ).data
        return task_sections
