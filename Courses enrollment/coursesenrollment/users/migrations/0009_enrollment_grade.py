# Generated by Django 4.2.2 on 2023-07-09 17:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_enrollment_status_customuser_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='grade',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)]),
        ),
    ]
