from django.db.models.deletion import SET_NULL
from person.models import Person
from task.models import *


def create_admin() -> Person:
    """
    create a admin 

    Argument:
        nothing

    Return :
        Parson
            firebase_id="admin_firebase_user_uid",
            name="test_name_admin",
            email="test_email_admin@adb.com",
            email_verified=True,
            provider_id="google.com",
            is_staff=True,
    """
    return Person.objects.create(
            firebase_id="admin_firebase_user_uid",
            name="test_name_admin",
            email="test_email_admin@adb.com",
            email_verified=True,
            provider_id="google.com",
            is_staff=True,
    )


def create_person(
        firebase_id="custom_firebase_user_uid",
        name="test_name_custom",
        email="test_email_custom@adb.com",
        email_verified=True,
        provider_id="google.com",
        is_staff=False ) -> Person:
    """
    create a person

    argument:
        firebase_id : String
        name : String
        email : String and mail address
        email_verified : Boolean
        provider_id : String
        is_staff : Boolean

        Default : 
            firebase_id="custom_firebase_user_uid",
            name="test_name_custom",
            email="test_email_custom@adb.com",
            email_verified=True,
            provider_id="google.com",
            is_staff=False,
    return
        type of Person
    """

    return Person.objects.create(
        firebase_id=firebase_id,
        name=name,
        email=email,
        email_verified=email_verified,
        provider_id=provider_id,
        is_staff=is_staff
    )


def create_taskFolder(
    person: Person,
    name = "shopping") -> TaskFolder:
    """
    create a TaskFolder

    Argument:
        person : Person
        name : String
            name of task folder
            default = shopping

    return :
        type of TaskFolder
    """

    return TaskFolder.objects.create(
        name=name,
        person=person
    )


def create_taskSection(
    person: Person,
    taskFolder: TaskFolder,
    name="Happy box" ) -> TaskSection:
    """
    create a task section

    Arguments
        person : Person,
        taskFolder : TaskFolder,
        name : String
            name of task section
            defalt = "Happy box"

    Return
        type of TaskSection
    """
    
    return TaskSection.objects.create(
        name=name,
        taskFolder=taskFolder,
        person=person,
    )


def create_task(
    person: Person,
    taskFolder: TaskFolder,
    taskSection=None,
    name = "do my landry",) -> Task:
    """
    crete a task

    Arguments
        person : Person,
        taskFolder : TaskFolder,
        taskSection : TaskSection,
        name : String
            name of task
            default = do my landry

    Return 
        type of Task
    """

    return Task.objects.create(
        name=name,
        taskSection=taskSection,
        taskFolder=taskFolder,
        person=person,
    )


def create_subTask(
    person: Person,
    task: Task,
    name = "step 1") -> SubTask:
    """
    create a subTask

    Argument:
        person : Person,
        task : Task,
        name : String
            name of subTask
            default = step 1

    Return:
        type of SubTask
    """

    return SubTask.objects.create(
        name=name,
        task=task,
        person=person
    )


def create_taskData():
    """
    Create Task Folders, Task Sections, Tasks, SubTasks, 
    """
    TaskFactory.excute_subTasks()


class TaskFactory(object):
        
    @classmethod
    def excute_persons(self):
        self._create_persons()

    @classmethod
    def excute_taskFolders(self):
        persons = self._create_persons()
        self._create_taskFolders(persons)

    @classmethod
    def excute_taskSections(self):
        persons = self._create_persons()
        taskFolders = self._create_taskFolders(persons)
        taskSections = self._create_taskSections(persons, taskFolders)

    @classmethod
    def excute_tasks(self):
        persons = self._create_persons()
        taskFolders = self._create_taskFolders(persons)
        taskSections = self._create_taskSections(persons, taskFolders)
        tasks = self._create_tasks(persons, taskFolders, taskSections)

    @classmethod
    def excute_subTasks(cls):
        persons = cls._create_persons()
        taskFolders = cls._create_taskFolders(persons)
        taskSections = cls._create_taskSections(persons, taskFolders)
        tasks = cls._create_tasks(persons, taskFolders, taskSections)
        subTasks = cls._create_subTasks(persons, tasks)


    def _create_persons():
        person_a = Person.objects.create(
            firebase_id="person_a_firebase_uid",
            name="test_name_person_a",
            email="test_email_person_a@adb.com",
            email_verified=True,
            provider_id="google.com",
            is_staff=True,
        )
        person_b = Person.objects.create(
            firebase_id="person_b_firebase_uid",
            name="test_name_person_b",
            email="test_email_person_b@adb.com",
            email_verified=True,
            provider_id="google.com",
            is_staff=False,
        )
        person_c = Person.objects.create(
            firebase_id="person_c_firebase_uid",
            name="test_name_person_c",
            email="test_email_person_c@adb.com",
            email_verified=False,
            provider_id="google.com",
            is_staff=False,
        )
        person_d = Person.objects.create(
            firebase_id="person_d_firebase_uid",
            name="test_name_person_d",
            email="test_email_person_d@adb.com",
            email_verified=False,
            provider_id="google.com",
            is_staff=False,
        )
        person_e = Person.objects.create(
            firebase_id="person_e_firebase_uid",
            name="test_name_person_e",
            email="test_email_person_e@adb.com",
            email_verified=False,
            provider_id="google.com",
            is_staff=False,
        )
        return [person_a, person_b, person_c, person_d, person_e]


    def _create_taskFolders(persons):

        folder_a = TaskFolder.objects.create(
            name="ToDo",
            person=persons[0],
        )
        folder_b = TaskFolder.objects.create(
            name="ToDo Later",
            person=persons[1],
        )
        folder_c = TaskFolder.objects.create(
            name="Future",
            person=persons[2],
        )
        folder_d = TaskFolder.objects.create(
            name="ToDo_d",
            person=persons[3],
        )
        folder_e = TaskFolder.objects.create(
            name="Future_dd",
            person=persons[4],
        )
        return [folder_a, folder_b, folder_c, folder_d, folder_e]


    def _create_taskSections(persons, task_folders):

        task_section_a = TaskSection.objects.create(
            name="in progress",
            taskFolder=task_folders[0],
            person=persons[0],
        )
        task_section_b = TaskSection.objects.create(
            name="is waiting",
            taskFolder=task_folders[1],
            person=persons[1],
        )
        task_section_c = TaskSection.objects.create(
            name="done",
            taskFolder=task_folders[2],
            person=persons[2],
        )
        task_section_d = TaskSection.objects.create(
            name="done",
            taskFolder=task_folders[3],
            person=persons[3],
        )
        task_section_e = TaskSection.objects.create(
            name="done",
            taskFolder=task_folders[4],
            person=persons[4],
        )
        return [task_section_a, task_section_b, task_section_c, task_section_d, task_section_e]


    def _create_tasks(persons, task_folders, task_sections):

        tasks_a = Task.objects.create(
            name="task_a",
            taskSection=task_sections[0],
            taskFolder=task_folders[0],
            person=persons[0],
        )
        tasks_b = Task.objects.create(
            name="task_b",
            taskSection=task_sections[1],
            taskFolder=task_folders[1],
            person=persons[1],
        )
        tasks_c = Task.objects.create(
            name="task_c",
            taskSection=task_sections[2],
            taskFolder=task_folders[2],
            person=persons[2],
        )
        tasks_d = Task.objects.create(
            name="task_d",
            taskSection=task_sections[3],
            taskFolder=task_folders[3],
            person=persons[3],
        )
        tasks_e = Task.objects.create(
            name="task_e",
            taskSection=task_sections[4],
            taskFolder=task_folders[4],
            person=persons[4],
        )
        return [tasks_a, tasks_b, tasks_c, tasks_d, tasks_e]


    def _create_subTasks(persons, tasks):

        sub_task_a = SubTask.objects.create(
            name='sub_task_a',
            task=tasks[0],
            person=persons[0]
        )
        sub_task_b = SubTask.objects.create(
            name='sub_task_a',
            task=tasks[1],
            person=persons[1]
        )
        sub_task_c = SubTask.objects.create(
            name='sub_task_a',
            task=tasks[2],
            person=persons[2]
        )
        sub_task_d = SubTask.objects.create(
            name='sub_task_a',
            task=tasks[3],
            person=persons[3]
        )
        sub_task_e = SubTask.objects.create(
            name='sub_task_a',
            task=tasks[4],
            person=persons[4]
        )
        return [sub_task_a, sub_task_b, sub_task_c, sub_task_d, sub_task_e, ]
