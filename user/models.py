from django.db import models
from django.contrib.auth.models import User
from core.models import Tag

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    followed_tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.user.username