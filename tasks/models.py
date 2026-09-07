from django.db import models


class Folder(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        "auth.User", related_name="folders", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at"]
        # a user shouldn't be able to create two folders with the same name
        unique_together = ("owner", "name")


class Task(models.Model):
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        "auth.User", related_name="tasks", on_delete=models.CASCADE
    )
    folder = models.ForeignKey(
        Folder, related_name="tasks", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
