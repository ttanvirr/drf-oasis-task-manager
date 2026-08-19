# Table of contents <!-- omit in toc -->

- [1. Oasis task manager](#1-oasis-task-manager)
- [2. Step by step guide from scratch](#2-step-by-step-guide-from-scratch)
  - [2.1. Initialze project](#21-initialze-project)
  - [2.2. Creating `tasks` app](#22-creating-tasks-app)
  - [2.3. Creating `Task` model](#23-creating-task-model)

# 1. Oasis task manager

Oasis Task Manager is a modern task management application designed to help users organise and manage their tasks efficiently. Users can create, edit and delete tasks, organise them into folders, and mark some tasks as importent, or completed.

The application is built with Django REST Framework (DRF) and React, with PostgreSQL as the primary database. The backend provides a RESTful API for managing users, folders, and tasks, while the React frontend provides the interactive user interface.

# 2. Step by step guide from scratch

## 2.1. Initialze project

1. Create a project directory (whatever name). Then navigate to the directory.
2. create a new virtual environment called `.venv`, using `venv`. Then Activate the venv.

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Put `.venv/` in the `.gitignore` file.
4. Now that we're inside a virtual environment, we can install our package requirements:

   ```bash
   pip install django
   pip install djangorestframework
   pip freeze > requirements.txt
   ```

5. Let's create the project core inside our root directory `.`. We'll name the core directory as `config`:

   ```bash
   django-admin startproject config .
   ```

6. We'll need to add the `rest_framework` app to `INSTALLED_APPS`. Let's edit the `config/settings.py` file:

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

We'll also need to create an initial migration sync the database for the first time.

```bash
python manage.py makemigrations tasks
python manage.py migrate tasks
```

Commit changes to Git.
