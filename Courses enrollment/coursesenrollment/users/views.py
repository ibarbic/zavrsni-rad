from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, TemplateView, UpdateView
from .models import CustomUser, Course, Enrollment,Post
from .forms import StudentForm, UserRegisterForm, UserAuthenticationForm, CourseForm, PostForm, ProfessorPostForm,ProfessorIndexForm

def home_view(request):
    user = request.user      
    if  request.user.is_anonymous:
        print(user)
        return HttpResponseRedirect(reverse('home'))
    else:
        if user:
                if(user.role.name == "Professor"):
                    return HttpResponseRedirect(reverse('professor'))
                elif(user.role.name == "Admin"):
                    return HttpResponseRedirect(reverse('admin'))
                    #return HttpResponseRedirect(reverse('home'))
                elif(user.role.name == "Student"):
                    return HttpResponseRedirect('/student/' + str(user.pk) + '/')
    
        
    return HttpResponseRedirect(reverse('login'))
def registration_view(request):
    context = {}
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data['password1']
            account = authenticate(email=email, password=raw_password)
            print(email, raw_password)
            messages.success(
                request, f'Your account has been created! You are now able to log in.')
            return HttpResponseRedirect(reverse('login'))
        else:
            context['registration_form'] = form
    else:
        form = UserRegisterForm()
        context['registration_form'] = form
    context['title'] = 'Register'

    return render(request, 'register', context)

def logout_view(request):
    logout(request)
    courses = Course.objects.all()
    for course in courses:
        print(course.pk)
    context = {}
    context['title'] = 'Logout'
    return render(request, 'logout', context)


def login_view(request):
    context = {}
    user = request.user

    if user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    if request.POST:
        form = UserAuthenticationForm(request.POST)

        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                if(user.role.name == "Professor"):
                    return HttpResponseRedirect(reverse('professor'))
                elif(user.role.name == "Admin"):
                    return HttpResponseRedirect(reverse('admin'))
                    #return HttpResponseRedirect(reverse('home'))
                elif(user.role.name == "Student"):
                     return HttpResponseRedirect('/student/' + str(user.pk) + '/')
                return HttpResponseRedirect(reverse('home'))
    else:
        form = UserAuthenticationForm()

    context['login_form'] = form
    context['title'] = 'Login'
    return render(request, 'login', context)

@login_required
def student_view_pk(request, pk):
    context = {}
    user = CustomUser.objects.get(pk=pk)
    enrollment = Enrollment.objects.all()
    courses = Course.objects.all()
    enrollment_filtered = set()
    courses_filtered = set()
    counter_regular = 0
    counter_parttime = 0
    redovni_polozeni = 0
    izvanredni_polozeni = 0
    if request.user.role.name == "Student" and request.user.pk != user.pk:
        return HttpResponseRedirect(reverse('home'))

    flag = True
    for course in courses:
        if course.semester_regular == 1 or course.semester_regular == 2:
            counter_regular = counter_regular + 1
        if course.semester_part_time == 3 or course.semester_part_time == 4:
            counter_parttime = counter_parttime + 1
        for enroll in enrollment:
            if course.id == course.pk and user.id == enroll.course.pk:
                enrollment_filtered.add(course)
                flag = False

        if flag:
            enrollment_filtered.add(course)
            courses_filtered.add(course)
        flag = True

    if request.POST:
        for course in courses_filtered:
            if request.POST.get(str(course))=="added":
                obj, created = Enrollment.objects.get_or_create(user=user, course=course)
                if(created):
                    obj.save()
                    messages.success(request, "Upisano: " + course.name)
        for enrollment_f in enrollment_filtered:
            if request.POST.get(str(enrollment_f)):
                for enroll in enrollment:
                    if enrollment_f.pk == enroll.course.pk and user.pk == enroll.user.pk:
                        if request.POST.get(str(enrollment_f)) == "Fail":
                            enrollment.filter(pk=str(enroll.pk)).update(
                                status="Fail")
                            messages.success(
                                request, "Nije položeno: " + enrollment_f.name)

                        elif request.POST.get(str(enrollment_f)) == "Pass" and request.user.role.name == "Professor":
                            enrollment.filter(pk=str(enroll.pk)).update(
                                status="Pass")
                            messages.success(
                                request, "Položeno: " + enrollment_f.name)
                        elif request.POST.get(str(enrollment_f)) == "remove":
                            enroll.delete()
                            messages.success(
                                request, "Ispisano: " + enrollment_f.name)
        return HttpResponseRedirect('/student/' + str(pk) + '/')

    enrollment_html = ""
    br_sem = 0
    if user.status == "regular":
        br_sem = 6
    elif user.status == "part time":
        br_sem = 8
    for i in range(br_sem):
        enrollment_html += "<div class='semestar'>"
        enrollment_html += "<p>Semestar " + str(i+1) + ":</p>"
        enrollment_html += "<table>"
        for enroll in enrollment:
            course = courses.get(pk=enroll.course.pk)
            if user.pk == enroll.user.pk:
                if user.status == "regular" and course.semester_regular == i+1:
                    if enroll.status == "Pass":
                        enrollment_html += "<tr><td></td><td><button type='submit' class='add-btn' name='" + \
                            str(course) + \
                            "' value='Fail'>&#10004;</button></td>"
                    elif enroll.status == "Fail":
                        if request.user.role.name == "Professor":
                            enrollment_html += "<tr><td><button type='submit' class='add-btn' name='" + \
                                str(course) + \
                                "' value='Pass'>&#10004;</button></td>"
                        enrollment_html += "<td><button type='submit' class='add-btn' name='" + \
                            str(course) + \
                            "' value='remove'>&#10006;</button></td>"
                    enrollment_html += "<td>" + course.name + "</td></tr>"
                elif user.status == "part time" and course.semester_part_time == i+1:
                    if enroll.status == "Pass":
                        enrollment_html += "<tr><td></td><td><button class='add-btn' type='submit' name='" + \
                            str(course) + \
                            "' value='Fail'>&#10004;</button></td>"
                    elif enroll.status == "Fail":
                        if request.user.role.name == "Professor":
                            enrollment_html += "<tr><td><button type='submit' class='add-btn' name='" + \
                                str(course) + \
                                "' value='Pass'>&#10004;</button></td>"
                        enrollment_html += "<td><button type='submit' class='add-btn' name='" + \
                            str(course) + \
                            "' value='remove'>&#10006;</button></td>"
                    enrollment_html += "<td>" + course.name + "</td></tr>"
        enrollment_html += "</table>"
        enrollment_html += "</div>"
    if user.status == "regular":
        for enroll in enrollment:
            temp_course = Course.objects.get(pk=enroll.course.pk)
            # print(temp_predmet.sem_redovni)
            if enroll.user.pk == user.pk and (temp_course.semester_regular == 1 or temp_course.semester_regular == 2) and enroll.status_choices == "Fail":
                redovni_polozeni = redovni_polozeni + 1
    else:
        for enroll in enrollment:
            temp_course = Course.objects.get(pk=enroll.course.pk)
            if enroll.user.pk == user.pk and (temp_course.semester_part_time == 3 or temp_course.semester_part_time == 4) and enroll.status == "Pass":
                izvanredni_polozeni = izvanredni_polozeni + 1

    context = {
        'user': user,
        'courses': courses_filtered,
        'enrollment': enrollment_html,
        'title': user.email,
        'regular_pass': redovni_polozeni,
        'counter_regular': counter_regular,
        'part_time': counter_parttime,
    }


    return render(request, 'student', context)

@login_required
def professor_view(request):
    print(request.user.role.name)
    if request.user.role.name != "Professor":
        print(request.user.role.name)
        return HttpResponseRedirect(reverse('home'))
    context = {}
    context['title'] = str(request.user.email)
    return render(request, 'professor', context)

@login_required
def professor_students_view(request):
    context = {}
    users = CustomUser.objects.all()
    if request.user.role.name != "Professor":
        return HttpResponseRedirect(reverse('home'))
    context = {
        'users': users,
        'title': str(request.user.email),
    }
    return render(request, 'professor_students', context)

@login_required
def professor_courses_students_view(request, pk):
    if request.user.role.name != "Professor":
        return HttpResponseRedirect(reverse('home'))
    course = Course.objects.get(pk=pk)
    print(course.name)
    users = CustomUser.objects.filter(role=3)
    enrollment = Enrollment.objects.filter(course=pk)
    #upisi = Upisi.objects.all()
    users_filtered = set()
    context = {}

    for enroll in enrollment:
        for user in users:
            print(enroll.user.pk)
            if enroll.user.pk == user.pk:
                users_filtered.add(user)

    context['users'] = users_filtered
    context['title'] = str(request.user.email)
    context['course'] = course

    return render(request, 'professor_courses_students', context)

@login_required
def professor_courses_view(request):
    print(request)
    if request.user.role.name != "Professor":
        return HttpResponseRedirect(reverse('home'))
    context = {}
    courses = Course.objects.filter(professor=request.user.pk)
    #predmeti = Predmeti.objects.all()
    for course in courses:
        print(course.professor)
    if request.POST:
        for course in courses:
            if request.POST.get(str(course)) == 'delete':
                messages.success(request, "Izbrisano: " + str(course.name))
                course.delete()
                return HttpResponseRedirect(reverse('professor_courses'))
            elif request.POST.get(str(course)) == 'edit':
                return HttpResponseRedirect(reverse('professor_courses_edit', args=(course.pk,)))
    context = {
        'courses': courses,
        'title': str(request.user.email),
    }
    return render(request, 'professor_courses', context)

@login_required
def professor_students_fail_view(request, pk):
    if request.user.role.name != "Professor":
        return HttpResponseRedirect(reverse('home'))
    course = Course.objects.get(pk=pk)
    users = CustomUser.objects.filter(role=3)
    enrollment = Enrollment.objects.filter(course=pk)
    #upisi = Upisi.objects.all()
    users_filtered = set()
    context = {}

    for enroll in enrollment:
        for user in users:
            if enroll.user.pk == user.pk and enroll.status == "Fail":
                users_filtered.add(user)

    context['users'] = users_filtered
    context['title'] = str(request.user.email)

    return render(request, 'professor_students_fail', context)


@login_required
def professor_students_pass_view(request, pk):
    if request.user.role.name != "Professor":
        return HttpResponseRedirect(reverse('home'))
    course = Course.objects.get(pk=pk)
    users = CustomUser.objects.filter(role=3)
    enrollment = Enrollment.objects.filter(course=pk)
    #upisi = Upisi.objects.all()
    users_filtered = set()
    context = {}

    for enroll in enrollment:
        for user in users:
            if enroll.user.pk == user.pk and enroll.status == "Pass":
                users_filtered.add(user)

    context['users'] = users_filtered
    context['title'] = str(request.user.email)

    return render(request, 'professor_students_pass', context)


@login_required
def professor_students_droppedOut_view(request, pk):
    if request.user.role.name != "Professor":
        return HttpResponseRedirect(reverse('home'))
    course = Course.objects.get(pk=pk)
    users = CustomUser.objects.filter(role=3)
    enrollment = Enrollment.objects.filter(course=pk)
    #upisi = Upisi.objects.all()
    users_filtered = set()
    context = {}

    for enroll in enrollment:
        for user in users:
            if enroll.user.pk == user.pk and enroll.status == "DropOut":
                users_filtered.add(user)

    context['users'] = users_filtered
    context['title'] = str(request.user.email)

    return render(request, 'professor_students_droppedOut', context)

@login_required
def admin_view(request):
    if request.user.role.name != "Admin":
        return HttpResponseRedirect(reverse('home'))
    context = {}
    context['title'] = str(request.user.email)
    return render(request, 'admin', context)

@login_required
def admin_courses_view(request):
    if request.user.role.name != "Admin":
        return HttpResponseRedirect(reverse('home'))
    context = {}
    courses = Course.objects.all()

    if request.POST:
        for course in courses:
            if request.POST.get(str(course)) == 'delete':
                messages.success(request, "Izbrisano: " + str(course.name))
                course.delete()
                return HttpResponseRedirect(reverse('admin_courses'))
            elif request.POST.get(str(course)) == 'edit':
                return HttpResponseRedirect(reverse('admin_courses_edit', args=(course.id,)))
    context = {
        'courses': courses,
        'title': str(request.user.email),
    }
    return render(request, 'admin_courses', context)

@login_required
def admin_courses_add_view(request):
    if request.user.role.name != "Admin":
        return HttpResponseRedirect(reverse('home'))
    context = {}
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Predmet has been created!')
            return HttpResponseRedirect(reverse('admin_courses'))
        else:
            context['course_add_form'] = form
    else:
        form = CourseForm()
        context['course_add_form'] = form
    context['title'] = str(request.user.email)

    return render(request, 'admin_courses_add', context)

@login_required
def admin_students_view(request):
    context = {}
    users = CustomUser.objects.all()
    print(request.user.role.name)
    if request.user.role.name != "Admin":
        return HttpResponseRedirect(reverse('home'))
    context = {
        'users': users,
        'title': str(request.user.email),
    }
    return render(request, 'admin_students', context)

@login_required
def admin_students_regular_view(request):
    context = {}
    users = CustomUser.objects.all()
    if request.user.role.name != "Admin":
        return HttpResponseRedirect(reverse('home'))
    context = {
        'users': users,
        'title': str(request.user.email),
    }
    return render(request, 'admin_students_regular', context)


@login_required
def admin_students_partTime_view(request):
    context = {}
    users = CustomUser.objects.all()
    if request.user.role.name != "Admin":
        return HttpResponseRedirect(reverse('home'))
    context = {
        'users': users,
        'title': str(request.user.email),
    }
    return render(request, 'admin_students_partTime', context)

@login_required
def admin_students_add_view(request):
    if request.user.role.name != "Admin":
        return HttpResponseRedirect(reverse('home'))
    context = {}
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Student has been created!')
            return HttpResponseRedirect(reverse('professor_students'))
        else:
            context['student_add_form'] = form
    else:
        form = StudentForm()
        context['student_add_form'] = form
    context['title'] = str(request.user.email)

    return render(request, 'admin_students_add.', context)

@login_required
def admin_students_edit_view(request, pk):
    if request.user.role.name != "Admin":
        return HttpResponseRedirect(reverse('home'))
    student = CustomUser.objects.get(pk=pk)
    context = {}
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f'Student has been edited!')
            return HttpResponseRedirect(reverse('professor_students'))
        else:
            context['student_edit_form'] = form
    else:
        form = StudentForm(instance=student)
        context['student_edit_form'] = form
    context['student'] = student
    context['title'] = str(request.user.email)

    return render(request, 'admin_students_edit', context)

@login_required
def admin_professors_view(request):
    context = {}
    users = CustomUser.objects.all()
    if request.user.role.name != "Admin":
        return HttpResponseRedirect(reverse('home'))
    context = {
        'users': users,
        'title': str(request.user.email),
    }
    return render(request, 'admin_professors', context)

@login_required
def admin_students_regular_view(request):
    context = {}
    users = CustomUser.objects.all()
    if request.user.role.name != "Admin":
        return HttpResponseRedirect(reverse('home'))
    context = {
        'users': users,
        'title': str(request.user.email),
    }
    return render(request, 'admin_students_regular', context)


@login_required
def admin_students_partTime_view(request):
    context = {}
    users = CustomUser.objects.all()
    if request.user.role.name != "Admin":
        return HttpResponseRedirect(reverse('home'))
    context = {
        'users': users,
        'title': str(request.user.email),
    }
    return render(request, 'admin_students_partTime', context)

@login_required
def admin_students_add_view(request):
    if request.user.role.name != "Admin":
        return HttpResponseRedirect(reverse('home'))
    context = {}
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Student has been created!')
            return HttpResponseRedirect(reverse('professor_students'))
        else:
            context['student_add_form'] = form
    else:
        form = StudentForm()
        context['student_add_form'] = form
    context['title'] = str(request.user.email)

    return render(request, 'admin_students_add', context)


@login_required
def admin_students_edit_view(request, pk):
    if request.user.role.name != "Admin":
        return HttpResponseRedirect(reverse('home'))
    student = CustomUser.objects.get(pk=pk)
    context = {}
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f'Student has been edited!')
            return HttpResponseRedirect(reverse('professor_students'))
        else:
            context['student_edit_form'] = form
    else:
        form = StudentForm(instance=student)
        context['student_edit_form'] = form
    context['student'] = student
    context['title'] = str(request.user.email)

    return render(request, 'admin_students_edit', context)

@login_required
def admin_courses_students_view(request, pk):
    if request.user.role.name != "Admin":
        return HttpResponseRedirect(reverse('home'))
    course = Course.objects.get(pk=pk)

    users = CustomUser.objects.filter(role=3)
    enrollment = Enrollment.objects.filter(course=pk)
    #upisi = Upisi.objects.all()
    users_filtered = set()
    context = {}

    for enroll in enrollment:
        for user in users:
            if enroll.user.pk == user.pk:
                users_filtered.add(user)

    context['users'] = users_filtered
    context['title'] = str(request.user.email)

    return render(request, 'admin_courses_students.', context)

@login_required
def admin_courses_edit_view(request, pk):

    if request.user.role.name != "Admin":
        return HttpResponseRedirect(reverse('home'))
    course = Course.objects.get(pk=pk)
    context = {}
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f'Predmet has been edited!')
            return HttpResponseRedirect(reverse('admin_courses'))
        else:
            context['course_edit_form'] = form
    else:
        form = CourseForm(instance=course)
        context['course_edit_form'] = form
    context['course'] = course
    context['title'] = str(request.user.email)

    return render(request, 'admin_courses_edit', context)

# def admin_posts_view(request, pk):
#     posts = Post.objects.filter(course = pk)
#     print(posts)
#     return render(request, 'admin_posts', {'posts': posts, })
@login_required
def admin_posts_view(request, pk):
    if request.user.role.name != "Admin":
        return HttpResponseRedirect(reverse('home'))
    context = {}
    
    posts = Post.objects.filter(course=pk)
    if request.POST:
        for post in posts:
            print(post)
            if request.POST.get(str(post)) == 'delete':
                messages.success(request, "Izbrisano: " + str(post.title))
                post.delete()
                return HttpResponseRedirect(reverse('admin_posts', args= pk,))
            elif request.POST.get(str(post)) == 'edit':
                return HttpResponseRedirect(reverse('admin_posts_edit', args=(post.pk,)))
    context = {
        'posts': posts,
    }
    return render(request, 'admin_posts', context)


def admin_posts_edit_view(request, pk):
    if request.user.role.name != "Admin":
        return HttpResponseRedirect(reverse('home'))
    post = Post.objects.get(pk = pk)
    context = {}
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, f'Post has been edited!')
            return HttpResponseRedirect(reverse('admin_posts', args=(post.course.pk,)))
        else:
            context['post_edit_form'] = form
    else:
        form = PostForm(instance=post)
        context['post_edit_form'] = form
        
    context['post'] = post
    context['title'] = post.title
    return render(request, 'admin_post_edit', context)

@login_required
def admin_posts_add_view(request,pk):
    if request.user.role.name != "Admin":
        return HttpResponseRedirect(reverse('home'))
    context = {}
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            tempform = form.save(commit=False)
            tempform.user = request.user
            tempform.save()
            messages.success(request, f'Post has been created!')
            return HttpResponseRedirect(reverse('admin_courses'))
        else:
            context['post_add_form'] = form
    else:
        form = PostForm()
        context['post_add_form'] = form
    context['title'] = str(request.user.email)

    return render(request, 'admin_posts_add', context)

@login_required
def professor_posts_view(request, pk):
    if request.user.role.name != "Professor":
        return HttpResponseRedirect(reverse('home'))
    context = {}
    course = Course.objects.filter(pk=pk)
    posts = Post.objects.filter(course=pk)
    if request.POST:
        if(course[0].professor.pk == request.user.pk):
            for post in posts:
            
                if request.POST.get(str(post)) == 'delete':
                    messages.success(request, "Izbrisano: " + str(post.title))
                    post.delete()
                    return HttpResponseRedirect(reverse('admin_posts', args= pk,))
                elif request.POST.get(str(post)) == 'edit':
                    return HttpResponseRedirect(reverse('admin_posts_edit', args=(post.pk,)))
    context = {
        'posts': posts,
        'professor' : course[0].professor,
        'user' : request.user,
    }
    return render(request, 'professor_posts', context)


def professor_posts_edit_view(request, pk):
    if request.user.role.name != "Professor":
        return HttpResponseRedirect(reverse('home'))
    post = Post.objects.get(pk = pk)
    context = {}
    if request.method == 'POST':
        form = ProfessorPostForm(request.POST, instance=post, request=request)
        print("aaaa")
        if form.is_valid():
            
            form.save()
            messages.success(request, f'Post has been edited!')
            return HttpResponseRedirect(reverse('professor_posts', args=(post.course.pk,)))
        else:
            context['post_edit_form'] = form
    else:
        form = ProfessorPostForm(instance=post,request=request)
        context['post_edit_form'] = form
        
    context['post'] = post
    context['title'] = post.title
    return render(request, 'professor_post_edit', context)

@login_required
def professor_posts_add_view(request,pk):
    if request.user.role.name != "Professor":
        return HttpResponseRedirect(reverse('home'))
    context = {}
    if request.method == 'POST':
        form = ProfessorPostForm(request.POST)
        if form.is_valid():
            tempform = form.save(commit=False)
            tempform.user = request.user
            tempform.save()
            messages.success(request, f'Post has been created!')
            return HttpResponseRedirect(reverse('professor_courses'))
        else:
            context['post_add_form'] = form
    else:
        form = ProfessorPostForm(request=request)
        context['post_add_form'] = form
    context['title'] = str(request.user.email)

    return render(request, 'professor_posts_add', context)

@login_required
def student_posts_view(request, pk):
    if request.user.role.name != "Student":
        return HttpResponseRedirect(reverse('home'))
    context = {}
    posts = Post.objects.filter(course=pk)
    print(posts)
    context = {
        'posts': posts,
        'user' : request.user,
    }
    return render(request, 'student_posts', context)

@login_required
def student_courses_view(request):
    print(request)
    if request.user.role.name != "Student":
        return HttpResponseRedirect(reverse('home'))
    context = {}
    enrollment = Enrollment.objects.filter(user=request.user.pk)
    courses_filtered= set()
    for enroll in enrollment:
        courses_filtered.add(enroll.course)
    context = {
        'courses': courses_filtered,
        'title': str(request.user.email),
    }
    return render(request, 'student_courses', context)

@login_required
def student_index_view(request, pk):
    if request.user.role.name != "Student":
        return HttpResponseRedirect(reverse('home'))
    print(request.user.status)
    context = {}
    enrollment = Enrollment.objects.filter(user=request.user.pk)
    enrollment_filtered= set()
    if(request.user.status == "regular"):
        for enroll in enrollment:
            if (enroll.course.semester_regular == pk):
                enrollment_filtered.add(enroll)
    if(request.user.status == "part time"):
        for enroll in enrollment:
            if (enroll.course.semester_part_time == pk):
                enrollment_filtered.add(enroll)
    context = {
        'enrollment': enrollment_filtered,
        'title': str(request.user.email),
        'number' : pk,
        'user' : request.user,
    }
    return render(request, 'student_index', context)

@login_required
def professor_index_view(request, pk):
    if request.user.role.name != "Professor":
        return HttpResponseRedirect(reverse('home'))
    context = {}
    user = CustomUser.objects.get(pk=pk)
    print(user.first_name)
    enrollment = Enrollment.objects.all()
    enrollment_filtered= set()
    for enroll in enrollment:
        if (enroll.course.professor == request.user and enroll.user.pk == pk):
            enrollment_filtered.add(enroll)

    context = {
        'enrollment': enrollment_filtered,
        'title': str(request.user.email),
        'student' : user,
        'user' : request.user,
    }
    return render(request, 'professor_index', context)

@login_required
def professor_grade_edit_view(request, pk):
    if request.user.role.name != "Professor":
        return HttpResponseRedirect(reverse('home'))
    enroll = Enrollment.objects.get(pk=pk)
    user = enroll.user
    context = {}
    if request.method == 'POST':
        print(user.email)
        form = ProfessorIndexForm(request.POST, instance=enroll)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('professor_courses'))
        else:
            context['grade_edit_form'] = form
    else:
        form = ProfessorIndexForm(instance=enroll)
        context['grade_edit_form'] = form
    context['student'] = user
    context['title'] = str(request.user.email)
    context['course'] = enroll.course

    return render(request, 'professor_grade_edit', context)
