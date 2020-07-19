import uuid
import os

from django.db import models
from django.conf import settings

from user.models import AbstractModel
from poetster.validators import validate_image_file_size


def poem_image_file_path(instance, filename):
    """Generate the file path for uploading image to a poem"""
    ext = filename.split('.')[-1]
    name = filename.split('.')[0]

    filename = f'{name}-{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/poem/images/', filename)


class PoemManager(models.Manager):
    """Managing poem objects"""
    def is_published(self):
        """Return only published poems"""
        return super().get_queryset().filter(is_published=True)

    def up_vote_toggle(self, user, poem):
        """Logic for up voting toggle"""
        if user in poem.up_votes.all():
            is_upvoted = False
            poem.up_votes.remove(user)
        else:
            is_upvoted = True
            poem.up_votes.add(user)
        return is_upvoted


class Poem(AbstractModel):
    """Poem that can be submitted by any auth user"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.SET_NULL, related_name='poems', null=True)
    categories = models.ManyToManyField('Category', related_name='poems')
    up_votes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='voted_by', blank=True)
    title = models.CharField(max_length=75, blank=False)
    summary = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=False)
    is_published = models.BooleanField(default=True)
    image = models.ImageField(validators=[validate_image_file_size], upload_to=poem_image_file_path, null=True,
                              blank=True)
    objects = PoemManager()

    def __str__(self):
        return f'{self.user} - {self.title}'

    @property
    def up_vote_count(self):
        return self.up_votes.count()


class CategoryManager(models.Manager):
    """Managing category objects"""
    def active(self):
        return super().get_queryset().filter(disabled=False)


class Category(AbstractModel):
    """Categories to describe poem"""
    name = models.CharField(max_length=75, unique=True)
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
    name = models.CharField(max_length=75, unique=True)
    disabled = models.BooleanField(default=False)

    objects = GenreManager()

    def __str__(self):
        return self.name
