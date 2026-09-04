from django.contrib.auth.models import User
from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from tasks.permissions import IsOwnerOrAdmin, IsSuperuser

from .models import Task
from .serializers import TaskSerializer, UserRegistrationSerializer, UserSerializer


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
