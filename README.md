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
      - [2.7.3.3. Url patterns for user views](#2733-url-patterns-for-user-views)
    - [2.7.4. Adding required permissions to user views](#274-adding-required-permissions-to-user-views)
    - [2.7.5. Adding login to the Browsable API](#275-adding-login-to-the-browsable-api)
    - [2.7.6. Restricting access to users](#276-restricting-access-to-users)
    - [2.7.7. Associating tasks with users](#277-associating-tasks-with-users)
    - [2.7.8. Updating our `TaskSerializer`](#278-updating-our-taskserializer)
    - [2.7.9. Adding required permissions to task views](#279-adding-required-permissions-to-task-views)
    - [2.7.10. Object level permissions to tasks](#2710-object-level-permissions-to-tasks)
    - [2.7.11. Restricting Task lists](#2711-restricting-task-lists)
    - [2.7.12. Authenticating requests](#2712-authenticating-requests)
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
    - [2.10.4. Give the API some proper identity](#2104-give-the-api-some-proper-identity)
    - [2.10.5. Document the actual API properly](#2105-document-the-actual-api-properly)
      - [2.10.5.1. Edit the ViewSet docstrings](#21051-edit-the-viewset-docstrings)
      - [2.10.5.2. Customize the `TaskViewSet` documentation](#21052-customize-the-taskviewset-documentation)
      - [2.10.5.3. Customize the `UserRegistration` documentation](#21053-customize-the-userregistration-documentation)
      - [2.10.5.4. Customize the `UserViewSet` documentation](#21054-customize-the-userviewset-documentation)
    - [2.10.6. ReDoc](#2106-redoc)
  - [2.11. Containerizing our API with Docker (Optional)](#211-containerizing-our-api-with-docker-optional)
    - [2.11.1. Prerequisites](#2111-prerequisites)
    - [2.11.2. Start with a simple Dockerfile](#2112-start-with-a-simple-dockerfile)
    - [2.11.3. Update the `.env` file](#2113-update-the-env-file)
    - [2.11.4. Create a simple docker compose](#2114-create-a-simple-docker-compose)
    - [2.11.5. Build image and run the containers](#2115-build-image-and-run-the-containers)
    - [2.11.6. Test postgreSQL](#2116-test-postgresql)
    - [2.11.7. Run migrations and create a superuser](#2117-run-migrations-and-create-a-superuser)
    - [2.11.8. Persist data through volumes](#2118-persist-data-through-volumes)
    - [2.11.9. Improve Dockerfile using mounts to `uv sync`](#2119-improve-dockerfile-using-mounts-to-uv-sync)
    - [2.11.10. Create multi-stage Dockerfile](#21110-create-multi-stage-dockerfile)
  - [2.12. Organising tasks with folders](#212-organising-tasks-with-folders)
    - [2.12.1. Creating the `Folder` model](#2121-creating-the-folder-model)
    - [2.12.2. Creating `FolderSerializer` and updating others](#2122-creating-folderserializer-and-updating-others)
    - [2.12.3. Creating `FolderViewSet`, permissions and URL routing](#2123-creating-folderviewset-permissions-and-url-routing)
    - [2.12.4. Filtering tasks by folder](#2124-filtering-tasks-by-folder)
      - [2.12.4.1. Install and register `django-filter`](#21241-install-and-register-django-filter)
      - [2.12.4.2. Creating a TaskFilter](#21242-creating-a-taskfilter)
      - [2.12.4.3. Wiring it into `TaskViewSet`](#21243-wiring-it-into-taskviewset)
      - [2.12.4.4. Edit documentation for FolderViewSet](#21244-edit-documentation-for-folderviewset)
  - [2.13. Production-ready setup with Docker, Gunicorn, and Nginx](#213-production-ready-setup-with-docker-gunicorn-and-nginx)
    - [2.13.1. What this local setup verifies](#2131-what-this-local-setup-verifies)
    - [2.13.2. Prerequisites](#2132-prerequisites)
    - [2.13.3. Prepare Django for static files and a local host](#2133-prepare-django-for-static-files-and-a-local-host)
    - [2.13.4. Run Django with Gunicorn](#2134-run-django-with-gunicorn)
    - [2.13.5. Add a local production-style Compose file](#2135-add-a-local-production-style-compose-file)
    - [2.13.6. Configure local Nginx](#2136-configure-local-nginx)
    - [2.13.7. Build and test the stack](#2137-build-and-test-the-stack)
    - [2.13.8. Restart and shutdown checks](#2138-restart-and-shutdown-checks)
  - [2.14. Initialize the React frontend](#214-initialize-the-react-frontend)

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

When that's all done we'll need to update our database tables. Normally we'd create a database migration in order to do that, but for this development project, let's just recreate the database and migrations.

First, drop and recreate the database using the database credentials from the `.env` file:

```bash
dropdb -U <db_user> <db_name>
createdb -U <db_user> <db_name>
```

Then recreate the migrations and database tables:

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

Notice that registration is deliberately separate from `/users/`. `/users/register/` represents the action of creating a new account, while `/users/` represents administrative access to existing users.

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


class UserList(generics.ListCreateAPIView):
    """
    List all users (GET), or create a new user (POST).
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve (GET), update (PUT), or delete (DELETE) a single user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
```

[⬆️ Return to Table of contents](#table-of-contents)

#### 2.7.3.3. Url patterns for user views

Finally we need to add those views into the API, by referencing them from the URLconf. Add the following to the patterns in `tasks/urls.py`.

```py
path("users/register/", views.UserRegistration.as_view()),
path("users/me/", views.UserMe.as_view()),
path("users/", views.UserList.as_view()),
path("users/<int:pk>/", views.UserDetail.as_view()),
```

Open the browsable API in the browser and verify that the new endpoints return the expected user representations.

### 2.7.4. Adding required permissions to user views

We want to make sure that users can only access user endpoints when they are authenticated.

REST framework includes a number of permission classes to restrict who can access a given view. For this stage, we'll use IsAuthenticated, which requires users to be authenticated before they can access the view.

1. First add the following import in the `tasks/views.py` module

   ```py
   from rest_framework import permissions
   ```

2. Then, add the permission classes to the `UserMe`, `UserList` and `UserDetail` views.

   ```py
    class UserMe(generics.RetrieveUpdateAPIView):
        # authenticated users can read or update their own profile
        permission_classes = [permissions.IsAuthenticated]

    class UserList(generics.ListCreateAPIView):
        # authenticated users can read users
        permission_classes = [permissions.IsAuthenticated]


    class UserDetail(generics.RetrieveUpdateDestroyAPIView):
        permission_classes = [permissions.IsAuthenticated]
   ```

We don't add a permission class to `UserRegistration` because unauthenticated users must be able to create an account.

[⬆️ Return to Table of contents](#table-of-contents)

### 2.7.5. Adding login to the Browsable API

At this stage, we'll include the login and logout views for the browsable API to allow users to log in and log out easily.

At the end of our project-level `config/urls.py` file, add a pattern to include the login and logout views for the browsable API.

```py
urlpatterns += [
    # include the login and logout views for the browsable API
    path("api-auth/", include("rest_framework.urls")),
]
```

The `'api-auth/'` part of pattern can actually be whatever URL you want to use.

Now, if you open the browser again and refresh the page, you'll see a `'Login'` link in the top right of the page which redirects to the `/api-auth/login/` page.

Log in as one of the users you created earlier. You should now be able to perform the actions allowed by that user's permissions.

[⬆️ Return to Table of contents](#table-of-contents)

### 2.7.6. Restricting access to users

At the moment, any authenticated user can access the user list and any individual user.

We want these administrative endpoints to be available only to superusers.

To enforce this, we'll create a custom permission class.

In the `tasks` app, create a new file, `permissions.py` with following content:

`tasks/permissions.py`

```py
from rest_framework import permissions

class IsSuperuser(permissions.BasePermission):
    """
    Custom permission that allows only superusers to access a view.
    """

    def has_permission(self, request, view):
        return request.user.is_superuser
```

The `has_permission()` instead of `has_object_permission()` method is used here because we want to restrict access to the entire endpoint, rather than check an individual object.

Now add that custom permission into `tasks/views.py`:

```py
from tasks.permissions import IsSuperuser

class UserList(generics.ListCreateAPIView):
    # ...
    permission_classes = [permissions.IsAuthenticated, IsSuperuser]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    # ...
    permission_classes = [permissions.IsAuthenticated, IsSuperuser]
```

Now:

- Normal authenticated users can access `/users/me/`.
- Normal authenticated users cannot access `/users/` or `/users/<id>/`.
- Superusers can access `/users/` and `/users/<id>/`.

[⬆️ Return to Table of contents](#table-of-contents)

### 2.7.7. Associating tasks with users

Right now, if we created a task, there'd be no way of associating the user that created the task with the task instance.

The user isn't sent as part of the serialized representation.

The way we deal with that is by overriding a `.perform_create()` method on our task views, that allows us to modify how the instance save is managed, and handle any information that is implicit in the incoming request or requested URL.

On the `TaskList` view class, add the following method:

`tasks/views.py`

```py
def perform_create(self, serializer):
    # associate authenticated user with a new task
    serializer.save(owner=self.request.user)
```

The `create()` method will now save the authenticated user as the task's owner.

> [!NOTE]
> You might think the `Task` model already has an `owner` field. So why do we need to associate the task with a user again?
>
> Yes, every task has an `owner` field. But who sets its value?
>
> This is why the view saves the authenticated (logged in) user as the `owner`. Here `self.request.user` is the authenticated user.

[⬆️ Return to Table of contents](#table-of-contents)

### 2.7.8. Updating our `TaskSerializer`

Now that tasks are associated with the user that created them, let's update our `TaskSerializer` to reflect that.

1. Add the `owner` field as a read-only field to the `TaskSerializer` definition in `tasks/serializers.py`:

   ```py
   owner = serializers.ReadOnlyField(source="owner.username")
   ```

2. Make sure you also add `'owner'`, to the list of fields in the inner `Meta` class.

The `source` argument controls which attribute is used to populate a field (and can point at any attribute on the serialized instance).

The field we've added is the untyped `ReadOnlyField` class, in contrast to the other typed fields, such as `CharField`, `BooleanField` etc... The untyped `ReadOnlyField` is always read-only, and will be used for serialized representations, but will not be used for updating model instances when they are deserialized. We could have also used `CharField(read_only=True)` here.

[⬆️ Return to Table of contents](#table-of-contents)

### 2.7.9. Adding required permissions to task views

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

### 2.7.10. Object level permissions to tasks

At the moment, any authenticated user can access tasks, including tasks created by other users.

We want to make our API creator-related:

- A normal authenticated user can read, update and delete only their own tasks.
- A superuser can read, update and delete all tasks.
- Users must be authenticated to access the tasks and users.

To enforce ownership at the object level, we'll create a new custom permission class named `IsOwnerOrAdmin` in the `tasks/permissions.py` module.

```py
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

### 2.7.11. Restricting Task lists

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

[⬆️ Return to Table of contents](#table-of-contents)

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

In this case we'd like to use a hyperlinked style between entities. In order to do so, we'll modify some of our serializers to extend `HyperlinkedModelSerializer` instead of the existing `ModelSerializer`.

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
        path("users/register/", views.UserRegistration.as_view(), name="user-register"),
        path("users/me/", views.UserMe.as_view(), name="user-me"),
        path("users/", views.UserList.as_view(), name="user-list"),
        path("users/<int:pk>/", views.UserDetail.as_view(), name="user-detail"),
    ]
)
```

### 2.8.2. Update serializers

Modify some of our serializers to extend `HyperlinkedModelSerializer` instead of the existing `ModelSerializer`.:

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

> Keep the `UserRegistrationSerializer` the same as before.

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

[⬆️ Return to Table of contents](#table-of-contents)

## 2.9. ViewSets & Routers

`ViewSets` allows the developer to concentrate on modeling the state and interactions of the API, and leave the URL construction to be handled automatically, based on common conventions.

`ViewSet` classes are almost the same thing as `View` classes, except that they provide operations such as `retrieve`, or `update`, and not method handlers such as `get` or `put`.

A `ViewSet` class is only bound to a set of method handlers at the last moment, when it is instantiated into a set of views, typically by using a `Router` class which handles the complexities of defining the URLconf for you.

### 2.9.1. Refactoring to use ViewSets

First of all let's refactor our `UserMe`, `UserList` and `UserDetail` into a single `UserViewSet` ViewSet class but keep the existing `UserRegistration` view to use generic view class. In `tasks/views.py`:

```py
from rest_framework import viewsets

class UserRegistration(generics.CreateAPIView):
    """
    Create a new user account.
    """

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user management.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "me":
            return [permissions.IsAuthenticated()]
        return [
            permissions.IsAuthenticated(),
            IsSuperuser(),
        ]

    @action(detail=False, methods=["get", "put", "patch"])
    def me(self, request):
        """
        Retrieve or update the currently authenticated user.
        """

        if request.method == "GET":
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=request.method == "PATCH",
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

```

Here we've used the `ModelViewSet` class to automatically provide the `list`, `create`, `retrieve`, `update` and `destroy` operations. We're still setting the `queryset` and `serializer_class` attributes, but we no longer need to provide the same information to two separate classes.

Next we're going to replace the `TaskList` and `TaskDetail` view classes with a single `TaskViewSet` class.

```py
from rest_framework import permissions, viewsets
# ...

class TaskViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`, `update`, `partial_update` and `destroy` actions.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # authenticated users can create new tasks,
    # creator of a task can update or delete it
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def perform_create(self, serializer):
        # associate authenticated user with a new task
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Task.objects.all()
        return Task.objects.filter(owner=self.request.user)
```

### 2.9.2. Binding ViewSets to URLs explicitly

The handler methods only get bound to the actions when we define the URLConf. To see what's going on under the hood let's first explicitly create a set of views from our ViewSets.

In the `tasks/urls.py` file we bind our ViewSet classes into a set of concrete views.

```py
# imports

task_list = views.TaskViewSet.as_view({"get": "list", "post": "create"})
task_detail = views.TaskViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)
user_me = views.UserViewSet.as_view({"get": "me", "put": "me", "patch": "me"})
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
        path("users/register/", views.UserRegistration.as_view(), name="user-registration"),
        path("users/me/", user_me, name="user-me"),
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
    path("users/register/", views.UserRegistration.as_view(), name="user-registration"),
]

```

Registering the `ViewSets` with the `router` is similar to providing a `urlpattern`. We include two arguments - the URL prefix for the views, and the view set itself.

The `DefaultRouter` class we're using also automatically creates the API root view for us, so we can remove the `api_root` function from our views module.

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

[⬆️ Return to Table of contents](#table-of-contents)

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

[⬆️ Return to Table of contents](#table-of-contents)

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

[⬆️ Return to Table of contents](#table-of-contents)

### 2.10.4. Give the API some proper identity

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

### 2.10.5. Document the actual API properly

Now we'll look through endpoint by endpoint.

#### 2.10.5.1. Edit the ViewSet docstrings

The docstrings related to a ViewSet are shown in every endpoint related to that ViewSet. So, they should fit for all related endpoints.

Open `tasks/views.py` and edit the docstrings for `TaskViewSet` and `UserViewSet`:

```py
class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for creating and managing tasks.

    Anyone can view tasks. Authenticated users can create tasks,
    while only the task owner can update or delete them.
    """
    # ...

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only ViewSet for accessing users.
    """

    # ...
```

[⬆️ Return to Table of contents](#table-of-contents)

#### 2.10.5.2. Customize the `TaskViewSet` documentation

Add a `@extend_schema_view` decorator to `TaskViewSet`:

`views/tasks.py`

```py
@extend_schema_view(
    list=extend_schema(
        summary="List all tasks",
        description="Return a paginated list of all tasks.",
        responses={
            200: OpenApiResponse(
                response=TaskSerializer,
                description="A paginated list of tasks.",
            ),
        },
    ),
    create=extend_schema(
        summary="Create a task",
        description="Create a new task. Authentication is required. "
        "The authenticated user will be set as the owner of the task.",
        request=TaskSerializer,
        responses={
            201: OpenApiResponse(
                response=TaskSerializer,
                description="The task was successfully created.",
            ),
            400: OpenApiResponse(
                description="The request data was invalid.",
            ),
        },
        examples=[
            OpenApiExample(
                "Create task",
                value={
                    "title": "Learn API documentation",
                    "completed": False,
                    "important": True,
                },
                request_only=True,
            ),
            OpenApiExample(
                "Created task",
                value={
                    "id": 0,
                    "title": "Learn API documentation",
                    "completed": False,
                    "important": True,
                    "created_at": "2026-09-02T00:15:07.857Z",
                    "updated_at": "2026-09-02T00:15:07.857Z",
                    "owner": "john",
                },
                response_only=True,
            ),
        ],
    ),
    retrieve=extend_schema(
        summary="Retrieve a task",
        description="Return the details of a single task.",
        responses={
            200: OpenApiResponse(
                response=TaskSerializer,
                description="The requested task.",
            ),
            404: OpenApiResponse(
                description="The requested task does not exist.",
            ),
        },
    ),
    update=extend_schema(
        summary="Update a task",
        description=(
            "Replace all writable fields of an existing task. "
            "Only the task owner can update the task."
        ),
        request=TaskSerializer,
        responses={
            200: OpenApiResponse(
                response=TaskSerializer,
                description="The task was successfully updated.",
            ),
            400: OpenApiResponse(
                description="The request data is invalid.",
            ),
            403: OpenApiResponse(
                description="The authenticated user is not the task owner.",
            ),
            404: OpenApiResponse(
                description="The requested task does not exist.",
            ),
        },
    ),
    partial_update=extend_schema(
        summary="Partially update a task",
        description=(
            "Update one or more fields of an existing task. "
            "Only the task owner can update the task."
        ),
        request=TaskSerializer,
        responses={
            200: OpenApiResponse(
                response=TaskSerializer,
                description="The task was successfully updated.",
            ),
            400: OpenApiResponse(
                description="The request data is invalid.",
            ),
            403: OpenApiResponse(
                description="The authenticated user is not the task owner.",
            ),
            404: OpenApiResponse(
                description="The requested task does not exist.",
            ),
        },
    ),
    destroy=extend_schema(
        summary="Delete a task",
        description="Delete a task. Only the task owner can delete it.",
        responses={
            204: OpenApiResponse(
                response=TaskSerializer,
                description="The task was successfully deleted.",
            ),
            403: OpenApiResponse(
                description="The authenticated user is not the task owner.",
            ),
            404: OpenApiResponse(
                description="The requested task does not exist.",
            ),
        },
    ),
)
class TaskViewSet(viewsets.ModelViewSet):
    # ...
```

> Only modify things you really want to change in the default documentation view.

Now reload Swagger UI and notice the changes in action.

[⬆️ Return to Table of contents](#table-of-contents)

#### 2.10.5.3. Customize the `UserRegistration` documentation

Because `UserRegistration` is a generic api view, we need to add the `@extend_schema` decorator instead of `@extend_schema_view` to it:

`views/tasks.py`

```py
@extend_schema(
    summary="Register a new user",
    description="Create a new user account.",
    request=UserRegistrationSerializer,
    responses={
        201: OpenApiResponse(
            response=UserRegistrationSerializer,
            description="The user account was successfully created.",
        ),
        400: OpenApiResponse(
            description="The request data was invalid.",
        ),
    },
)
class UserRegistration(generics.CreateAPIView):
    # ...
```

#### 2.10.5.4. Customize the `UserViewSet` documentation

Add a `@extend_schema_view` decorator to `UserViewSet`:

`views/tasks.py`

```py
@extend_schema_view(
    list=extend_schema(
        summary="List all users",
        description="Return a paginated list of users.",
        responses={
            200: OpenApiResponse(
                response=UserSerializer,
                description="A paginated list of users.",
            ),
        },
    ),
    create=extend_schema(
        summary="Create a user",
        description="Create a new user. Only a superuser can create a user.",
        request=UserSerializer,
        responses={
            201: OpenApiResponse(
                response=UserSerializer,
                description="The user was successfully created.",
            ),
            400: OpenApiResponse(
                description="The request data is invalid.",
            ),
            403: OpenApiResponse(
                description="The authenticated user is not a superuser.",
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve a user",
        description="Return details of a single user and their tasks.",
        responses={
            200: OpenApiResponse(
                response=UserSerializer,
                description="The requested user and their tasks.",
            ),
            404: OpenApiResponse(
                description="User not found.",
            ),
        },
    ),
)
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    # ...
```

We can also use `extend_schema` to customize the `me` endpoint:

`views/tasks.py`

```py
class UserViewSet(viewsets.ModelViewSet):
    # ...
    # Add the decorator before the `me` method
    @extend_schema(
        summary="Retrieve or update the current user",
        description="Retrieve or update the currently authenticated user's profile.",
        request=UserSerializer,
        responses={
            200: OpenApiResponse(
                response=UserSerializer,
                description="The current user's profile.",
            ),
            400: OpenApiResponse(
                description="The request data was invalid.",
            ),
        },
    )
    @action(detail=False, methods=["get", "put", "patch"])
    def me(self, request):
        # ...
```

Again, reload Swagger UI and notice the changes in action.

### 2.10.6. ReDoc

ReDoc is the final presentation layer for the same OpenAPI schema.

We just need to add the urlpattern for ReDoc:

`config/urls.py`

```py
from drf_spectacular.views import SpectacularRedocView

urlpatterns = [
    # ...
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
```

Now visit: http://localhost:8000/api/redoc/ to see the final presentation layer.

That's all about documenting our API.

[⬆️ Return to Table of contents](#table-of-contents)

## 2.11. Containerizing our API with Docker (Optional)

At this stage, let's run our Oasis Task Manager api and PostgreSQL with Docker. It follows a two-stage approach:

- _Development:_ Django’s development server plus Docker Compose Watch, which syncs code changes into the container.

- _Production:_ Gunicorn running on a smaller Docker Hardened Image (DHI).

### 2.11.1. Prerequisites

- Install `Docker Desktop`, start it, and verify the installation:

  ```bash
  docker --version
  docker compose version
  ```

This project already uses:

- `uv` for dependency management
- Django REST Framework
- PostgreSQL with `psycopg`
- `django-environ` and `DATABASE_URL`

### 2.11.2. Start with a simple Dockerfile

We'll first create a simple one-stage image from a base python imgae from `Docker Hardened Images` registry.

1. Open/run docker desktop

2. Sign in to the `DHI` registry to use Docker Hardened Images (default registry is `Docker hub`):

   ```bash
   docker login dhi.io
   ```

3. Create a `.dockerignore` file to exclude local artifacts from the build context:

   `.dockerignore`

   ```
   .venv/
    __pycache__/
    *.py[cod]
    .git/
    .env
    db.sqlite3
    staticfiles/
    media/
   ```

4. Create a `Dockerfile` in the project root with the following content:

   ```dockerfile
   # Build my image from a base python image from DHI registry
   # `-dev` image includes tools needed to install packages.
   FROM dhi.io/python:3.14-alpine3.24-dev

   # Prevent Python from writing `.pyc` files to disk.
   ENV PYTHONDONTWRITEBYTECODE=1
   # Prevent Python from buffering stdout/stderr so logs appear immediately.
   ENV PYTHONUNBUFFERED=1

   # Install uv using python image's pip;
   # `--quiet` (optional) reduces pip's output;
   # `--root-user-action=ignore` (optional) prevents pip from warning about the root user
   RUN pip install --quiet --root-user-action=ignore uv

   # Set `/app` as the working directory inside the container
   WORKDIR /app

   # Copy the dependencies files to the working directory
   COPY pyproject.toml uv.lock ./

   # `uv sync` creates `.venv` and installs the dependencies in it.
   # `--frozen` tells uv to use the existing `uv.lock` file;
   # `--no-install-project` tells uv not to install the project
   RUN uv sync --frozen --no-install-project

   # Copy the contents into container at `/app`
   COPY . .

   # Tell python to use `.venv`
   ENV PATH="/app/.venv/bin:$PATH"

   # Expose port 8000: just a metadata (optional)
   EXPOSE 8000

   # Base command to run when the container starts
   # Base command to run when the container starts
   CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
   ```

5. Now build the image named `oasis-task-manager` by running the following command in the project root directory:

   ```bash
   docker build -t oasis-task-manager .
   ```

Don't run the container yet. We'll also need to run our PostgreSQL database container. We'll use `docker compose` to run the containers.

### 2.11.3. Update the `.env` file

Add the following environment variables to the `.env` file for our database:

```
POSTGRES_DB=<db_name>
POSTGRES_USER=<db_user>
POSTGRES_PASSWORD=<db_password>
```

We alread have `<db_host>` and `<db_port>` in `DATABASE_URL` in `.env` file.

Replace `<db_name>`, `<db_user>` and `<db_password>` with appropriate values. We'll pass these values to the containers through Docker Compose.

> [!IMPORTANT]
> The `<db_host>` must match the service name of the PostgreSQL container defined in `compose.yaml`. So, update the `<db_host>` to `db` in the `.env` file.

### 2.11.4. Create a simple docker compose

Create a `compose.yaml` file in project root directory with the following content to start the drf app and db containers:

```yaml
services:
  web:
    # Build the image using Dockerfile in the current directory
    build: .
    # (optional) name the image
    image: oasis-task-manager
    env_file:
      - .env
    ports:
      # equivalent to `docker run -p 8000:8000`
      - "8000:8000"
    # Wait for the database to pass its healthcheck and
    # start the `db` service before starting the `web` service.
    depends_on:
      db:
        condition: service_healthy

  db:
    # Run PostgreSQL container using an image
    image: dhi.io/postgres:18
    # Automatically restart the db container if it stops.
    restart: always
    # Left-side names are not arbitrary; Right-side name are defined in `.env`
    # These are PostgreSQL image environment variables.
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    # Expose the port only to other services on the Compose network,
    # not to the host machine.
    expose:
      - 5432
    # Only report healthy once PostgreSQL is ready to accept connections,
    # so the web service doesn't start before the database is available.
    healthcheck:
      test:
        ["CMD", "pg_isready", "-U", "${POSTGRES_USER}", "-d", "${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5
```

### 2.11.5. Build image and run the containers

From the project directory, run:

```bash
docker compose up --build
```

Make sure both the `web` and `db` containers are running.

### 2.11.6. Test postgreSQL

Run the `psql` shell from the `db` container:

```bash
docker compose exec db psql -U <db_user> -l
```

We should see our database name.

Again run:

```bash
docker compose exec db psql -U <db_user> <db_name>
```

It should connect to the database.

> [!TIP]
> You can also access the `exec` shell from your Docker Desktop by navigating to the `db` container.

### 2.11.7. Run migrations and create a superuser

In another terminal window, run migrations and create a superuser in the web container:

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

Open the browser and navigate to http://localhost:8000. You should see our same api application running but this time from the containerized application.

Press `ctrl+c` to stop the application.

### 2.11.8. Persist data through volumes

Currently, PostgreSQL stores its data inside the `db` container. If you delete the container, the database data will be lost.

To avoid this, we'll use a Docker volume to store PostgreSQL's data independently of the container.

Update the `compose.yaml` file as follows:

```yaml
services:
  web:
    # ...

  db:
    #...
    restart: always
    volumes:
      # Persist database data across container restarts.
      - db-data:/var/lib/postgresql
    environment:
      # ...

volumes:
  db-data:
```

The `db-data` volume is now managed by Docker and persists even when the `db` container is deleted and recreated.

You can now verify persistence by creating some database data (you can use the browsable api to create some tasks attached to a user), deleting the `db` container, and recreating it.

First, press `ctrl+c` to stop the application if it's running.

Then, run:

```bash

docker compose down
docker compose up --build
```

The database data is now stored in the `db-data` volume rather than inside the container.

> [!NOTE]
> To remove the volume and its data, you would need to explicitly use `-v` flag with `docker compose down`:
>
> ```bash
> docker compose down -v
> ```

### 2.11.9. Improve Dockerfile using mounts to `uv sync`

We'll update the `Dockerfile` with a few improvements to how dependencies are installed::

- Add `UV_LINK_MODE=copy` so `uv` copies packages instead of creating links between the cache and the virtual environment.
- Use a `cache` mount so `uv` can reuse downloaded packages between builds.
- Instead of permanently copying `pyproject.toml` and `uv.lock` into an image layer, make them temporarily available to `uv sync` using `bind` mounts.
- Add `# syntax=docker/dockerfile:1` to the top of the Dockerfile. This tells Docker to use the stable version `1` of the Dockerfile syntax, which supports features such as `RUN --mount`.

So, our resulting `Dockerfile` is:

```dockerfile
# syntax=docker/dockerfile:1

FROM dhi.io/python:3.14-alpine3.24-dev

# ... existing instructions ...

RUN pip install --quiet --root-user-action=ignore uv

# Use copy mode since the cache and build filesystem are on different volumes.
ENV UV_LINK_MODE=copy

WORKDIR /app

# Install dependencies into a `.venv` using `cache` and `bind` mounts
# so neither uv not the lock files need to be copied into the image.
# `uv sync` creates `.venv` and installs the dependencies in it.
# `--frozen` tells uv to use the existing `uv.lock` file;
# `--no-install-project` tells uv not to install the project
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# ... existing instructions ...
```

Run `docker compose down` and then `docker compose up --build` to rebuild the image.

### 2.11.10. Create multi-stage Dockerfile

Now, let's introduce a simple two-stage Dockerfile.

Our current Dockerfile does everything in one image

The problem is that the `-dev` image contains tools needed to build the application, but we don't need those tools when we're merely running the application. So, we split our Dockerfile into two stages:

```
BUILD STAGE
────────────────────────
DHI Python -dev
install uv (create .venv)
install dependencies
       └────┐
            ▼
RUNTIME STAGE
────────────────────────
DHI Python runtime
copy .venv
copy application source
run dev server
```

This is the fundamental idea of a multi-stage build.

So, here is our two-stage Dockerfile:

```dockerfile
# syntax=docker/dockerfile:1

###### BUILD STAGE ######

# Build my image from a base python image from DHI registry
# `-dev` image includes tools needed to install packages.
FROM dhi.io/python:3.14-alpine3.24-dev AS builder

# Prevent Python from writing `.pyc` files to disk.
ENV PYTHONDONTWRITEBYTECODE=1
# Prevent Python from buffering stdout/stderr so logs appear immediately.
ENV PYTHONUNBUFFERED=1

# Install uv using python image's pip;
# `--quiet` (optional) reduces pip's output;
# `--root-user-action=ignore` (optional) prevents pip from warning about the root user
RUN pip install --quiet --root-user-action=ignore uv

# Use copy mode since the cache and build filesystem are on different volumes.
ENV UV_LINK_MODE=copy

# Set `/app` as the working directory inside the container
WORKDIR /app

# Install dependencies into a `.venv` using `cache` and `bind` mounts
# so neither uv not the lock files need to be copied into the image.
# `uv sync` creates `.venv` and installs the dependencies in it.
# `--frozen` tells uv to use the existing `uv.lock` file;
# `--no-install-project` tells uv not to install the project
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project


###### RUNTIME STAGE ######

# # Use minimal DHI image with no shell or package manager
# already runs as the nonroot user.
FROM dhi.io/python:3.14-alpine3.24

# Prevent Python from writing `.pyc` files to disk.
ENV PYTHONDONTWRITEBYTECODE=1
# Prevent Python from buffering stdout/stderr so logs appear immediately.
ENV PYTHONUNBUFFERED=1
# Make executables from the copied virtual environment available on PATH.
ENV PATH="/app/.venv/bin:$PATH"

# Set `/app` as the working directory inside the container
WORKDIR /app

# Copy the pre-built virtual environment and application source code.
COPY --from=builder /app/.venv /app/.venv

# Copy the contents into container at `/app`
COPY . .

# Expose port 8000: just a metadata (optional)
EXPOSE 8000

# Base command to run when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

Run `docker compose down` and `docker compose up --build` to rebuild the image and on browser visit `http://localhost:8000/` to check that everything is working fine.

[⬆️ Return to Table of contents](#table-of-contents)

## 2.12. Organising tasks with folders

So far, every Task just floats around in one big list. We want users to be able to create their own folders (like "Deep Work", "Personal Projects", "Reading List") and organise tasks into them.

We'll build this the same way we built everything else: model → migration → serializer → view → permissions → URLs.

### 2.12.1. Creating the `Folder` model

A folder is owned by exactly one user (just like a `Task`), and has a name. Let's edit `tasks/models.py` to add the `Folder` model:

```py
from django.db import models

class Folder(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        "auth.User", related_name="folders", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at"]
        # a user shouldn't be able to create two folders with the same name
        unique_together = ("owner", "name")

class Task(models.Model):
    # ...
```

Now let's link `Task` to `Folder`. Edit the `Task` model in the same file:

`tasks/models.py`

```py
# ...

class Task(models.Model):
    # existing fields...
    folder = models.ForeignKey(
        Folder, related_name="tasks", on_delete=models.SET_NULL, null=True, blank=True
    )

    # existing codes...
```

Two design decisions here are worth explaining:

- `null=True, blank=True` — a task doesn't have to belong to a folder. This also means existing tasks (created before this feature existed) don't break; they simply end up with `folder = None`, which is effectively an "All Tasks" / uncategorised bucket.
- `on_delete=models.SET_NULL` — if a user deletes a folder, we don't want to silently destroy every task inside it. Instead, Django detaches those tasks (`folder` becomes `None`) and leaves them intact.

As always, create the migration (don't apply it yet):

```bash
uv run manage.py makemigrations tasks
```

This will successfully generate a single migration file for the changes. But you'll probably see a warning like this:

```
RuntimeWarning: Got an error checking a consistent migration history... failed to resolve host 'db'
```

Why this warning?

Our `DATABASE_URL` (in `.env`) points at a host called `db` — that's the name of our Postgres service inside `compose.yaml`. Docker's internal network resolves `db` to the right container only when a command runs inside that same Docker network (e.g., via `docker compose exec web ...`).

We ran `uv run manage.py makemigrations` directly on our host machine, outside Docker entirely. Our host has no idea what `db` means — hence failed to resolve host `'db'`.

So, for now, we will be creating migrations on the host using `uv run manage.py makemigrations` as we did, ignoring the warning but apply those migrations on container:

```bash
# Rebuild the image so `COPY . .` picks up the new migration file
docker compose up --build
# Apply migrations against the real Postgres container
docker compose exec web python manage.py migrate
```

Commit changes to Git.

[⬆️ Return to Table of contents](#table-of-contents)

### 2.12.2. Creating `FolderSerializer` and updating others

We'll use `HyperlinkedModelSerializer` for `FolderSerializer`. This will be similar to `UserSerializer`.

Edit `tasks/serializers.py`:

```py
from .models import Task, Folder

class FolderSerializer(serializers.HyperlinkedModelSerializer):
    # make the `owner` field read-only
    owner = serializers.ReadOnlyField(source="owner.username")
    tasks = serializers.HyperlinkedRelatedField(
        many=True, view_name="task-detail", read_only=True
    )

    class Meta:
        model = Folder
        fields = ["url", "id", "name", "owner", "tasks", "created_at", "updated_at"]
```

Update the `TaskSerializer`:

```py
class TaskSerializer(serializers.HyperlinkedModelSerializer):
    # ...
    # include folder to override its default behavior
    folder = serializers.HyperlinkedRelatedField(
        view_name="folder-detail",
        queryset=Folder.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Task
        fields = [
            # ...
            "folder",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Restrict the `folder` dropdown/choices to folders owned by the
        # currently authenticated user, so nobody can file a task into
        # someone else's folder.
        request = self.context.get("request")
        if request is not None:
            self.fields["folder"].queryset = Folder.objects.filter(owner=request.user)
```

> [!IMPORTANT]
> `view_name="folder-detail"` won't resolve to anything yet — we haven't registered a `FolderViewSet` with the router. That's the next step.

We override `__init__` to narrow the queryset to folders owned by the currently authenticated user per-request, using `self.context["request"]` — which DRF automatically provides when a ViewSet builds the serializer.

`required=False, allow_null=True` mirror the model field (`null=True, blank=True`), so a task can be created or kept without a folder — landing in the "uncategorised" bucket.

Finally, update `UserSerializer` so a user's own folders are discoverable from their profile too, the same way `tasks` already is:

```py
class UserSerializer(serializers.HyperlinkedModelSerializer):
    # ...
    folders = serializers.HyperlinkedRelatedField(
        many=True, view_name="folder-detail", read_only=True
    )

    class Meta:
        model = User
        fields = [
            # ...
            "folders",
        ]
```

Commit changes to Git.

[⬆️ Return to Table of contents](#table-of-contents)

### 2.12.3. Creating `FolderViewSet`, permissions and URL routing

Same shape as `TaskViewSet`: a `ModelViewSet` scoped to the current user, with the owner set automatically on create.

In `tasks/views.py`:

```py
from .models import Folder, Task
from .serializers import (
    FolderSerializer,
    # ...
)

# ...

class FolderViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for folders.
    """

    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    # authenticated users can create new folders,
    # creator of a folder can update or delete it
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def perform_create(self, serializer):
        # associate authenticated user with a new folder
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Folder.objects.all()
        return Folder.objects.filter(owner=self.request.user)
```

Register the route in `tasks/urls.py`:

```py
# ...
router.register(r"folders", views.FolderViewSet, basename="folder")
# ...
```

Run the development server using `docker compose up --build` and check that everything works as expected.

> [!NOTE]
> Don't skip testing the actual permission boundaries here. Before moving on, manually verify (e.g. with curl, Postman, or the browsable API using two different accounts):
>
> - An anonymous request to `/folders/` is rejected.
> - User B cannot see User A's folders in `GET /folders/`.
> - User B gets a `404` (not a `403`) retrieving User A's folder by ID directly — `get_queryset()` filtering means it looks like it doesn't exist at all, which is more secure than confirming it exists but is forbidden.
> - User A cannot create a task whose `folder` points at User B's folder.
> - Deleting a folder detaches its tasks (`folder` becomes `null`) instead of deleting them, confirming `on_delete=SET_NULL` behaves as intended through the API, not just in the database.

Commit changes to Git.

[⬆️ Return to Table of contents](#table-of-contents)

### 2.12.4. Filtering tasks by folder

In the frontend, clicking a folder in the sidebar (e.g. "Deep Work") should display only the tasks belonging to that folder. To support this, we need an endpoint such as `/tasks/?folder=<id>` that filters tasks on the backend.

This approach is preferable to relying on `/folders/<id>/` for three reasons::

- The folder detail endpoint returns task URLs, not task data. Fetching the tasks through `/folders/<id>/` would therefore require additional client-side `GET` requests. Filtering through `/tasks/?folder=<id>` lets the frontend retrieve the complete task data in a single request.

- Tasks without a folder need to be supported. The "All Tasks" view includes tasks that don't belong to any folder. Since there is no folder resource representing these tasks, there is no `/folders/<id>/` endpoint to query. A filter such as `?folder=none` provides a way to explicitly request these uncategorised tasks.

- The nested task list returned by `/folders/<id>/` is a flat, unpaginated array. By contrast, `/tasks/?folder=<id>` uses the same `PageNumberPagination` as other task-list requests, making it more suitable for a real frontend UI.

#### 2.12.4.1. Install and register `django-filter`

Using `django-filter` is the recommended way to filter query results in DRF. So, let's install it using `uv`:

```bash
uv add django-filter
```

Add it to `INSTALLED_APPS` in `config/settings.py`:

```py
INSTALLED_APPS = [
    # ... existing django apps ...
    # 3rd-party
    "rest_framework",
    "django_filters",  # new
    "drf_spectacular",
    # Local apps
    "tasks",
]
```

Then tell DRF to use it as the default filtering backend, in the same `REST_FRAMEWORK` settings dict we already use for pagination and docs:

```py
REST_FRAMEWORK = {
    # ... existing settings ...
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}
```

#### 2.12.4.2. Creating a TaskFilter

`django-filter` works by describing what's filterable in a `FilterSet` class — the same idea as a serializer, but for query parameters instead of request bodies. Create `tasks/filters.py`:

```py
from django_filters import rest_framework as filters
from rest_framework.exceptions import ValidationError

from .models import Task


class TaskFilter(filters.FilterSet):
    # a plain NumberFilter would reject "none", so we handle it ourselves
    folder = filters.CharFilter(method="filter_folder")

    class Meta:
        model = Task
        # `completed` and `important` are booleans, so django-filter can
        # generate working filters for them automatically, no extra code.
        fields = ["completed", "important"]

    def filter_folder(self, queryset, name, value):
        # Treat "none" and "null" as requests for tasks without folder.
        if value.lower() in ("none", "null"):
            return queryset.filter(folder__isnull=True)
        # Otherwise, treat a numeric value as a folder's primary key.
        if value.isdigit():
            return queryset.filter(folder_id=value)
        # Reject any value that is neither a folder ID nor a null-folder value.
        raise ValidationError({"folder": "Must be an integer id, or 'none'."})

```

A few things worth pointing out:

- **`completed` and `important` needed zero custom code.** Listing them in `Meta.fields` is enough — `django-filter` looks at the model field types (`BooleanField`) and generates working, validated filters for `?completed=true` and `?important=false` automatically.
- **`folder` needed a custom `method`** because we want `?folder=none` to mean "tasks without a folder" — behaviour a plain numeric filter doesn't have out of the box. `method="filter_folder"` tells `django-filter` to hand off to our own function instead of generating one.
- **Raising `rest_framework.exceptions.ValidationError`** for a non-numeric, non-"none" value still gets converted into a clean `400` response by DRF.

#### 2.12.4.3. Wiring it into `TaskViewSet`

In `TaskViewSet`, add the `TaskFilter` class to `filterset_class`:

`tasks/views.py`:

```py
from tasks.filters import TaskFilter

class TaskViewSet(viewsets.ModelViewSet):
    # ...
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    filterset_class = TaskFilter # new
```

We didn't need to set `filter_backends` on the ViewSet itself — that comes from `DEFAULT_FILTER_BACKENDS` in settings, applied project-wide. `filterset_class` is the only per-view piece needed.

#### 2.12.4.4. Edit documentation for FolderViewSet

Add a `@extend_schema_view()` decorator before `FolderViewSet`:

`tasks/views.py`

```py
@extend_schema_view(
    list=extend_schema(
        summary="List all folders",
        description="Return a paginated list of the authenticated user's folders.",
        responses={
            200: OpenApiResponse(
                response=FolderSerializer,
                description="A paginated list of folders.",
            ),
        },
    ),
    create=extend_schema(
        summary="Create a folder",
        description="Create a new folder. Authentication is required. "
        "The authenticated user will be set as the owner of the folder.",
        request=FolderSerializer,
        responses={
            201: OpenApiResponse(
                response=FolderSerializer,
                description="The folder was successfully created.",
            ),
            400: OpenApiResponse(
                description="The request data was invalid, or a folder "
                "with this name already exists for this user.",
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve a folder",
        description="Return the details of a single folder.",
        responses={
            200: OpenApiResponse(
                response=FolderSerializer,
                description="The requested folder.",
            ),
            404: OpenApiResponse(
                description="The requested folder does not exist.",
            ),
        },
    ),
    update=extend_schema(
        summary="Update a folder",
        description=(
            "Replace all writable fields of an existing folder. "
            "Only the folder owner can update the folder."
        ),
        request=FolderSerializer,
        responses={
            200: OpenApiResponse(
                response=FolderSerializer,
                description="The folder was successfully updated.",
            ),
            400: OpenApiResponse(
                description="The request data was invalid, or a folder "
                "with this name already exists for this user.",
            ),
            403: OpenApiResponse(
                description="The authenticated user is not the folder owner.",
            ),
            404: OpenApiResponse(
                description="The requested folder does not exist.",
            ),
        },
    ),
    partial_update=extend_schema(
        summary="Partially update a folder",
        description=(
            "Update one or more fields of an existing folder. "
            "Only the folder owner can update the folder."
        ),
        request=FolderSerializer,
        responses={
            200: OpenApiResponse(
                response=FolderSerializer,
                description="The folder was successfully updated.",
            ),
            400: OpenApiResponse(
                description="The request data was invalid, or a folder "
                "with this name already exists for this user.",
            ),
            403: OpenApiResponse(
                description="The authenticated user is not the folder owner.",
            ),
            404: OpenApiResponse(
                description="The requested folder does not exist.",
            ),
        },
    ),
    destroy=extend_schema(
        summary="Delete a folder",
        description="Delete a folder. Only the folder owner can delete it. "
        "Tasks in the folder are not deleted — they become uncategorised.",
        responses={
            204: OpenApiResponse(
                description="The folder was successfully deleted.",
            ),
            403: OpenApiResponse(
                description="The authenticated user is not the folder owner.",
            ),
            404: OpenApiResponse(
                description="The requested folder does not exist.",
            ),
        },
    ),
)
class FolderViewSet(viewsets.ModelViewSet):
   # ...
```

Update the `schema.yaml` file with the following command (this command is also helpful for debugging):

```bash
uv run manage.py spectacular --file schema.yaml
```

Rebuild the image:

```bash
docker compose down
docker compose up --build
```

Check every enpoint and make sure that all of them are working as expected.

[⬆️ Return to Table of contents](#table-of-contents)

## 2.13. Production-ready setup with Docker, Gunicorn, and Nginx

This chapter replaces Django's development server with Gunicorn and places Nginx in front of it, while keeping the entire stack local and testable on Ubuntu or WSL.

```
Browser → http://localhost:8080 → Nginx → Gunicorn → Django → PostgreSQL
```

Nginx is the only service published to the host. Gunicorn and PostgreSQL communicate only across Docker Compose's internal network. That mirrors the application topology used in production, without requiring a domain, DNS, HTTPS certificates, a cloud server, or firewall changes.

> [!NOTE]
> This is deliberately a **production-style local test**, not an Internet-facing deployment. The URL remains \`http://localhost:8080\`; TLS, domain configuration, HSTS, and public-host hardening are out of scope here.

### 2.13.1. What this local setup verifies

After completing this section, you can verify all of the following on your Ubuntu/WSL machine:

- Django starts through Gunicorn instead of `manage.py runserver`.
- Nginx proxies application/API requests to Gunicorn.
- Nginx serves collected static files directly.
- PostgreSQL, Gunicorn, and Nginx resolve one another by Compose service name.
- Port `8000` is not published on the host; only Nginx is reachable at port `8080`.
- Container health checks, restart policies, stdout logs, and graceful Gunicorn shutdown work as expected.

### 2.13.2. Prerequisites

Keep the project directory on the Linux filesystem for a smoother Docker/WSL experience.

Update `.env` with these Django/Gunicorn settings:

```.env
DEBUG=False
SECRET_KEY=local-only-long-random-value
DATABASE_URL=postgresql://<db_user>:<user_password>@db:5432/<db_name>

ALLOWED_HOSTS=localhost,127.0.0.1
GUNICORN_WORKERS=2
GUNICORN_TIMEOUT=60

POSTGRES_DB=<db_name>
POSTGRES_USER=<db_user>
POSTGRES_PASSWORD=<user_password>
```

`DEBUG=False` is useful here because it exposes configuration mistakes that Django's development mode can hide.

### 2.13.3. Prepare Django for static files and a local host

Update `config/settings.py`:

```py
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
```

`STATIC_ROOT` is where `collectstatic` gathers Django admin assets and any project assets. That directory will be shared read-only with Nginx.

Add an inexpensive health endpoint in `config/urls.py`:

```py
from django.http import HttpResponse

def health_check(request):
    return HttpResponse("ok", content_type="text/plain")

urlpatterns = [
    path("health/", health_check, name="health"),
    # existing paths…
]
```

It gives Docker and Nginx a dependable way to confirm that Gunicorn can serve Django. It does not need authentication and should remain simple.

### 2.13.4. Run Django with Gunicorn

Install Gunicorn:

```bash
uv add gunicorn
```

Create `gunicorn.conf.py` in the repository root:

```py
import os

bind = "0.0.0.0:8000"
workers = int(os.getenv("GUNICORN_WORKERS", "2"))
timeout = int(os.getenv("GUNICORN_TIMEOUT", "60"))
graceful_timeout = 30
keepalive = 5

accesslog = "-"
errorlog = "-"
loglevel = "info"
max_requests = 1000
max_requests_jitter = 100
```

> [!NOTE]
>
> - `os.getenv` is deliberate here. `django-environ` is ideal for Django settings, but Gunicorn starts before Django has any need to load its settings; using the standard library keeps `gunicorn.conf.py` independent and simple.
> - `bind = "0.0.0.0:8000"` is required because Nginx runs in a separate container. It makes Gunicorn reachable from Nginx.

Then replace the final command in `Dockerfile`:

```dockerfile
CMD ["gunicorn", "config.wsgi:application", "--config", "gunicorn.conf.py"]
```

The existing multi-stage image and its non-root runtime stage can remain unchanged.

### 2.13.5. Add a local production-style Compose file

Keep the current `compose.yaml` for ordinary development. Create `compose.local-prod.yaml` for the local Nginx/Gunicorn test:

```yaml
services:
  web:
    # Build the image using Dockerfile in the current directory
    build: .
    # (optional) name the image
    image: oasis-task-manager
    env_file:
      - .env
    expose:
      - "8000"
    volumes:
      - staticfiles:/app/staticfiles
    # Wait for the database to pass its healthcheck and
    # start the `db` service before starting the `web` service.
    depends_on:
      db:
        condition: service_healthy
    # Automatically restart the db container unless explicitly stopped.
    restart: unless-stopped
    stop_grace_period: 35s
    healthcheck:
      test:
        [
          "CMD",
          "python",
          "-c",
          "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health/', timeout=5)",
        ]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s

  nginx:
    image: dhi.io/nginx:1.31-alpine3.24
    ports:
      # Docker Hardened Images run as non-root,
      # so Nginx should listen on an unprivileged port such as 8080, not 80.
      - "8080:8080"
    volumes:
      # Create `nginx/default.conf` in the project root
      # and mount it as a read-only file on the Nginx container.
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
      # Mount the static files directory as a read-only volume.
      - staticfiles:/static:ro
    depends_on:
      # Wait for Gunicorn to pass its healthcheck and
      # start the `web` service before starting the `nginx` service.
      web:
        condition: service_healthy
    restart: unless-stopped

  db:
    # Run PostgreSQL container using an image
    image: dhi.io/postgres:18
    env_file:
      - .env
    # Left-side names are not arbitrary; Right-side name are defined in `.env`
    # These are PostgreSQL image environment variables.
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      # Persist database data across container restarts.
      - db-data:/var/lib/postgresql
    # Expose the port only to other services on the Compose network,
    # not to the host machine.
    expose:
      - 5432
    # Automatically restart the db container unless explicitly stopped.
    restart: unless-stopped
    # Only report healthy once PostgreSQL is ready to accept connections,
    # so the web service doesn't start before the database is available.
    healthcheck:
      test:
        ["CMD", "pg_isready", "-U", "${POSTGRES_USER}", "-d", "${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  db-data:
  staticfiles:
```

The important difference from the existing Compose file is that `web` uses `expose`, not `ports`. Nginx alone maps a host port 8080 to `http://localhost:8080`.

### 2.13.6. Configure local Nginx

Create `nginx/default.conf`:

```nginx
# Give Nginx a named backend group
upstream django {
    server web:8000;
    keepalive 32;
}

server {
    listen 8080;
    server_name localhost;
    # limit an incoming request body to 10 MB (optional)
    client_max_body_size 10m;

    location /static/ {
        alias /static/;
        access_log off;
        add_header Cache-Control "public, max-age=3600";
    }

    location = /health/ {
        proxy_pass http://django;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        proxy_pass http://django;
        proxy_http_version 1.1;

        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_connect_timeout 5s;
        proxy_read_timeout 60s;
        proxy_send_timeout 60s;
    }
}
```

> [!NOTE]
> We use `$http_host` instead of `$host` intentionally so that Nginx preserves the port from the original Host header (e.g. `localhost:8080`). This allows Django/DRF to generate absolute URLs with the correct externally accessible host and port.

### 2.13.7. Build and test the stack

Run these commands from the project root:

```bash
# Validate the expanded Compose configuration.
docker compose -f compose.local-prod.yaml config

# Start PostgreSQL first, then run one-off release tasks.
docker compose -f compose.local-prod.yaml up -d --build db
docker compose -f compose.local-prod.yaml run --rm web python manage.py migrate --noinput
docker compose -f compose.local-prod.yaml run --rm web python manage.py collectstatic --noinput
```

You may face an error like this:

```bash
PermissionError: Permission denied: '/app/staticfiles/admin'
```

`collectstatic` ran as the non-root user in your DHI Python runtime image, but the new `staticfiles` named volume is owned by root. Django could read it but could not create: `/app/staticfiles/admin`. So this is a volume-permissions issue.

First confirm the runtime UID:

```bash
docker compose -f compose.local-prod.yaml run --rm --no-deps \
    web python -c "import os; print(os.geteuid(), os.getegid())"
```

It will likely print `65532 65532`, the common DHI non-root UID/GID.

Now update the `compose.local-prod.yaml` to add a service named `staticfiles-init`:

```yaml
services:
  staticfiles-init:
    image: dhi.io/python:3.14-alpine3.24-dev
    user: "0:0"
    volumes:
      - staticfiles:/app/staticfiles
    entrypoint:
      - /bin/sh
      - -ec
    command:
      - |
        mkdir -p /app/staticfiles
        chown -R 65532:65532 /app/staticfiles
    restart: "no"

  web:
    # ...
    depends_on:
      db:
        condition: service_healthy
      staticfiles-init:
        condition: service_completed_successfully
```

Now run the above commands again and check that they succeed.

Then Start Gunicorn and Nginx.

```bash
docker compose -f compose.local-prod.yaml up -d --build
```

Now test the routes:

```bash
curl -i http://localhost:8080/health/
curl -I http://localhost:8080/static/admin/css/base.css
docker compose -f compose.local-prod.yaml logs -f web nginx
```

Expected results:

- `/health/` returns `200 OK` with `ok`.
- The admin CSS request returns `200 OK` and is logged by Nginx, not Gunicorn.
- Gunicorn access/error logs appear through `web`; Nginx logs appear through `nginx`.
- `docker compose ... ps` shows the health state for `web` and `db`.

To confirm that Gunicorn is not exposed directly, `docker compose -f compose.local-prod.yaml ps` should show only the Nginx `8080->8080` port mapping. There should be no `8000->8000` or `5432->5432` mapping.

### 2.13.8. Restart and shutdown checks

Try a controlled restart:

```bash
docker compose -f compose.local-prod.yaml restart web
curl -fsS http://localhost:8080/health/
docker compose -f compose.local-prod.yaml down
```

Gunicorn receives Docker's stop signal and has 30 seconds of graceful shutdown time; Compose allows 35 seconds before forcefully stopping the container. The named `db-data` volume survives `down`, so your local PostgreSQL data remains available next time.

## The end of backend <!-- omit in toc -->

Use this setup as the deployment baseline before later adding a real domain and HTTPS. Those Internet-facing concerns should be a separate follow-up, rather than mixed into this local verification guide.

## 2.14. Initialize the React frontend

In the project root, create a folder named `frontend` and navigate into it

Then follow [this link](https://github.com/ttanvirr/react-ts-starter-template) to setup Vite-React-TypeScript, TailwindCSS and Shadcn with a theme toggler.
