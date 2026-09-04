from django.contrib.auth.models import User
from rest_framework import generics, permissions, viewsets
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
)

from tasks.permissions import IsOwnerOrAdmin, IsSuperuser

from .models import Task
from .serializers import TaskSerializer, UserRegistrationSerializer, UserSerializer


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
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
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
