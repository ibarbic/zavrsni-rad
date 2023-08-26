
from django.contrib import admin
from django.urls import path, include
from university.views import home
from users.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('superadmin/', admin.site.urls),
    path('admin/', admin_view, name='admin'),
    path('admin_courses_add/', admin_courses_add_view, name='admin_courses_add'),
    path('admin_courses/', admin_courses_view, name='admin_courses'),
    path('admin_courses_edit/<int:pk>/', admin_courses_edit_view, name='admin_courses_edit'),
    path('admin_students', admin_students_view, name='admin_students'),
    path('admin_professors', admin_professors_view, name='admin_professors'),
    path('admin_students_add', admin_students_add_view, name='admin_students_add'),
    path('admin_students_edit/<int:pk>/', admin_students_edit_view, name='admin_students_edit'),
    path('admin_students_regular', admin_students_regular_view, name='admin_students_regular'),
    path('admin_students_partTime', admin_students_partTime_view, name='admin_students_partTime'),
    path('admin_courses_students/<int:pk>/',admin_courses_students_view, name='admin_courses_students'),
    path('admin_students_regular', admin_students_regular_view, name='admin_students_regular'),
    path('admin_students_partTime', admin_students_partTime_view, name='admin_students_partTime'),
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('register', registration_view, name='register'),
    path('student/<int:pk>/', student_view_pk, name='student'),
    path('professor_courses/', professor_courses_view, name='professor_courses'),
    path('professor/', professor_view, name='professor'),
    path('professor_students', professor_students_view, name='professor_students'),
    path('professor_courses_students/<int:pk>/',professor_courses_students_view, name='professor_courses_students'),
    path('professor_students_fail/<int:pk>/', professor_students_fail_view, name='professor_students_fail'),
    path('professor_students_pass/<int:pk>/',professor_students_pass_view, name='professor_students_pass'),
    path('professor_students_droppedOut/<int:pk>/',professor_students_droppedOut_view, name='professor_students_droppedOut'),
    path('professor_posts/<int:pk>/', professor_posts_view, name='professor_posts'),
    path('professor_posts_add/', professor_posts_add_view, name='professor_posts_add'),
    path('professor_posts_edit/<int:pk>', professor_posts_edit_view, name='professor_posts_edit'),
    path('admin_posts/<int:pk>', admin_posts_view, name='admin_posts'),
    path('admin_posts_edit/<int:pk>/', admin_posts_edit_view, name='admin_posts_edit'),
    path('admin_posts_add/<int:pk>', admin_posts_add_view, name='admin_posts_add'),
    path('student_posts/<int:pk>', student_posts_view, name='student_posts'),
    path('student_courses/', student_courses_view, name='student_courses'),
    path('student_index/<int:pk>', student_index_view, name='student_index'),
    path('professor_index/<int:pk>/', professor_index_view, name='professor_index'),
    path('professor_grade_edit/<int:pk>/', professor_grade_edit_view, name='professor_grade_edit'),
    path('professor_statistic/<int:pk>/', professor_statistic_view, name='professor_statistic'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
