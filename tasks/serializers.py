from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Task, Folder


class FolderSerializer(serializers.HyperlinkedModelSerializer):
    # make the `owner` field read-only
    owner = serializers.ReadOnlyField(source="owner.username")
    tasks = serializers.HyperlinkedRelatedField(
        many=True, view_name="task-detail", read_only=True
    )

    class Meta:
        model = Folder
        fields = ["url", "id", "name", "owner", "tasks", "created_at", "updated_at"]


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    # make the `owner` field read-only
    owner = serializers.ReadOnlyField(source="owner.username")
    # include folder to override its default behavior
    folder = serializers.HyperlinkedRelatedField(
        view_name="folder-detail",
        queryset=Folder.objects.all(),
        required=False,
        allow_null=True,
    )

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
            "folder",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Restrict the `folder` dropdown/choices to folders owned by the
        # currently authenticated user, so nobody can file a task into
        # someone else's folder.
        request = self.context.get("request")
        if request is not None:
            self.fields["folder"].queryset = Folder.objects.filter(owner=request.user)


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
    folders = serializers.HyperlinkedRelatedField(
        many=True, view_name="folder-detail", read_only=True
    )

    class Meta:
        model = User
        fields = [
            "url",
            "id",
            "username",
            "tasks",
            "folders",
        ]
