from django.db import models
from django.contrib.auth.models import User


def user_directory_path(instance,filename):
    return 'users/avatars/{0}/{1}'.format(instance.user.id,filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=user_directory_path, default='users/default.jpg')
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)