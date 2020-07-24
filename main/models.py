from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    SMOKING_CHOICES = [
        ('CURRENT', "Current Smoker"),
        ('FORMER', 'Former Smoker'),
        ('NEVER', 'Never Smoker'),
    ]

    ALCOHOL_CHOICES = [
        ('CURRENT', "Current Drinker"),
        ('FORMER', 'Former Drinker'),
        ('NEGATIVE', 'Never Drank'),
    ]
    HOUSING_CHOICES = [
        ('ALONE', "Live Alone"),
        ('GROUP', 'Live With Others'),
    ]
    MARTIAL_CHOICES = [
        ('SINGLE', "Single"),
        ('MARRIED', 'Married'),
    ]
    INSURANCE_CHOICES = [
        ('UNINSURED', "UnInsured"),
        ('INSURED', 'Insured'),
    ]
    EMPLOYMENT_CHOICES = [
        ('EMPLOYED', "Employed"),
        ('UNEMPLOYED', 'UnEmployed'),
    ]
    DIET_CHOICES = [
        ('VEGAN', "Vegan"),
        ('VEGETARIAN', 'Vegetarian'),
        ('REGULAR', 'Regular'),
    ]
    VETERAN_CHOICES = [
        ('NOT', 'Not A Veteran'),
        ('FORMER', "Former Veteran"),
        ('CURRENT', 'Current Veteran'),
    ]
    DISABILITIES_CHOICES = [
        ('DISABLE', 'Disabled'),
        ('ABLE', "Able"),
    ]

    age = models.IntegerField(default=69,)
    height = models.IntegerField()
    weight = models.IntegerField()

    smoking = models.CharField(
        max_length=10,
        choices=SMOKING_CHOICES,
        default='NEVER',
    )
    drinking = models.CharField(
        max_length=10,
        choices=ALCOHOL_CHOICES,
        default='NEVER',
    )
    housing = models.CharField(
        max_length=10,
        choices=HOUSING_CHOICES,
        default='ALONE',
    )
    martial = models.CharField(
        max_length=10,
        choices=MARTIAL_CHOICES,
        default='ALONE',
    )
    insurance = models.CharField(
        max_length=10,
        choices=INSURANCE_CHOICES,
        default='UNINSURED',
    )
    employment = models.CharField(
        max_length=10,
        choices=EMPLOYMENT_CHOICES,
        default='INSURED',
    )
    diet = models.CharField(
        max_length=10,
        choices=DIET_CHOICES,
        default='REGULAR',
    )
    veteran = models.CharField(
        max_length=10,
        choices=VETERAN_CHOICES,
        default='NOT',
    )
    disabilities = models.CharField(
        max_length=10,
        choices=DISABILITIES_CHOICES,
        default='ABLE',
    )

    def __str__(self):
        return self.user.username


class CovidTest(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    TYPE_CHOICES = [
        ('ANTIBODY', "Antibody Testing"),
        ('ANTIGEN', 'Antigen Testing'),
    ]
    RESULT_CHOICES = [
        ('UNKNOWN', 'Unknown'),
        ('NEGATIVE', 'Negative'),
        ('POSITIVE', 'Positive'),
    ]
    HOSPITALIZATION_CHOICES = [
        ('YES', "Yes"),
        ('NO', 'No'),
    ]
    VENTILATION_CHOICES = [
        ('YES', "Yes"),
        ('NO', 'No'),
    ]
    INTERVENTION_CHOICES = [
        ('YES', "Yes"),
        ('NO', 'No'),
    ]
    MEDICATION_CHOICES = [
        ('HCQ', "Hydroxychloroquine"),
    ]
    Date = models.DateField()
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default='ANTIBODY',
    )
    results = models.CharField(
        max_length=10,
        choices=RESULT_CHOICES,
        default='UNKNOWN',
    )
    hospitalization = models.CharField(
        max_length=10,
        choices=HOSPITALIZATION_CHOICES,
        default='NO',
    )
    ventilation = models.CharField(
        max_length=10,
        choices=VENTILATION_CHOICES,
        default='NO',
    )
    medication = models.CharField(
        max_length=10,
        choices=MEDICATION_CHOICES,
        default='HCQ',
    )

    def __str__(self):
        return self.patient.user.username

class ScientificArticle(models.Model):
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


# class Point(models.Model):
#     point = gis_models.PointField()


# class ClinicalTrials(models.Model):
#     What they are searching for'
#
#     location = models.geolocation()


