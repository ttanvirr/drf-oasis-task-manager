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
