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

    TESTED_CHOICES = [
        ('BLOOD', "Antibody Testing"),
        ('SWAB', 'Neonatal Nasopharyngeal Swabs'),
    ]
    tested = models.CharField(
        max_length=10,
        choices=TESTED_CHOICES,
        default='BLOOD',
    )

    def __str__(self):
        return self.user.get_full_name()


class ScientificArticles(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    date = models.DateField()
    author = models.CharField(max_length=100)
    publication = models.CharField(max_length=100)


class NewsArticle(models.Model):
    title = models.CharField(max_length=100)
    headline = models.CharField(max_length=1000)
    image = models.FileField()
    text = models.TextField()
    date = models.DateField()
    author = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
