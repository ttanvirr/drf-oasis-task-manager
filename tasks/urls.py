from django.urls import path

from tasks import views

urlpatterns = [
    path("tasks/", views.task_list),
    path("tasks/<int:pk>/", views.task_detail),
]
