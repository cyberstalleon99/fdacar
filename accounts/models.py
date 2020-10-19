from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class UserDesignation(models.Model):
    name =              models.CharField(max_length=250)
    description =       models.TextField()

    def __str__(self):
        return self.name

def profile_directory_path(instance, filename):
    return 'accounts/inspector/user_{0}/{1}'.format(instance.user.get_short_name(), filename)

class Profile(models.Model):
    user =          models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    designation =   models.ManyToManyField(UserDesignation)
    img =           models.ImageField(null=True, blank=True, upload_to=profile_directory_path, verbose_name='Profile Pic')

    def __str__(self):
        return self.user.get_short_name()

    def designations(self):
        return ",\n".join(s.name for s in self.designation.all())

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class  User(AbstractBaseUser):
    email =             models.EmailField(verbose_name='email address', max_length=255, unique=True)
    first_name =        models.CharField(max_length=255)
    middle_initial =    models.CharField(max_length=1)
    last_name =         models.CharField(max_length=255)
    active =            models.BooleanField(default=True)
    staff =             models.BooleanField(default=False) # a admin user; non super-user
    admin =             models.BooleanField(default=False) # a superuser
    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.
    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name + " " + self.middle_initial + ". " + self.last_name

    def get_short_name(self):
        full_name = self.get_full_name()
        splitted = full_name.split()
        short_name = ""
        for i in range(len(splitted)-1):
            full_name = splitted[i]
            short_name += (full_name[0].upper())
        short_name += splitted[-1].title()
        return short_name

    def get_initials(self):
        full_name = self.get_full_name()
        splitted = full_name.split()
        initials = ""
        for i in range(len(splitted)):
            full_name = splitted[i]
            initials += (full_name[0].upper())
        return initials

    def __str__(self):              # __unicode__ on Python 2
        return self.get_short_name()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active
