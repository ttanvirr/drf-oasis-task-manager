from django.contrib.auth.models import User
from rest_framework import generics, permissions

from tasks.permissions import IsOwnerOrAdmin

from .models import Task
from .serializers import TaskSerializer, UserRegistrationSerializer, UserSerializer


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


class UserRegistration(generics.CreateAPIView):
    """
    Create a new user account.
    """

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    # Allow anyone to register
    permission_classes = [permissions.AllowAny]


class UserMe(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update the currently authenticated user.
    """

    serializer_class = UserSerializer
    # authenticated users can read or update their own profile
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """We won't receive a pk in the URL, so we return the currently authenticated user."""
        return self.request.user


class UserList(generics.ListAPIView):
    """
    List all users (GET).
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    # authenticated users can read users
    permission_classes = [permissions.IsAuthenticated]


class UserDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve (GET) or update (PUT) a single user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
