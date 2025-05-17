from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField(blank=True, default='')
    image_url = models.URLField(default='https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/330px-No-Image-Placeholder.svg.png')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='posts')
    url = models.URLField(default='')
    
    def __str__(self):
        return self.title
