from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from tasks.permissions import IsOwnerOrReadOnly

from .models import Task
from .serializers import TaskSerializer, UserSerializer


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


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(["GET"])
def api_root(request, format=None):
    # return a json response of a list of available endpoints
    return Response(
        {
            "users": reverse("user-list", request=request, format=format),
            "tasks": reverse("task-list", request=request, format=format),
        }
    )
