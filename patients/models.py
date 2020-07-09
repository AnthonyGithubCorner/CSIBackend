from django.db import models

from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('NA', "NA"),
        ('UNKNOWN', 'Unknown'),
        ('NEGATIVE', 'Negative'),
        ('POSITIVE', 'Positive'),
        ('RECOVERED', 'Recovered'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='NA',
    )

    def __str__(self):
        return self.user.get_full_name()
