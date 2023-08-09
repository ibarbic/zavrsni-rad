# Generated by Django 4.2.2 on 2023-08-08 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_alter_enrollment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='status',
            field=models.CharField(choices=[('Fail', 'Fail'), ('Pass', 'Pass'), ('Dropped', 'Dropped'), ('Enrolled', 'Enrolled')], default='Enrolled', max_length=30),
        ),
    ]
