from django.contrib.auth.models import User
from rest_framework import generics, permissions

from tasks.permissions import IsOwnerOrAdmin

from .models import Task
from .serializers import TaskSerializer, UserSerializer


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


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve (GET), update (PUT), or delete (DELETE) a single task.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # Authenticated users can access tasks (read, update, delete).
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]


class UserList(generics.ListAPIView):
    """
    List all users (GET).
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Authenticated users can access users (read).
    permission_classes = [permissions.IsAuthenticated]


class UserDetail(generics.RetrieveAPIView):
    """
    Retrieve (GET) a single user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Authenticated users can access his profile (read).
    permission_classes = [permissions.IsAuthenticated]
