# Generated by Django 4.2.2 on 2023-07-04 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_course_elective'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='kod',
            new_name='code',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='ime',
            new_name='name',
        ),
        migrations.AddField(
            model_name='course',
            name='elective',
            field=models.CharField(choices=[('No', 'No'), ('Yes', 'Yes')], default='No', max_length=3),
        ),
    ]
