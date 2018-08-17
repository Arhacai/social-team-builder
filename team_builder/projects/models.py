from django.conf import settings
from django.db import models


class Position(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=140)

    def __str__(self):
        return self.title


class Project(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="project")
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=140)
    requirements = models.CharField(max_length=100)
    timeline = models.CharField(max_length=30, blank=True, default="")

    positions = models.ManyToManyField(Position, blank=True)

    def __str__(self):
        return self.title
