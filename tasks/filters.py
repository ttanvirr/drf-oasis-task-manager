from django_filters import rest_framework as filters
from rest_framework.exceptions import ValidationError

from .models import Task


class TaskFilter(filters.FilterSet):
    # a plain NumberFilter would reject "none", so we handle it ourselves
    folder = filters.CharFilter(method="filter_folder")

    class Meta:
        model = Task
        # `completed` and `important` are booleans, so django-filter can
        # generate working filters for them automatically, no extra code.
        fields = ["completed", "important"]

    def filter_folder(self, queryset, name, value):
        # Treat "none" and "null" as requests for tasks without folder.
        if value.lower() in ("none", "null"):
            return queryset.filter(folder__isnull=True)
        # Otherwise, treat a numeric value as a folder's primary key.
        if value.isdigit():
            return queryset.filter(folder_id=value)
        # Reject any value that is neither a folder ID nor a null-folder value.
        raise ValidationError({"folder": "Must be an integer id, or 'none'."})
