# Generated by Django 4.2.2 on 2023-07-04 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_rename_courses_course_alter_role_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='elective',
        ),
    ]
