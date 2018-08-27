from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.http import HttpResponseRedirect


from profiles.models import Skill


class Position(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=250)
    related_project = models.ForeignKey('Project', null=True)
    related_skill = models.ForeignKey(Skill, null=True)
    applications = models.ManyToManyField(
        'Application',
        blank=True,
        related_name="position_applications"
    )
    filled = models.BooleanField(default=False)
    filled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        related_name="position"
    )

    def __str__(self):
        return self.title


class Project(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="project"
    )
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    requirements = models.CharField(max_length=100)
    timeline = models.CharField(max_length=30, blank=True, default="")
    completed = models.BooleanField(default=False)

    positions = models.ManyToManyField(Position, blank=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return HttpResponseRedirect(
            reverse('projects:view-project', kwargs={'pk': self.pk})
        )

    def delete(self, using=None, keep_parents=False):
        self.positions.all().delete()
        return super(Project, self).delete()


class Application(models.Model):
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="application"
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name="applications_position"
    )
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
