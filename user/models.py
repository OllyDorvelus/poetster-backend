import uuid
import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


def profile_image_file_path(instance, filename):
    """Generate the file path for uploading image to a poem"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/profile/images/', filename)


class AbstractModel(models.Model):
    """Abstract model that handles common fields"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    pen_name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.pen_name


class Profile(AbstractModel):
    """Extending user module for more information about the user
        Don't want to modify the given django user model too much"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name='follow_by', symmetrical=False)
    bio = models.TextField(blank=True)
    instagram = models.URLField(blank=True)
    image = models.ImageField(null=True, upload_to=profile_image_file_path)

    def __str__(self):
        return self.user.pen_name

# Signals
@receiver(post_save, sender=User)
def add_profile_when_user_created(sender, instance, created, **kwargs):
    if created:
        new_profile = Profile.objects.create(user=instance)
        new_profile.save()