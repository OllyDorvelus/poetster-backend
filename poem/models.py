import uuid
import os

from django.db import models
from django.conf import settings

from user.models import AbstractModel


def poem_image_file_path(instance, filename):
    """Generate the file path for uploading image to a poem"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/poem/', filename)


class Poem(AbstractModel):
    """Poem that can be submitted by any auth user"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.SET_NULL, null=True, related_name='poems')
    categories = models.ManyToManyField('Category', related_name='poems')
    title = models.CharField(max_length=75, blank=False)
    summary = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=False, null=False)

    image = models.ImageField(null=True, upload_to=poem_image_file_path)


class Category(AbstractModel):
    """Categories to describe poem"""
    name = models.CharField(max_length=75)


class Genre(AbstractModel):
    """Genre to describe poem"""
    name = models.CharField(max_length=75)

