from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.db.models.deletion import CASCADE
from .managers import UserManager


from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from django.contrib import admin
from django.core.validators import MaxValueValidator, MinValueValidator
from ckeditor.fields import RichTextField
class Role(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'roles'


class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=128, default="")
    surname = models.CharField(max_length=128, default="")
    email = models.CharField(verbose_name="email", max_length=55, unique=True)
    password = models.CharField(max_length=128, unique=True)
    telephone_number= models.CharField(max_length=15,default="")
    address = models.CharField(max_length=128, default="")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default=3)
    student_number =models.CharField(max_length=128, default="")
    status = models.CharField(max_length=10, default="none")
    username = models.CharField(max_length=30)
    date_joined = models.DateTimeField(
        verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_staff = models.IntegerField(default=False)
    is_active = models.IntegerField(default=True)
    is_superuser = models.IntegerField(default=False)

    objects = UserManager()

    def __str__(self):
        return self.email  # kad zelimo isprintat ime usera dobijemo ovo

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = 'users'


class Course(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(unique=True, max_length=16)
    program = models.TextField(default="None")
    points = models.IntegerField(null=True, blank=True)
    year = models.IntegerField(default=0)
    semester_regular = models.IntegerField(null=True, blank=True)
    semester_part_time = models.IntegerField(null=True, blank=True)
    YES = "Yes"
    NO = "No"
    
    elective_choices = [
        (NO, "No"),
        (YES, "Yes"),
        
    ]
    elective = models.CharField(max_length=30, choices= elective_choices, default=NO)
    professor = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'courses'



class Enrollment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.IntegerField(blank=False, default= 1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    date = models.DateTimeField(auto_now_add=True, blank=True)
    enroll_times = models.IntegerField(blank=False, default= 1)
    FAIL = "Fail"
    PASS = "Pass"
    DROPPED = "Dropped"
    ENROLLED = "Enrolled"
    status_choices = [
        (FAIL, "Fail"),
        (PASS, "Pass"),
        (DROPPED, "Dropped"),
        (ENROLLED, "Enrolled")
    ]
    status = models.CharField(max_length=30, choices= status_choices, default=FAIL)
    class Meta:
        db_table = 'enrollments'

class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=128, default="Title")
    #content = models.CharField(max_length=9999, default="")
    content = RichTextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "posts"

# class Comment(models.Model):
#     post = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     content = models.CharField(max_length=9999, default="")
#     created_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         db_table = "comments"
        