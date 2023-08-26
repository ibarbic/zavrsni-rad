from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, views
from .models import CustomUser, Enrollment, Course, Role, Post
from ckeditor.widgets import CKEditorWidget

class UserRegisterForm(UserCreationForm):
    STATUS_CHOICES = [
        ('regular', 'Redovni'),
        ('part time', 'Izvanredni'),
        ('none', 'none'),
    ]
    email = forms.EmailField(max_length=64)
    status = forms.CharField(
        max_length=10, widget=forms.Select(choices=STATUS_CHOICES))

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2', 'status']


class UserAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    email = forms.EmailField(max_length=64)

    class Meta:
        model = CustomUser
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            print(email, password)
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")


class UpdateEnrollmentForm(forms.Form):
    class Meta:
        model = Enrollment

class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s  %s" % (obj.first_name, obj.surname)

class CourseForm(forms.ModelForm):
    ELECTIVE_CHOICES = [
        ('No', 'Ne'),
        ('Yes', 'Da'),
    ]
    name = forms.CharField(max_length=255,label="Ime")
    code = forms.CharField(max_length=16,label= "Kod predmeta")
    year = forms.IntegerField(label="Godina predmeta")
    semester_regular = forms.IntegerField(label="Semestar (redovni studenti)")
    semester_part_time = forms.IntegerField(label="Semestar (izvanredni studenti)")
    elective = forms.CharField(
        max_length=3, widget=forms.Select(choices=ELECTIVE_CHOICES),label="Izborni predmet")
    #professor = forms.ModelChoiceField(queryset=CustomUser.objects.filter(role=2),label="Profesor",)
    professor = UserModelChoiceField(queryset=CustomUser.objects.filter(role=2),label="Profesor",)
    class Meta:
        model = Course
        fields = ['name', 'code','year', 'points', 'semester_regular','semester_part_time', 'elective', 'professor']

class RoleModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s " % (obj.name)
    
class StudentForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('regular', 'redovni'),
        ('part time', 'izvanredni'),
        ('none', 'none'),
    ]
    ELECTIVE_CHOICES = [
        (1, 'Admin'),
        (2, 'Profesor'),
        {3,'Student'},
    ]
    email = forms.EmailField(max_length=64)
    status = forms.CharField(
        max_length=10, widget=forms.Select(choices=STATUS_CHOICES))
    #role = forms.ModelChoiceField(queryset=Role.objects.all(), widget=forms.Select(choices=ELECTIVE_CHOICES))
    role =RoleModelChoiceField(queryset=Role.objects.all())
    username = forms.CharField(max_length=64)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'status', 'role', 'username', 'password']

class CourseModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)          

class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=64, label= "Naslov")
    content = forms.CharField(label="Sadrzaj", widget=CKEditorWidget())
    course =  CourseModelChoiceField(queryset=Course.objects.all())
    class Meta:
        model = Post
        fields = ['title', 'content','course']
        #widgets = {'content': RichTextFormField(config_name="default")}

class ProfessorPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ProfessorPostForm, self).__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(professor =self.request.user)
    
    title = forms.CharField(max_length=64, label= "Naslov")
    content = forms.CharField(label="Sadrzaj", widget=CKEditorWidget())
    course =  CourseModelChoiceField(queryset=Course.objects.all())
    class Meta:
        model = Post
        fields = ['title', 'content','course']
        #widgets = {'content': RichTextFormField(config_name="default")}

class ProfessorIndexForm(forms.ModelForm):

    grade = forms.IntegerField(label="Ocjena")
    class Meta:
        model = Enrollment
        fields = ['grade']
    