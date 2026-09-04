from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Task


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


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    tasks = serializers.HyperlinkedRelatedField(
        many=True, view_name="task-detail", read_only=True
    )

    class Meta:
        model = User
        fields = ["url", "id", "username", "tasks"]
