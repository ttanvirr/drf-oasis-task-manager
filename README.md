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
    - [2.7.2. Adding endpoints for our User models](#272-adding-endpoints-for-our-user-models)
      - [2.7.2.1. Create UserSerializer](#2721-create-userserializer)
      - [2.7.2.2. User views](#2722-user-views)
      - [2.7.2.3. Url patterns](#2723-url-patterns)
    - [2.7.3. Associating tasks with users](#273-associating-tasks-with-users)
    - [2.7.4. Updating our `TaskSerializer`](#274-updating-our-taskserializer)
    - [2.7.5. Adding required permissions to views](#275-adding-required-permissions-to-views)
    - [2.7.6. Adding login to the Browsable API](#276-adding-login-to-the-browsable-api)
    - [2.7.7. Object level permissions](#277-object-level-permissions)
    - [2.7.8. Authenticating requests](#278-authenticating-requests)
  - [2.8. Relationships \& Hyperlinked APIs](#28-relationships--hyperlinked-apis)
    - [2.8.1. Making sure our URL patterns are named](#281-making-sure-our-url-patterns-are-named)
    - [2.8.2. Update serializers](#282-update-serializers)
    - [2.8.3. Creating an endpoint for the root of our API](#283-creating-an-endpoint-for-the-root-of-our-api)
    - [2.8.4. Adding pagination](#284-adding-pagination)
  - [2.9. ViewSets \& Routers](#29-viewsets--routers)
    - [2.9.1. Refactoring to use ViewSets](#291-refactoring-to-use-viewsets)
    - [2.9.2. Binding ViewSets to URLs explicitly](#292-binding-viewsets-to-urls-explicitly)
    - [2.9.3. Using Routers](#293-using-routers)
    - [2.9.4. Trade-offs between views vs ViewSets](#294-trade-offs-between-views-vs-viewsets)
  - [2.10. Documenting our API](#210-documenting-our-api)
    - [2.10.1. `drf-spectacular`](#2101-drf-spectacular)
    - [2.10.2. Add the OpenAPI schema endpoint](#2102-add-the-openapi-schema-endpoint)
    - [2.10.3. Add Swagger UI](#2103-add-swagger-ui)
    - [Give the API some proper identity](#give-the-api-some-proper-identity)
    - [2.10.4. ReDoc?](#2104-redoc)
  - [2.11. Next steps](#211-next-steps)

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

Currently our API doesn't have any restrictions on who can edit or delete tasks. We'd like to have some more advanced behavior in order to make sure that:

- Tasks are always associated with a creator.
- Only authenticated users may create new tasks.
- Only the creator of a task may update or delete it.
- Unauthenticated requests should have full read-only access.

### 2.7.1. Adding owner field to our model

Let's add a field to our `Task` model to represent the user who created the task.

`tasks/models.py/Task`

```py
class Task(models.Model):
    # ...
    owner = models.ForeignKey(
        "auth.User", related_name="tasks", on_delete=models.CASCADE
    )

    # ...
```

When that's all done we'll need to update our database tables. Normally we'd create a database migration in order to do that, but for our convenience, let's just delete and recreate the database and start again.

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

You might also want to create a few different users, to use for testing the API. The quickest way to do this will be with the `createsuperuser` command. Let's create 3 superusers.

```bash
uv run manage.py createsuperuser
```

### 2.7.2. Adding endpoints for our User models

#### 2.7.2.1. Create UserSerializer

Now that we've got some users to work with, let's add representations of those users to our API. In `tasks/serializers.py` add:

```py
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(many=True, queryset=Task.objects.all())

    class Meta:
        model = User
        fields = ["id", "username", "tasks"]
```

Because `tasks` is a reverse relationship on the `User` model, it will not be included by default when using the `ModelSerializer` class, so we needed to add an explicit field for it.

> [!NOTE]
> Here, `tasks` exists only in the serialized representation (e.g., JSON). It does not modify the database or the `User` model.

#### 2.7.2.2. User views

We'd just use read-only views for the user representations, so we'll use the `ListAPIView` and `RetrieveAPIView` generic class-based views.

`tasks/views.py`

```py
from django.contrib.auth.models import User
from tasks.serializers import UserSerializer

class UserList(generics.ListAPIView):
    """
    List all users (GET).
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    """
    Retrieve (GET) a single user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
```

#### 2.7.2.3. Url patterns

Finally we need to add those views into the API, by referencing them from the URLconf. Add the following to the patterns in `tasks/urls.py`.

```py
path("users/", views.UserList.as_view()),
path("users/<int:pk>/", views.UserDetail.as_view()),
```

Check if the api endpoints show users or user.

### 2.7.3. Associating tasks with users

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

### 2.7.4. Updating our `TaskSerializer`

Now that tasks are associated with the user that created them, let's update our `TaskSerializer` to reflect that.

1. Add the `owner` field as a read-only field to the `TaskSerializer` definition in `tasks/serializers.py`:

   ```py
   owner = serializers.ReadOnlyField(source="owner.username")
   ```

2. Make sure you also add `'owner'`, to the list of fields in the inner `Meta` class.

The `source` argument controls which attribute is used to populate a field (and can point at any attribute on the serialized instance).

The field we've added is the untyped `ReadOnlyField` class, in contrast to the other typed fields, such as `CharField`, `BooleanField` etc... The untyped `ReadOnlyField` is always read-only, and will be used for serialized representations, but will not be used for updating model instances when they are deserialized. We could have also used `CharField(read_only=True)` here.

### 2.7.5. Adding required permissions to views

Now that tasks are associated with users, we want to make sure that only authenticated users are able to create, update and delete tasks.

REST framework includes a number of permission classes to restrict who can access a given view. In this case we'll use `IsAuthenticatedOrReadOnly`, which will ensure that authenticated requests get read-write access, and unauthenticated requests get read-only access.

1. First add the following import in the `tasks/views.py` module

   ```py
   from rest_framework import permissions
   ```

2. Then, add the following property to both the `TasktList` and `TasktDetail` view classes.

   ```py
   permission_classes = [permissions.IsAuthenticatedOrReadOnly]
   ```

### 2.7.6. Adding login to the Browsable API

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

### 2.7.7. Object level permissions

At the moment, any logged in user can update and delete tasks even that were created by other users.

We want to make sure that only the user that created the task is able to update or delete it.

To do that we need to create a custom permission.

In the `tasks` app, create a new file, `permissions.py` with following content:

`tasks/permissions.py`

```py
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed if current user = owner of the requested object.
        return obj.owner == request.user
```

Now add that custom permission to our task instance endpoint, by editing the `permission_classes` property on the `TaskDetail` view class:

`tasks/views.py/TaskDetail`

```py
from tasks.permissions import IsOwnerOrReadOnly

class taskDetail(generics.RetrieveUpdateDestroyAPIView):
    #...
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
```

Now, if you check on a browser again, you find that the `'DELETE'` and `'PUT'` actions only appear on a task instance endpoint if you're logged in as the same user that created the task.

### 2.7.8. Authenticating requests

When we interact with the API through the web browser, we can login, and the browser session will then provide the required authentication for the requests.

If we're interacting with the API programmatically we need to explicitly provide the authentication credentials on each request.

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

We haven't set up any authentication classes, so the defaults are currently applied, which are `SessionAuthentication` and `BasicAuthentication`.

> [!NOTE]
> In a api testing app, like `Postman`, use Basic Authorization to authenticate while creating, deleting or updating tasks.

## 2.8. Relationships & Hyperlinked APIs

At the moment relationships within our API are represented by using `primary keys`. In this part of the tutorial we'll improve the cohesion and discoverability of our API, by instead using `hyperlinking` for relationships.

Dealing with relationships between entities is one of the more challenging aspects of Web API design. There are a number of different ways that we might choose to represent a relationship:

- Using primary keys.
- Using hyperlinking between entities.
- Using a unique identifying slug field on the related entity.
- Using the default string representation of the related entity.
- Nesting the related entity inside the parent representation.
- Some other custom representation.

REST framework supports all of these styles.

In this case we'd like to use a hyperlinked style between entities. In order to do so, we'll modify our serializers to extend `HyperlinkedModelSerializer` instead of the existing `ModelSerializer`.

The `HyperlinkedModelSerializer` has the following differences from `ModelSerializer`:

- It does not include the `id` field by default.
- It includes a `url` field, using `HyperlinkedIdentityField`.
- Relationships use `HyperlinkedRelatedField`, instead of `PrimaryKeyRelatedField`.

### 2.8.1. Making sure our URL patterns are named

If we're going to have a hyperlinked API, we need to make sure we name our URL patterns.

The resulting `tasks/urls.py` file should look like this:

```py
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from tasks import views

# API endpoints
urlpatterns = format_suffix_patterns(
    [
        path("tasks/", views.TaskList.as_view(), name="task-list"),
        path("tasks/<int:pk>/", views.TaskDetail.as_view(), name="task-detail"),
        path("users/", views.UserList.as_view(), name="user-list"),
        path("users/<int:pk>/", views.UserDetail.as_view(), name="user-detail"),
    ]
)
```

### 2.8.2. Update serializers

Modify our serializers to extend `HyperlinkedModelSerializer` instead of the existing `ModelSerializer`.:

`tasks/serializers.py`

```py
# ...

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    # make the `owner` field read-only
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "completed",
            "important",
            "created_at",
            "updated_at",
            "owner",
        ]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    tasks = serializers.HyperlinkedRelatedField(
        many=True, view_name="task-detail", read_only=True
    )

    class Meta:
        model = User
        fields = ["url", "id", "username", "tasks"]
```

- The `url` field in the `UserSerializer` automatically points to `user-detail` url pattern.
- The `tasks` field in the `UserSerializer` points to `task-detail` url pattern for each task which is set by `view_name="task-detail"`

> [!NOTE]
> When you are manually instantiating these serializers inside your views (e.g., in `TaskDetail` or `TaskList`), you must pass `context={'request': request}` so the serializer knows how to build absolute URLs. For example, instead of:
>
> `serializer = TaskSerializer(task)` You must write:
>
> `serializer = TaskSerializer(task, context={"request": request})`
>
> If your view is a subclass of `GenericAPIView`, you may use the `get_serializer_context()` as a convenience method.

Now browse to the `users/` endpoints and notice the `url` field and the `tasks` field that includes task urls instead of ids.

### 2.8.3. Creating an endpoint for the root of our API

Right now we have endpoints for `'tasks'` and `'users'`, but we don't have a single entry point to our API. To create one, we'll use a regular function-based view and the `@api_view` decorator we introduced earlier. In your `tasks/views.py` add:

```py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "users": reverse("user-list", request=request, format=format),
            "tasks": reverse("task-list", request=request, format=format),
        }
    )
```

> [!IMPORTANT]
> Import `reverse` from `rest_framework.reverse`

Two things should be noticed here. First, we're using REST framework's `reverse` function in order to return fully-qualified URLs; second, URL patterns are identified by names in our `tasks/urls.py`.

Let's update our `tasks/urls.py` file to include the `api_root` view:

```py
# ...

urlpatterns = format_suffix_patterns(
    [
        path("", views.api_root, name="api-root"),
        # ...
    ]
)
```

Now browse to http://localhost:8000/ and you should see a list of available endpoints.

### 2.8.4. Adding pagination

The list views for `users` and `tasks` could end up returning quite a lot of instances, so really we'd like to make sure we paginate the results, and allow the API client to step through each of the individual pages.

We can change the default list style to use pagination, by modifying our `config/settings.py` file slightly. Add the following setting:

```py
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}
```

We could also customize the pagination style if we needed to, but in this case we'll just stick with the default.

## 2.9. ViewSets & Routers

`ViewSets` allows the developer to concentrate on modeling the state and interactions of the API, and leave the URL construction to be handled automatically, based on common conventions.

`ViewSet` classes are almost the same thing as `View` classes, except that they provide operations such as `retrieve`, or `update`, and not method handlers such as `get` or `put`.

A `ViewSet` class is only bound to a set of method handlers at the last moment, when it is instantiated into a set of views, typically by using a `Router` class which handles the complexities of defining the URLconf for you.

### 2.9.1. Refactoring to use ViewSets

First of all let's refactor our `UserList` and `UserDetail` classes into a single `UserViewSet` class in the `tasks/views.py`:

```py
from rest_framework import viewsets

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
```

Here we've used the `ReadOnlyModelViewSet` class to automatically provide the default 'read-only' operations. We're still setting the `queryset` and `serializer_class` attributes, but we no longer need to provide the same information to two separate classes.

Next we're going to replace the `TaskList` and `TaskDetail` view classes with a single `TaskViewSet` class.

```py
from rest_framework import permissions, viewsets
# ...

class TaskViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # authenticated users can create new tasks,
    # creator of a task can update or delete it
    # any user has read access
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # associate authenticated user with a new task
        serializer.save(owner=self.request.user)
```

This time we've used the `ModelViewSet` class in order to get the complete set of default read and write operations.

### 2.9.2. Binding ViewSets to URLs explicitly

The handler methods only get bound to the actions when we define the URLConf. To see what's going on under the hood let's first explicitly create a set of views from our ViewSets.

In the `tasks/urls.py` file we bind our ViewSet classes into a set of concrete views.

```py
# imports

task_list = views.TaskViewSet.as_view({"get": "list", "post": "create"})
task_detail = views.TaskViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)
user_list = views.UserViewSet.as_view({"get": "list"})
user_detail = views.UserViewSet.as_view({"get": "retrieve"})
```

Notice how we're creating multiple views from each `ViewSet` class, by binding the `HTTP` methods to the required action for each view.

Now we can register the views with the URLconf as usual.

`tasks/urls.py`

```py
# ...

urlpatterns = format_suffix_patterns(
    [
        path("", views.api_root, name="api-root"),
        path("tasks/", task_list, name="task-list"),
        path("tasks/<int:pk>/", task_detail, name="task-detail"),
        path("users/", user_list, name="user-list"),
        path("users/<int:pk>/", user_detail, name="user-detail"),
    ]
)
```

### 2.9.3. Using Routers

Because we're using `ViewSet` classes rather than `View` classes, we actually don't need to design the URLconf ourselves. The conventions for wiring up resources into views and urls can be handled automatically, using a `Router` class. All we need to do is register the appropriate view sets with a router, and let it do the rest.

Here's our final `tasks/urls.py` file.

```py
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from tasks import views

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r"tasks", views.TaskViewSet, basename="task")
router.register(r"users", views.UserViewSet, basename="user")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path("", include(router.urls)),
]
```

Registering the `ViewSets` with the `router` is similar to providing a `urlpattern`. We include two arguments - the URL prefix for the views, and the view set itself.

The `DefaultRouter` class we're using also automatically creates the API root view for us, so we deleted the `api_root` function from our views module.

Run the development server and check that everything works as expected.

### 2.9.4. Trade-offs between views vs ViewSets

Using `ViewSets` helps ensure that URL conventions will be consistent across your API, minimizes the amount of code you need to write, and allows you to concentrate on the interactions and representations your API provides rather than the specifics of the URL conf.

That doesn't mean it's always the right approach to take. There's a similar set of trade-offs to consider as when using class-based views instead of function-based views. Using ViewSets is less explicit than building your API views individually.

[⬆️ Return to Table of contents](#table-of-contents)

## 2.10. Documenting our API

Outline of our Plan:

```
                   ┌──────────────────┐
                   │   DRF API code   │
                   │                  │
                   │ serializers      │
                   │ views/viewsets   │
                   │ routers/URLs     │
                   └────────┬─────────┘
                            │
                            ▼
                   ┌──────────────────┐
                   │ drf-spectacular  │
                   │                  │
                   │ OpenAPI 3 schema │
                   └────────┬─────────┘
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
       ┌──────────────┐            ┌──────────────┐
       │ Swagger UI   │            │    ReDoc     │
       │              │            │              │
       │ interactive  │            │ documentation│
       │ API explorer │            │ reference    │
       └──────────────┘            └──────────────┘
```

### 2.10.1. `drf-spectacular`

REST framework recommends using third-party packages, like `drf-spectacular`, for generating and presenting OpenAPI 3 schemas.

`drf-spectacular` library inpects your DRF application, extract as much schema information from DRF as possible. There is explicit support for `swagger-codegen`, `SwaggerUI` and `Redoc`, i18n, versioning, authentication, polymorphism (dynamic requests and responses), query/path/header parameters, documentation and more.

Let's install [drf-spectacular](https://github.com/tfranzel/drf-spectacular/#installation) using `uv` tool:

```bash
uv add drf-spectacular
```

We don't need to install `Swagger UI` or `ReDoc` as separate Python packages. `drf-spectacular` provides the integration for both interfaces.

Let's add `drf_spectacular` to `INSTALLED_APPS` in `config/settings.py`:

```py
INSTALLED_APPS = [
    # ALL YOUR APPS
    'drf_spectacular',
]
```

And finally register our spectacular AutoSchema with DRF.

`config/settings.py`

```py
REST_FRAMEWORK = {
    # YOUR OTHER SETTINGS
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
```

`AutoSchema` is the mechanism that allows `drf-spectacular` to inspect your DRF views and serializers and turn that information into an OpenAPI schema.

### 2.10.2. Add the OpenAPI schema endpoint

Now we need an endpoint that actually serves the OpenAPI schema.

Open `config/urls.py` and add the import first:

```py
from drf_spectacular.views import SpectacularAPIView
```

Then add this to the existing urlpatterns:

```py
urlpatterns = [
    # Other patterns
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
]

# ...
```

Now start Django:

```bash
uv run manage.py runserver
```

Now visiting: http://127.0.0.1:8000/api/schema/

is supposed to return/download the machine-readable OpenAPI schema/document (usually a yaml file) of the API. For example:

```yaml
paths:
  /tasks/:
    get:
      # ...
    post:
      # ...

  /tasks/{id}/:
    get:
      # ...
    put:
      # ...
    patch:
      # ...
    delete:
      # ...
```

That's OpenAPI schema.

### 2.10.3. Add Swagger UI

Swagger UI reads that OpenAPI schema and creates the nice interactive documentation page.

Open `config/urls.py` and import `SpectacularSwaggerView`:

```py
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
```

Then add this to the existing urlpatterns:

```py
urlpatterns = [
    # Other patterns
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # API Documentation
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]

# ...
```

Now visit: http://localhost:8000/api/docs/

We should get Swagger UI documentation page.

You should see your API operations automatically generated from your existing code:

```
tasks
GET /tasks/
POST /tasks/

GET /tasks/{id}/
PUT /tasks/{id}/
PATCH /tasks/{id}/
DELETE /tasks/{id}/

USER
GET /users/
GET /users/{id}/
```

Your router is already defining those endpoints through `TaskViewSet` and `UserViewSet`.

### Give the API some proper identity

Right now, the generated documentation will work, but it won't yet feel like a polished public API.

We'll improve that next.

Add a `SPECTACULAR_SETTINGS` section to `config/settings.py`:

```py
SPECTACULAR_SETTINGS = {
    "TITLE": "Oasis Task Manager API",
    "DESCRIPTION": "A RESTful API for managing users and tasks.",
    "VERSION": "1.0.0",
}
```

Now reload Swagger UI.

You'll have:

```
Oasis Task Manager API
```

rather than an unnamed generic schema.

### 2.10.4. ReDoc?

ReDoc is another presentation layer for the same OpenAPI schema.

So you could have:

```
/openapi/schema/    → OpenAPI JSON/YAML
/docs/              → Swagger UI
/redoc/             → ReDoc
```

All three are ultimately based on the same API schema.

We don't need both Swagger UI and ReDoc for a small project.

For this project, we'd initially use Swagger UI because it is particularly useful while we're developing and testing the API.

Later, if we want to demonstrate a more polished `documentation/reference` site, we can add ReDoc too.

## 2.11. Next steps

- Dockerize your API
