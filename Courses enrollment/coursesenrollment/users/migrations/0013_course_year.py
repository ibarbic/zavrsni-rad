# Generated by Django 4.2.2 on 2023-08-03 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_enrollment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='year',
            field=models.IntegerField(default=0),
        ),
    ]
