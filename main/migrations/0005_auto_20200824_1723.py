# Generated by Django 3.0.7 on 2020-08-24 17:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20200824_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='dateEnrolled',
            field=models.DateField(default=datetime.datetime(2020, 8, 24, 17, 23, 21, 131513)),
        ),
        migrations.AlterField(
            model_name='patient',
            name='dateOfBirth',
            field=models.DateField(default=datetime.datetime(2020, 8, 24, 17, 23, 21, 131578)),
        ),
        migrations.AlterField(
            model_name='patient',
            name='email',
            field=models.TextField(default='abc@email.com', help_text='Enter in correct format abc@email.com'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='ethnicity',
            field=models.TextField(default='Not Reported'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='firstName',
            field=models.TextField(default='John'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='lastName',
            field=models.TextField(default='Smith'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='phoneNumber',
            field=models.IntegerField(verbose_name=1111111111),
        ),
        migrations.AlterField(
            model_name='patient',
            name='race',
            field=models.TextField(default='Not Reported'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='timesBirth',
            field=models.PositiveIntegerField(verbose_name=0),
        ),
        migrations.AlterField(
            model_name='patient',
            name='userComment',
            field=models.CharField(default='None', max_length=1000),
        ),
    ]
