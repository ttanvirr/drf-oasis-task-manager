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
      - [2.6.7.2. Using mixins](#2672-using-mixins)
      - [2.6.7.3. Using generic class-based views](#2673-using-generic-class-based-views)
  - [2.7. Authentication \& Permissions](#27-authentication--permissions)
    - [2.7.1. Adding owner field to our model](#271-adding-owner-field-to-our-model)
    - [2.7.2. Creating test users](#272-creating-test-users)
    - [2.7.3. Adding endpoints for our User models](#273-adding-endpoints-for-our-user-models)
      - [2.7.3.1. Create UserSerializer](#2731-create-userserializer)
      - [2.7.3.2. User views](#2732-user-views)
      - [2.7.3.3. Url patterns](#2733-url-patterns)
    - [2.7.4. Adding required permissions to user views](#274-adding-required-permissions-to-user-views)
    - [2.7.5. Associating tasks with users](#275-associating-tasks-with-users)
    - [2.7.6. Updating our `TaskSerializer`](#276-updating-our-taskserializer)
    - [2.7.7. Adding required permissions to task views](#277-adding-required-permissions-to-task-views)
    - [2.7.8. Adding login to the Browsable API](#278-adding-login-to-the-browsable-api)
    - [2.7.9. Object level permissions](#279-object-level-permissions)
    - [2.7.10. Restricting Task lists](#2710-restricting-task-lists)
    - [2.7.11. Restricting User endpoints](#2711-restricting-user-endpoints)
    - [2.7.12. Authenticating requests](#2712-authenticating-requests)

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

Let's refactor our `tasks/views.py` as follows:

```py
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer


class TaskList(APIView):
    """
    List all tasks (GET), or create a new task (POST).
    """

    def get(self, request, format=None):
        tasks = Task.objects.all()
        # serialize the tasks into python native data types (here a list of dictionaries)
        # many=True indicates that we want to serialize multiple instances (tasks)
        serializer = TaskSerializer(tasks, many=True)
        # convert python data into json and return the JSON response
        return Response(serializer.data)

    def post(self, request, format=None):
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


class TaskDetail(APIView):
    """
    Retrieve (GET), update (PUT), or delete (DELETE) a single task.
    """

    def get_object(self, pk):
        return get_object_or_404(Task, pk=pk)

    def get(self, request, pk, format=None):
        # Get task instance
        task = self.get_object(pk)
        # Serialize task instance into python data type (here dictionery)
        serializer = TaskSerializer(task)
        # Return json response
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        # Get task instance
        task = self.get_object(pk)
        # Deserialize requested data to validate it
        # `task` -> existing instance we want to update
        serializer = TaskSerializer(task, data=request.data)

        if serializer.is_valid():
            # Update task instance
            serializer.save()
            # Return json response
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        # Get task instance
        task = self.get_object(pk)
        # Delete task instance
        task.delete()
        # Return json response
        return Response(status=status.HTTP_204_NO_CONTENT)
```

It looks pretty similar to the previous function-based views, but we've got better separation between the different 'HTTP methods'.

We'll also need to refactor our `tasks/urls.py` slightly now that we're using class-based views (similar to regular django).

```py
#...

urlpatterns = [
    path("tasks/", views.TaskList.as_view()),
    path("tasks/<int:pk>/", views.TaskDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
```

Okay, we're done. If you run the development server everything should be working just as before.

[⬆️ Return to Table of contents](#table-of-contents)

#### 2.6.7.2. Using mixins

Class-based views allows us to easily compose reusable behavior.

The create/retrieve/update/delete operations that we've been using so far are going to be pretty similar for any model-backed API views we create. Those bits of common behavior are implemented in REST framework's mixin classes.

Here's our `TaskList` view in `tasks/views.py` module again:

```py
from rest_framework import mixins, generics

from .models import Task
from .serializers import TaskSerializer

class TaskList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """
    List all tasks (GET), or create a new task (POST).
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        # List all tasks
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Create new task
        return self.create(request, *args, **kwargs)
```

Here, we're building our view using `GenericAPIView`, and adding in `ListModelMixin` and `CreateModelMixin`.

The base class provides the core functionality, and the mixin classes provide the `.list()` and `.create()` actions. We're then explicitly binding the `get` and `post` methods to the appropriate actions.

Now modify the detail view:

```py
class TaskDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """
    Retrieve (GET), update (PUT), or delete (DELETE) a single task.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        # Get single task instance
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        # Update single task instance
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # Delete single task instance
        return self.destroy(request, *args, **kwargs)
```

Again we're using the `GenericAPIView` class to provide the core functionality, and adding in mixins to provide the `.retrieve()`, `.update()` and `.destroy()` actions.

Run the development server and make sure everything is working as expected.

[⬆️ Return to Table of contents](#table-of-contents)

#### 2.6.7.3. Using generic class-based views

REST framework provides a set of already mixed-in generic views that we can use to trim down our `views.py` module even more.

`tasks/views.py`

```py
from rest_framework import generics

from .models import Task
from .serializers import TaskSerializer


class TaskList(generics.ListCreateAPIView):
    """
    List all tasks (GET), or create a new task (POST).
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve (GET), update (PUT), or delete (DELETE) a single task.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

```

We've gotten a huge amount for free, and our code looks like good, clean, idiomatic Django.

Again, run the development server and make sure everything is working as expected.

[⬆️ Return to Table of contents](#table-of-contents)

## 2.7. Authentication & Permissions

Currently, our API does not have any restrictions on who can access or modify tasks and users. We'd like to add authentication and permissions so that:

- Users can create their own accounts.
- Users can log in and authenticate API requests.
- Users can read and update only their own profile.
- Superusers can read and update other users.
- Tasks are always associated with their creator.
- Only authenticated users may create tasks.
- Only the creator of a task may update or delete it.
- Unauthenticated users may still read tasks.

We will first work on restricting tasks and then users.

We will use Django's built-in User model and DRF's built-in token authentication.

### 2.7.1. Adding owner field to our model

To associate every task with the user who created it, we'll add an owner field to our Task model.

Edit `tasks/models.py`:

```py
class Task(models.Model):
    # ...
    owner = models.ForeignKey(
        "auth.User", related_name="tasks", on_delete=models.CASCADE
    )

    # ...
```

When that's all done we'll need to update our database tables. Normally we'd create a database migration in order to do that, but for our convenience, let's just delete the existing database and migrations and then recreate the database using following command and start again.

```bash
createdb -U <db_user> <db_name>
```

the `<db_user>` and `<db_name>` should match the ones set in the `.env` file

Then:

```bash
rm -r tasks/migrations
uv run manage.py makemigrations tasks
uv run manage.py migrate
```

[⬆️ Return to Table of contents](#table-of-contents)

### 2.7.2. Creating test users

We'll create a few different users to test the API's authentication and object-level permissions.

First, create a superuser:

```bash
uv run manage.py createsuperuser
```

Creat one or two more superusers using the same command.

We'll also need some normal users. These can be created directly through the Django shell.

```bash
uv run manage.py shell
```

In the shell, create a few normal users:

```py
from django.contrib.auth.models import User

User.objects.create_user(
    username="alice",
    password="testpass123",
)

User.objects.create_user(
    username="bob",
    password="testpass123",
)
```

> [!TIP]
> We used `create_user()` instead of `create()` so that Django hashes the passwords before storing them in the database.

You can verify that the users were created:

```py
User.objects.values("username", "is_superuser")
```

You should see something similar to:

```
<QuerySet [
    {'username': 'admin', 'is_superuser': True},
    {'username': 'alice', 'is_superuser': False},
    {'username': 'bob', 'is_superuser': False},
]>
```

We'll use the superuser to test administrator access, and the normal users to test ownership restrictions.

[⬆️ Return to Table of contents](#table-of-contents)

### 2.7.3. Adding endpoints for our User models

We want to expose user-related endpoints with different purposes:

- `POST /users/register/` — create a new account.
- `GET /users/me/` — retrieve the currently authenticated user's profile.
- `PUT/PATCH /users/me/` — update the currently authenticated user's profile.
- `GET /users/` — list users, available only to superusers.
- `GET /users/<id>/` — retrieve a user, available only to superusers.
- `PUT/PATCH /users/<id>/` — update a user, available only to superusers.

Notice that registration is deliberately separate from `/users/`.

`/users/register/` represents the action of creating a new account, while `/users/` represents administrative access to existing users.

#### 2.7.3.1. Create UserSerializer

Now that we've got some users to work with, let's add representations of those users to our API.

We'll use one serializer for registration and another for reading and updating user profiles.

First, Create `UserRegistrationSerializer` in `tasks/serializers.py`:

```py
from django.contrib.auth.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
```

The password is marked as `write_only` so it can be submitted when creating an account but is never included in API responses.

We use `create_user()` rather than `create()` so that Django automatically hashes the password before storing it.

Now create the serializer used for existing users:

```py
class UserSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True,)

    class Meta:
        model = User
        fields = ["id", "username", "tasks"]
```

Because `tasks` is a reverse relationship on the `User` model, it will not be included by default when using the `ModelSerializer` class, so we needed to add an explicit field for it.

The `tasks` field is read-only. Clients should never be allowed to assign tasks to a user through the user API. Task ownership is determined when a task is created.

> [!NOTE]
> Here, `tasks` exists only in the serialized representation (e.g., JSON). It does not modify the database or the `User` model.

[⬆️ Return to Table of contents](#table-of-contents)

#### 2.7.3.2. User views

Now we'll create views for registration, the current user's profile, and administrative user management.

Edit `tasks/views.py`

```py
from django.contrib.auth.models import User

from .serializers import UserRegistrationSerializer, UserSerializer

class UserRegistration(generics.CreateAPIView):
    """
    Create a new user account.
    """

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


class UserMe(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update the currently authenticated user.
    """

    serializer_class = UserSerializer

    def get_object(self):
        """We won't receive a pk in the URL, so we return the currently authenticated user."""
        return self.request.user


class UserList(generics.ListAPIView):
    """
    List all users (GET).
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve (GET) or update (PUT) a single user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
```

[⬆️ Return to Table of contents](#table-of-contents)

#### 2.7.3.3. Url patterns

Finally we need to add those views into the API, by referencing them from the URLconf. Add the following to the patterns in `tasks/urls.py`.

```py
path("users/register/", views.UserRegistration.as_view()),
path("users/me/", views.UserMe.as_view()),
path("users/", views.UserList.as_view()),
path("users/<int:pk>/", views.UserDetail.as_view()),
```

Open the browsable API in the browser and verify that the new endpoints return the expected user representations.

### 2.7.4. Adding required permissions to user views

We want to make sure that users can only be accessed based on authentication.

REST framework includes a number of permission classes to restrict who can access a given view. For this stage, we'll use `AllowAny`, and `IsAuthenticated`.

1. First add the following import in the `tasks/views.py` module

   ```py
   from rest_framework import permissions
   ```

2. Then, add the permission classes to the user views.

   ```py
   class UserRegistration(generics.CreateAPIView):
        # Allow anyone to register
        permission_classes = [permissions.AllowAny]

    class UserMe(generics.RetrieveUpdateAPIView):
        # authenticated users can read or update their own profile
        permission_classes = [permissions.IsAuthenticated]

    class UserList(generics.ListAPIView):
        # authenticated users can read users
        permission_classes = [permissions.IsAuthenticated]


    class UserDetail(generics.RetrieveUpdateAPIView):
        permission_classes = [permissions.IsAuthenticated]
   ```

Open the browsable API in the browser and verify that the new endpoints return the expected user representations.

[⬆️ Return to Table of contents](#table-of-contents)

### 2.7.5. Associating tasks with users

Right now, if we created a task, there'd be no way of associating the user that created the task, with the task instance. The user isn't sent as part of the serialized representation, but is instead a property of the incoming request.

The way we deal with that is by overriding a `.perform_create()` method on our task views, that allows us to modify how the instance save is managed, and handle any information that is implicit in the incoming request or requested URL.

On the `TaskList` view class, add the following method:

`tasks/views.py`

```py
def perform_create(self, serializer):
    # associate authenticated user with a new task
    serializer.save(owner=self.request.user)
```

The `create()` method of our serializer will now be passed an additional `'owner'` field, along with the validated data from the request.

> [!NOTE]
> You might think the `'Task'` model already has `'owner'` field. So why again associating a task with an user?
>
> Yes, every task has an `owner` field. But who sets its value?
>
> This is why the view saves the authenticated (logged in) user as the `owner`. Here `self.request.user` is the authenticated user.

### 2.7.6. Updating our `TaskSerializer`

Now that tasks are associated with the user that created them, let's update our `TaskSerializer` to reflect that.

1. Add the `owner` field as a read-only field to the `TaskSerializer` definition in `tasks/serializers.py`:

   ```py
   owner = serializers.ReadOnlyField(source="owner.username")
   ```

2. Make sure you also add `'owner'`, to the list of fields in the inner `Meta` class.

The `source` argument controls which attribute is used to populate a field (and can point at any attribute on the serialized instance).

The field we've added is the untyped `ReadOnlyField` class, in contrast to the other typed fields, such as `CharField`, `BooleanField` etc... The untyped `ReadOnlyField` is always read-only, and will be used for serialized representations, but will not be used for updating model instances when they are deserialized. We could have also used `CharField(read_only=True)` here.

### 2.7.7. Adding required permissions to task views

Now that tasks are associated with users, we want to make sure that tasks and users can only be accessed based on authentication and ownership.

At this stage, we'll require users to be authenticated before accessing the task and user endpoints. We will add ownership restrictions in later sections.

REST framework includes a number of permission classes to restrict who can access a given view. For this stage, we'll use `IsAuthenticated`, which requires users to be authenticated before they can access the view.

1. First add the following import in the `tasks/views.py` module

   ```py
   from rest_framework import permissions
   ```

2. Then, add the following property to the `TaskList`, `TaskDetail`, `UserList` and `UserDetail` view classes.

   ```py
   permission_classes = [permissions.IsAuthenticated]
   ```

This ensures that anonymous users cannot access any of these endpoints.

### 2.7.8. Adding login to the Browsable API

If you open a browser and navigate to the browsable API at the moment, you'll find that you're no longer able to create new tasks. In order to do so we'd need to be able to login as a user.

At the end of our project-level `config/urls.py` file, add a pattern to include the login and logout views for the browsable API.

```py
urlpatterns += [
    # include the login and logout views for the browsable API
    path("api-auth/", include("rest_framework.urls")),
]
```

The `'api-auth/'` part of pattern can actually be whatever URL you want to use.

Now if you open up the browser again and refresh the page you'll see a `'Login'` link in the top right of the page which redirects to `/api-auth/login/` page. If you log in as one of the users you created earlier, you'll be able to create tasks again (as well as update and delete any tasks even that were created by other users, which we'll fix next).

Once you've created a few tasks, navigate to the `'/users/'` endpoint, and notice that the representation includes a list of the task ids that are associated with each user, in each user's `'tasks'` field.

### 2.7.9. Object level permissions

At the moment, any authenticated user can access tasks, including tasks created by other users.

We want to make our API creator-related:

- A normal authenticated user can read, update and delete only their own tasks.
- A superuser can read, update and delete all tasks.
- Users must be authenticated to access the tasks and users.

To enforce ownership at the object level, we need to create a custom permission.

In the `tasks` app, create a new file, `permissions.py` with following content:

`tasks/permissions.py`

```py
from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission that allows only the owner or a superuser to access an object.

    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed if current user = owner of the requested object.
        return request.user.is_superuser or obj.owner == request.user
```

Now add that custom permission to our task instance endpoint, by editing the `permission_classes` property on the `TaskDetail` view class:

`tasks/views.py/TaskDetail`

```py
from tasks.permissions import IsOwnerOrAdmin

class taskDetail(generics.RetrieveUpdateDestroyAPIView):
    #...
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
```

The `IsAuthenticated` permission ensures that only logged-in users can access the endpoint, while `IsOwnerOrAdmin` ensures that the authenticated user is either the task owner or a superuser.

Now, check on a browser again.

### 2.7.10. Restricting Task lists

The `TaskList` view needs an additional restriction. Unlike a detail view, a list view does not perform object-level permission checks on every object in the queryset. Therefore, we need to filter the queryset so that normal users only receive their own tasks.

Update the `TaskList` view as follows:

`tasks/views.py`

```py
class TaskList(generics.ListCreateAPIView):
    """
    List all tasks (GET), or create a new task (POST).
    """

    serializer_class = TaskSerializer
    # authenticated users can read or create tasks,
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # associate authenticated user with a new task
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Task.objects.all()
        return Task.objects.filter(owner=self.request.user)
```

### 2.7.11. Restricting User endpoints

### 2.7.12. Authenticating requests

When we interact with the API through the web browser, we can login, and the browser session will then provide the required authentication for the requests.

When using HTTP Basic Authentication, the client sends the username and password with each request that requires authentication.

If we try to create a task without authenticating, we'll get an error:

```bash
http POST http://127.0.0.1:8000/tasks/ title="Some task"

{
"detail": "Authentication credentials were not provided."
}
```

We can make a successful request by including the username and password of one of the users we created earlier.

```bash
http -a <user>:<password> POST http://127.0.0.1:8000/tasks/ title="Some task"

{
    "completed": false,
    "created_at": "2026-09-01T00:54:05.410481Z",
    "id": 6,
    "important": false,
    "owner": "usertwo",
    "title": "Some task",
    "updated_at": "2026-09-01T00:54:05.410534Z"
}
```

We haven't set up any custom authentication classes, so DRF's defaults are currently applied, which are `SessionAuthentication` and `BasicAuthentication`.
So, in a client application, we can use Basic Authorization (providing a username and password) to authenticate while creating, deleting or updating tasks.
