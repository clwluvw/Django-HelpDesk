from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = models.CharField('First Name', max_length=50)
    last_name = models.CharField('Last Name', max_length=50)
    approved = models.BooleanField('Approved', default=False)

    class Meta:
        permissions = (
            ("client", "Client"),
            ("support", "Support"),
        )
