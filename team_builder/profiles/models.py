from django.conf import settings
from django.db import models


class Skill(models.Model):
    skill = models.CharField(max_length=30)

    def __str__(self):
        return self.skill


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    display_name = models.CharField(max_length=50, null=True, blank=True)
    bio = models.CharField(max_length=500, blank=True, default="")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    skills = models.ManyToManyField(Skill, blank=True)

    def __str__(self):
        return self.display_name

    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = self.user.username
        try:
            profile = Profile.objects.get(id=self.id)
            if profile.avatar != self.avatar:
                profile.avatar.delete(save=False)
        except:
            pass
        super(Profile, self).save(*args, **kwargs)