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
