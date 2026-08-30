# Table of contents <!-- omit in toc -->

- [1. Oasis task manager](#1-oasis-task-manager)
- [2. Step by step guide from scratch](#2-step-by-step-guide-from-scratch)
  - [2.1. Initialze a DRF project with database setup](#21-initialze-a-drf-project-with-database-setup)
  - [2.2. Creating `tasks` app](#22-creating-tasks-app)
  - [2.3. Creating `Task` model](#23-creating-task-model)
  - [2.4. Creating a Serializer class for Task](#24-creating-a-serializer-class-for-task)
    - [2.4.1. Working with Serializers](#241-working-with-serializers)
      - [2.4.1.1. Create some tasks](#2411-create-some-tasks)
      - [2.4.1.2. Serializing a task instance](#2412-serializing-a-task-instance)
      - [2.4.1.3. Deserializing](#2413-deserializing)
  - [2.5. Request and responses](#25-request-and-responses)
  - [2.6. Creating API views using our serializer](#26-creating-api-views-using-our-serializer)
    - [2.6.1. Function-based views](#261-function-based-views)
    - [2.6.2. URLs for function-based views](#262-urls-for-function-based-views)
    - [2.6.3. Testing our first attempt at a Web API](#263-testing-our-first-attempt-at-a-web-api)
    - [2.6.4. Adding optional format suffixes to our URLs](#264-adding-optional-format-suffixes-to-our-urls)
    - [2.6.5. How's it looking?](#265-hows-it-looking)
    - [2.6.6. Browsability](#266-browsability)
    - [2.6.7. Class-based Views](#267-class-based-views)
      - [2.6.7.1. Rewriting our API using class-based views](#2671-rewriting-our-api-using-class-based-views)

# 1. Oasis task manager

Oasis Task Manager is a modern task management application designed to help users organise and manage their tasks efficiently. Users can create, edit and delete tasks, organise them into folders, and mark some tasks as importent, or completed.

The application is built with Django REST Framework (DRF) and React, with PostgreSQL as the primary database. The backend provides a RESTful API for managing users, folders, and tasks, while the React frontend provides the interactive user interface. We'll use `uv` tool to manage our development environment.

# 2. Step by step guide from scratch

## 2.1. Initialze a DRF project with database setup

1. [Follow this guide](https://tinyurl.com/2hwk68af) to create a django project with `PostgreSQL` database setup (use `uv` tool).

2. Install django rest framework:

   ```bash
   uv add djangorestframework
   ```

3. We'll need to add the `rest_framework` app to `INSTALLED_APPS`. Let's edit the `config/settings.py` file:

   ```py
   INSTALLED_APPS = [
       # ...
       'rest_framework',
   ]
   ```

[⬆️ Return to Table of contents](#table-of-contents)

## 2.2. Creating `tasks` app

1. Now, we can create an app that we'll use to create a Web API.

   ```bash
   uv run manage.py startapp tasks
   ```

2. We'll need to add our new `tasks` app to `INSTALLED_APPS`. Let's edit the `config/settings.py` file:

   ```py
   INSTALLED_APPS = [
       # ...
       'rest_framework',
       'tasks', # new
   ]
   ```

[⬆️ Return to Table of contents](#table-of-contents)

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

We'll also need to create an migration for `Task` model and sync the database.

```bash
uv run manage.py makemigrations tasks
uv run manage.py migrate
```

Commit changes to Git.

[⬆️ Return to Table of contents](#table-of-contents)

## 2.4. Creating a Serializer class for Task

To get started on our Web API, we need to provide a way of serializing and deserializing the `Task` instances into representations such as `json`. We can do this by declaring serializers. Create a file in the `tasks` directory named `serializers.py` and add the following model serializer class:

`tasks/serializers.py`

```py
from rest_framework import serializers

from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "completed", "important", "created_at", "updated_at"]
```

REST framework includes both `Serializer` and `ModelSerializer` classes. We used the latter to make our code concise.

You can inspect all the fields in a serializer instance, by printing its representation. Start the Django shell, then try the following:

```bash
uv run manage.py shell
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

[⬆️ Return to Table of contents](#table-of-contents)

### 2.4.1. Working with Serializers

(Some of the follwoing sections will demonstrate the serialization and deserialization process. You can skip to the [Creating API views](#26-creating-api-views-using-our-serializer) section if you want.)

Let's drop into the Django shell.

```bash
uv run manage.py shell
```

#### 2.4.1.1. Create some tasks

Now, let's create a couple of tasks to work with.

```py
>>> from tasks.models import Task
>>> from tasks.serializers import TaskSerializer
>>> from rest_framework.renderers import JSONRenderer
>>> from rest_framework.parsers import JSONParser
>>>
>>> task = Task(title="First task")
>>> task.save()
>>>
>>> task = Task(title="Second task", important=True)
>>> task.save()
```

#### 2.4.1.2. Serializing a task instance

We've now got a few task instances to play with. Let's take a look at serializing one of those instances.

```py
>>> serializer = TaskSerializer(task)
>>> serializer.data
{'id': 2, 'title': 'Second task', 'completed': False, 'important': True, 'created_at': '2026-08-20T04:25:42.608011Z', 'updated_at': '2026-08-20T04:25:42.608025Z'}
```

At this point we've translated the model instance into Python native datatypes (in this case python dictionary). To finalize the serialization process we render the data into `json`.

```
>>> content = JSONRenderer().render(serializer.data)
>>> content
b'{"id":2,"title":"Second task","completed":false,"important":true,"created_at":"2026-08-20T04:25:42.608011Z","updated_at":"2026-08-20T04:25:42.608025Z"}'
```

#### 2.4.1.3. Deserializing

Deserialization is similar.

First we need to convert `json` data, because `JSONParser().parse()` expects a stream of bytes, not a JSON string or Python dictionary.

Then we parse the stream into Python native datatypes...

```py
>>> import io
>>>
>>> stream = io.BytesIO(content)
>>> data = JSONParser().parse(stream)
>>> data
{'id': 2, 'title': 'Second task', 'completed': False, 'important': True, 'created_at': '2026-08-20T04:25:42.608011Z', 'updated_at': '2026-08-20T04:25:42.608025Z'}
```

...then we restore those native python datatypes into a fully populated object instance (updated task instance).

```py
>>> serializer = TaskSerializer(data=data)
>>> serializer.is_valid()
True
>>> serializer.validated_data
{'title': 'Second task', 'completed': False, 'important': True}
>>> serializer.save()
<Task: Second task>
```

We can also serialize querysets (all instances) instead of a single model instances. To do so we simply add a `many=True` flag to the serializer arguments.

```py
>>> serializer = TaskSerializer(Task.objects.all(), many=True)
>>> serializer.data
[{'id': 2, 'title': 'Second task', 'completed': False, 'important': True, 'created_at': '2026-08-30T21:42:49.403893Z', 'updated_at': '2026-08-30T21:42:49.403937Z'}, {'id': 1, 'title': 'First task', 'completed': False, 'important': True, 'created_at': '2026-08-30T21:24:30.044611Z', 'updated_at': '2026-08-30T21:24:30.044647Z'}]
```

Here, we got a list of python dictioneries.

[⬆️ Return to Table of contents](#table-of-contents)

## 2.5. Request and responses

### Request objects <!-- omit in toc -->

REST framework introduces a `Request` object that extends the regular `HttpRequest`, and provides more flexible request parsing. The core functionality of the `Request` object is the `request.data` attribute, which is similar to `request.POST`, but more useful for working with Web APIs.

```py
request.POST # Only handles form data. Only works for 'POST' method.
request.data # Handles arbitrary data. Works for 'POST', 'PUT' and 'PATCH' methods.
```

### Response objects <!-- omit in toc -->

REST framework also introduces a `Response` object, which is a type of `TemplateResponse` that takes unrendered content and uses content negotiation to determine the correct content type to return to the client.

```py
return Response(data) # Renders to content type as requested by the client.
```

[⬆️ Return to Table of contents](#table-of-contents)

## 2.6. Creating API views using our serializer

REST framework provides two wrappers you can use to write API views:

1. The `@api_view` decorator for working with function based views.
2. The `APIView` class for working with class-based views.

These wrappers provide functionalities such as making sure you receive `Request` instances in your view, and adding context to `Response` objects.

The wrappers also provide behavior such as returning `405 Method Not Allowed` responses when appropriate, and handling any `ParseError` exceptions that occur when accessing `request.data` with malformed input.

Okay, first, we'll work with function-based views to understand things more explicitely, and then will use class-based views for conciseness. But finally we'll use ViewSets.

### 2.6.1. Function-based views

`tasks/views`

```py
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer


@api_view(["GET", "POST"])
def task_list(request):
    """
    List all tasks (GET), or create a new task (POST).
    """

    if request.method == "GET":
        tasks = Task.objects.all()
        # serialize the tasks into python native data types (here a list of dictionaries)
        # many=True indicates that we want to serialize multiple instances (tasks)
        serializer = TaskSerializer(tasks, many=True)
        # convert python data into json and return the JSON response
        return Response(serializer.data)

    elif request.method == "POST":
        # resquest body contains json bytes (not raw json)
        # DRF's request handling process parses those bytes before
        # your view gets request.data
        # Deserialize python data for validation
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            # save the new task instance
            serializer.save()
            # Return json response
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def task_detail(request, pk):
    """
    Retrieve (GET), update (PUT), or delete (DELETE) a single task.
    """

    task = get_object_or_404(Task, pk=pk)

    if request.method == "GET":
        # Serialize task instance into python data type (here dictionery)
        serializer = TaskSerializer(task)
        # Return json response
        return Response(serializer.data)

    elif request.method == "PUT":
        # Deserialize requested data to validate it
        # `task` -> existing instance we want to update
        serializer = TaskSerializer(task, data=request.data)

        if serializer.is_valid():
            # Update task instance
            serializer.save()
            # Return json response
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        # Delete task instance
        task.delete()
        # Return a simple http response
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
```

[⬆️ Return to Table of contents](#table-of-contents)

### 2.6.2. URLs for function-based views

Finally we need to wire these views up. Create the `tasks/urls.py` file:

`tasks/urls.py`

```py
from django.urls import path

from tasks import views

urlpatterns = [
    path("tasks/", views.task_list),
    path("tasks/<int:pk>/", views.task_detail),
]
```

We also need to wire up the root urlconf in the `config/urls.py` file, to include our `tasks` app's URLs.

`config/urls.py`

```py
from django.urls import path, include

urlpatterns = [
path("", include("tasks.urls")),
]
```

It's worth noting that If we send malformed `json`, or if a request is made with a method that the view doesn't handle, then we'll end up with a `500 "server error"` response. Still, this'll do for now.

[⬆️ Return to Table of contents](#table-of-contents)

### 2.6.3. Testing our first attempt at a Web API

Now we can start up a sample server that serves our `tasks`.

Start up Django's development server.

```bash
uv run manage.py runserver
```

In another terminal window, we can test the server.

We can test our API using `curl` or `HTTPie`. `HTTPie` is a user-friendly http client that's written in Python. Let's install that globally using `uv` (don't add it as a project dependency):

```bash
uv tool install httpie
```

Finally, we can get a list of all of the tasks:

```bash
http GET http://127.0.0.1:8000/tasks/ --unsorted
```

Or we can get a particular task by referencing its id:

```bash
http GET http://127.0.0.1:8000/tasks/2/ --unsorted
```

> [!NOTE]
> Don't forget the trailing slash `/` at the end of the URL. Because these should match our defined urlpatterns.

Similarly, you can have the same json displayed by visiting these URLs in a web browser.

[⬆️ Return to Table of contents](#table-of-contents)

### 2.6.4. Adding optional format suffixes to our URLs

To take advantage of the fact that our responses are no longer hardwired to a single content type let's add support for format suffixes to our API endpoints. Using format suffixes gives us URLs that explicitly refer to a given format, and means our API will be able to handle URLs such as http://example.com/api/items/4.json.

Start by adding a `format` keyword argument to both of the views, like:

`tasks/views.py`

```py
# ...
def task_list(request, format=None):
    # ...

def task_detail(request, pk, format=None):
    # ...
```

Now update the `tasks/urls.py` file slightly, to append a set of `format_suffix_patterns` in addition to the existing URLs:

`tasks/urls.py`

```py
from rest_framework.urlpatterns import format_suffix_patterns # new

urlpatterns = [
# ...
]

urlpatterns = format_suffix_patterns(urlpatterns) # new
```

[⬆️ Return to Table of contents](#table-of-contents)

### 2.6.5. How's it looking?

Now we can control the format of the response that we get back, either by using the Accept header:

```bash
http http://127.0.0.1:8000/tasks/ Accept:application/json  # Request JSON
http http://127.0.0.1:8000/tasks/ Accept:text/html         # Request HTML
```

Or by appending a format suffix:

```bash
http http://127.0.0.1:8000/tasks.json  # JSON suffix
http http://127.0.0.1:8000/tasks.api   # Browsable API suffix
```

Similarly, we can control the format of the request that we send, using the `Content-Type` header.

```bash
# POST using form data
http --form POST http://127.0.0.1:8000/tasks/ title="Third task"

# POST using JSON
http --json POST http://127.0.0.1:8000/tasks/ title="Fifth task"
```

If you add a `--debug` switch to the http requests above, you will be able to see the request type in request headers.

Now go and open the API in a web browser, by visiting http://127.0.0.1:8000/tasks/.

> [!TIP]
> We can also test our API with all type of http requests using `Postman` tool.

### 2.6.6. Browsability

Because the API chooses the content type of the response based on the client request, it will, by default, return an HTML-formatted representation of the resource when that resource is requested by a web browser. This allows for the API to return a fully web-browsable HTML representation.

Having a web-browsable API also lowers the barrier for other developers wanting to inspect and work with your API.

See the [browsable api topic](https://tinyurl.com/mvbkcm88) for more information about the browsable API feature and how to customize it.

[⬆️ Return to Table of contents](#table-of-contents)

### 2.6.7. Class-based Views

We can also write our API views using class-based views. As it allows us to reuse common functionality, and helps us keep our code `DRY`.

#### 2.6.7.1. Rewriting our API using class-based views

Let's refactor our `tasks/views.py`:

```py

```
