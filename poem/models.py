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


class PoemManager(models.Manager):
    """Managing poem objects"""
    def is_published(self):
        """Return only published poems"""
        return super().get_queryset().filter(is_published=True)


class Poem(AbstractModel):
    """Poem that can be submitted by any auth user"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.SET_NULL, null=True, related_name='poems')
    categories = models.ManyToManyField('Category', related_name='poems')
    title = models.CharField(max_length=75, blank=False)
    summary = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=False, null=False)
    is_published = models.BooleanField(default=True)
    image = models.ImageField(null=True, blank=True, upload_to=poem_image_file_path)

    objects = PoemManager()

    def __str__(self):
        return f'{self.user} - {self.title}'


class CategoryManager(models.Manager):
    """Managing category objects"""
    def active(self):
        return super().get_queryset().filter(disabled=False)


class Category(AbstractModel):
    """Categories to describe poem"""
    name = models.CharField(max_length=75)
    disabled = models.BooleanField(default=False)

    objects = CategoryManager()

    def __str__(self):
        return self.name


class GenreManager(models.Manager):
    """Managing genre objects"""

    def active(self):
        return super().get_queryset().filter(disabled=False)


class Genre(AbstractModel):
    """Genre to describe poem"""
    name = models.CharField(max_length=75)
    disabled = models.BooleanField(default=False)

    objects = GenreManager()

    def __str__(self):
        return self.name