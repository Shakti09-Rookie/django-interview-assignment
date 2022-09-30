from django.db import models
from django.contrib.auth.models import AbstractUser

# # # Create your models here.

ROLE_CHOICES = (
    ("LIBRARIAN", "LIBRARIAN"),
    ("MEMBER", "MEMBER"),
)
class User(AbstractUser):

    role_type = models.CharField(max_length=25, choices=ROLE_CHOICES)