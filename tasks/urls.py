from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from tasks import views

task_list = views.TaskViewSet.as_view({"get": "list", "post": "create"})
task_detail = views.TaskViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)
user_list = views.UserViewSet.as_view({"get": "list"})
user_detail = views.UserViewSet.as_view({"get": "retrieve"})

# API endpoints
urlpatterns = format_suffix_patterns(
    [
        path("", views.api_root, name="api-root"),
        path("tasks/", task_list, name="task-list"),
        path("tasks/<int:pk>/", task_detail, name="task-detail"),
        path("users/", user_list, name="user-list"),
        path("users/<int:pk>/", user_detail, name="user-detail"),
    ]
)
