import uuid
import os


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


from poetster.validators import validate_image_file_size

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


class ProfileManager(models.Manager):

    def follow_toggle(self, profile_following, profile_to_follow):
        """Logic for follow toggle"""
        if profile_following in profile_to_follow.subscribers.all():
            is_followed = False
            profile_to_follow.subscribers.remove(profile_following)
        else:
            is_followed = True
            profile_to_follow.subscribers.add(profile_following)
        return is_followed

class Profile(AbstractModel):
    """Extending user module for more information about the user
        Don't want to modify the given django user model too much"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscribers = models.ManyToManyField('self', related_name='subscribed', symmetrical=False, blank=True)
    bio = models.TextField(blank=True)
    instagram = models.URLField(blank=True)
    image = models.ImageField(blank=True, validators=[validate_image_file_size], upload_to=profile_image_file_path)
    objects = ProfileManager()

    def __str__(self):
        return self.user.pen_name

    @property
    def total_subscribers(self):
        return self.subscribers.all().count()

    @property
    def total_subscribed(self):
        return Profile.objects.filter(subscribers=self).count()


# Signals
@receiver(post_save, sender=User)
def add_profile_when_user_created(sender, instance, created, **kwargs):
    if created:
        new_profile = Profile.objects.create(user=instance)
        new_profile.save()