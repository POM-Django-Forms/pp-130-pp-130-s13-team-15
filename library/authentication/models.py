import datetime
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import PermissionsMixin

ROLE_CHOICES = (
    (0, 'visitor'),
    (1, 'librarian'),
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = extra_fields.get('is_active', True)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 1)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    middle_name = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.IntegerField(choices=ROLE_CHOICES, default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    id = models.AutoField(primary_key=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.get_role_name()})"

    def get_role_name(self):
        return ROLE_CHOICES[self.role][1]

    @staticmethod
    def get_by_id(user_id):
        return CustomUser.objects.filter(id=user_id).first()

    @staticmethod
    def get_by_email(email):
        return CustomUser.objects.filter(email=email).first()

    @staticmethod
    def delete_by_id(user_id):
        user = CustomUser.objects.filter(id=user_id).first()
        if user:
            user.delete()
            return True
        return False

    @staticmethod
    def create(email, password, first_name=None, middle_name=None, last_name=None):
        if len(email) <= 100 and len(email.split('@')) == 2 and not CustomUser.objects.filter(email=email).exists():
            user = CustomUser(email=email, first_name=first_name, middle_name=middle_name, last_name=last_name)
            user.set_password(password)
            user.is_active = True
            user.save()
            return user
        return None

    def update(self, first_name=None, last_name=None, middle_name=None, password=None, role=None, is_active=None):
        if first_name and len(first_name) <= 20:
            self.first_name = first_name
        if last_name and len(last_name) <= 20:
            self.last_name = last_name
        if middle_name and len(middle_name) <= 20:
            self.middle_name = middle_name
        if password:
            self.set_password(password)
        if role is not None:
            self.role = role
        if is_active is not None:
            self.is_active = is_active
        self.save()

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': int(self.created_at.timestamp()),
            'updated_at': int(self.updated_at.timestamp()),
            'role': self.role,
            'is_active': self.is_active
        }

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True
