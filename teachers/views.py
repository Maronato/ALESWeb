from django.shortcuts import render
from .forms import TeacherFormSet, TeacherForm, ChangeCoursesTeacherForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from main.decorators import *
# Create your views here.


@user_passes_test(is_admin)
def update_teacher(request):
    """Update Teacher
    Allows the Admin to add and update teachers' information, except passwords.
    Generates a FormSet with all the teachers' infos
    """

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TeacherFormSet(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # Aplly it
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Professores atualizados!')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TeacherFormSet()

    return render(request, 'teachers/update_teachers.html', {'formset': form})


@user_passes_test(is_teacher)
def update_info(request):
    """Update Info - Teacher
    Allows Teachers to update their info
    Shows on Teacher Dashboard
    """

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TeacherForm(request.POST, instance=request.user.teacher)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Informações atualizadas!')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TeacherForm(instance=request.user.teacher)

    return render(request, 'teachers/teacher_info.html', {'form': form})


@user_passes_test(is_teacher)
def change_courses(request):
    """Change Courses - Teacher
    Allows Teachers to change their enrolled courses
    Shows on Teacher Dashboard
    """

    if request.method == 'POST':
        form = ChangeCoursesTeacherForm(request.POST, instance=request.user.teacher)
        print(form)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Cursos atualizados!')
    else:
        form = ChangeCoursesTeacherForm(instance=request.user.teacher)

    return render(request, 'teachers/teacher_courses.html', {'form': form})
