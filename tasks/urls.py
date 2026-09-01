from django.urls import include, path
from rest_framework.routers import DefaultRouter

from tasks import views

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r"tasks", views.TaskViewSet, basename="task")
router.register(r"users", views.UserViewSet, basename="user")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path("", include(router.urls)),
]
