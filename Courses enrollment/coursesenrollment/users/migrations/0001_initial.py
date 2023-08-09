# Generated by Django 4.2.2 on 2023-07-04 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ime', models.CharField(max_length=255)),
                ('kod', models.CharField(max_length=16, unique=True)),
                ('program', models.TextField(default='None')),
                ('points', models.IntegerField(blank=True, null=True)),
                ('semester_regular', models.IntegerField(blank=True, null=True)),
                ('semester_part_time', models.IntegerField(blank=True, null=True)),
                ('elective', models.CharField(max_length=2)),
            ],
            options={
                'db_table': 'courses',
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=55, unique=True, verbose_name='email')),
                ('password', models.CharField(max_length=128, unique=True)),
                ('status', models.CharField(default='none', max_length=10)),
                ('username', models.CharField(max_length=30)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_staff', models.IntegerField(default=False)),
                ('is_active', models.IntegerField(default=True)),
                ('is_superuser', models.IntegerField(default=False)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'role',
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='fail', max_length=64)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.courses')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.customuser')),
            ],
            options={
                'db_table': 'enrollments',
            },
        ),
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='users.role'),
        ),
        migrations.AddField(
            model_name='courses',
            name='professor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.customuser'),
        ),
    ]