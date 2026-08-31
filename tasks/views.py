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
