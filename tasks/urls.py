from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from tasks import views

# API endpoints
urlpatterns = format_suffix_patterns(
    [
        path("", views.api_root, name="api-root"),
        path("tasks/", views.TaskList.as_view(), name="task-list"),
        path("tasks/<int:pk>/", views.TaskDetail.as_view(), name="task-detail"),
        path("users/", views.UserList.as_view(), name="user-list"),
        path("users/<int:pk>/", views.UserDetail.as_view(), name="user-detail"),
    ]
)
