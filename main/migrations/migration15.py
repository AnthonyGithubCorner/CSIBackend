from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_conditionshelped2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ModalityResource',
            name='articleImage',
            field=models.CharField(max_length=1000),
        ),
    ]