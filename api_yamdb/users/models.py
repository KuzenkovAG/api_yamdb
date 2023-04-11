from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import validate_email
from django.db import models

ROLES = (
    ('u', 'user'),
    ('m', 'moderator'),
    ('a', 'admin'),
)
username_validator = UnicodeUsernameValidator()


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text=('Required. 254 characters or fewer. Letters, '
                   'digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    email = models.CharField(
        max_length=254,
        unique=True,
        help_text='Required. 150 characters or fewer.',
        validators=[validate_email],
        error_messages={
            'unique': "A user with that email already exists.",
        },
    )

    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=32, choices=ROLES, default='u')
