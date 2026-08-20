# Table of contents <!-- omit in toc -->

- [1. Oasis task manager](#1-oasis-task-manager)
- [2. Step by step guide from scratch](#2-step-by-step-guide-from-scratch)
  - [2.1. Initialze a DRF project with database setup](#21-initialze-a-drf-project-with-database-setup)
  - [2.2. Creating `tasks` app](#22-creating-tasks-app)
  - [2.3. Creating `Task` model](#23-creating-task-model)
  - [2.4. Creating a Serializer class for Task](#24-creating-a-serializer-class-for-task)

# 1. Oasis task manager

Oasis Task Manager is a modern task management application designed to help users organise and manage their tasks efficiently. Users can create, edit and delete tasks, organise them into folders, and mark some tasks as importent, or completed.

The application is built with Django REST Framework (DRF) and React, with PostgreSQL as the primary database. The backend provides a RESTful API for managing users, folders, and tasks, while the React frontend provides the interactive user interface.

# 2. Step by step guide from scratch

## 2.1. Initialze a DRF project with database setup

1. [Follow this guide](https://tinyurl.com/2hwk68af) to create a django project with `PostgreSQL` database setup.

2. We'll need to add the `rest_framework` app to `INSTALLED_APPS`. Let's edit the `config/settings.py` file:

   ```py
   INSTALLED_APPS = [
       # ...
       'rest_framework',
   ]
   ```

## 2.2. Creating `tasks` app

1. Now, we can create an app that we'll use to create a Web API.

   ```bash
   python manage.py startapp tasks
   ```

2. We'll need to add our new `tasks` app to `INSTALLED_APPS`. Let's edit the `config/settings.py` file:

   ```py
   INSTALLED_APPS = [
       # ...
       'rest_framework',
       'tasks', # new
   ]
   ```

## 2.3. Creating `Task` model

Start by creating a `Task` model that is used to manage store tasks. Edit the `tasks/models.py` file:

```py
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
```

We'll also need to create an migration for Task model and sync the database.

```bash
python manage.py makemigrations tasks
python manage.py migrate
```

Commit changes to Git.

## 2.4. Creating a Serializer class for Task

To get started on our Web API, we need provide a way of serializing and deserializing the `task` instances into representations such as `json`. We can do this by declaring serializers. Create a file in the `tasks` directory named `serializers.py` and add the following:

`tasks/serializers.py`

```py
from rest_framework import serializers

from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "completed", "important", "created_at", "updated_at"]
```

REST framework includes both `Serializer` classes, and `ModelSerializer` classes. We used the latter to make our code concise.

You can inspect all the fields in a serializer instance, by printing its representation. Start the Django shell, then try the following:

```bash
$ python manage.py shell
```

```py
>>> from tasks.serializers import TaskSerializer
>>> serializer = TaskSerializer()

>>> print(repr(serializer))
TaskSerializer():
    id = BigIntegerField(label='ID', read_only=True)
    title = CharField(max_length=255)
    completed = BooleanField(required=False)
    important = BooleanField(required=False)
    created_at = DateTimeField(read_only=True)
    updated_at = DateTimeField(read_only=True)
```
