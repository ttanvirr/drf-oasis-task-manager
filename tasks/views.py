from venv import create

from django.contrib.auth.models import User
from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
)

from tasks.filters import TaskFilter
from tasks.permissions import IsOwnerOrAdmin, IsSuperuser

from .models import Folder, Task
from .serializers import (
    FolderSerializer,
    TaskSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)


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
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # authenticated users can create new tasks,
    # creator of a task can update or delete it
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    filterset_class = TaskFilter

    def perform_create(self, serializer):
        # associate authenticated user with a new task
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Task.objects.all()
        return Task.objects.filter(owner=self.request.user)


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
    """
    Create a new user account.
    """

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


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
    update=extend_schema(
        summary="Update a user",
        description="Update a user. Only a superuser can update a user.",
        request=UserSerializer,
        responses={
            200: OpenApiResponse(
                response=UserSerializer,
                description="The user was successfully updated.",
            ),
            400: OpenApiResponse(
                description="The request data is invalid.",
            ),
            403: OpenApiResponse(
                description="The authenticated user is not a superuser.",
            ),
            404: OpenApiResponse(
                description="The requested user does not exist.",
            ),
        },
    ),
    partial_update=extend_schema(
        summary="Partially update a user",
        description="Partially update a user. Only a superuser can update a user.",
        request=UserSerializer,
        responses={
            200: OpenApiResponse(
                response=UserSerializer,
                description="The user was successfully updated.",
            ),
            400: OpenApiResponse(
                description="The request data is invalid.",
            ),
            403: OpenApiResponse(
                description="The authenticated user is not a superuser.",
            ),
            404: OpenApiResponse(
                description="The requested user does not exist.",
            ),
        },
    ),
    destroy=extend_schema(
        summary="Delete a user",
        description="Delete a user. Only a superuser can delete a user.",
        responses={
            204: OpenApiResponse(
                description="The user was successfully deleted.",
            ),
            403: OpenApiResponse(
                description="The authenticated user is not a superuser.",
            ),
            404: OpenApiResponse(
                description="The requested user does not exist.",
            ),
        },
    ),
)
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
