from django.shortcuts import render, reverse
from .models import School
from .forms import CityFormSet, SchoolFormSet, StudentFormSet, ChangeCoursesStudentForm, StudentInfo, YearFormSet, StudentForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from main.decorators import *
# Create your views here.


@user_passes_test(is_admin)
def update_city(request):
    """Update City
    Allows for the creation end edit of cities
    """

    if request.method == 'POST':
        form = CityFormSet(request.POST)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Cidades atualizadas!')

        else:
            return render(request, 'schools/update_cities.html', {'formset': form})

    form = CityFormSet()
    return render(request, 'schools/update_cities.html', {'formset': form})


@user_passes_test(is_admin)
def update_school(request):
    """Update School
    Allows for the creation and edit of schools
    """

    if request.method == 'POST':
        form = SchoolFormSet(request.POST)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Escolas atualizadas!')

        else:
            return render(request, 'schools/update_cities.html', {'formset': form})

    form = SchoolFormSet()
    return render(request, 'schools/update_schools.html', {'formset': form})


@user_passes_test(is_admin)
def update_year(request):
    """Update Year
    Allows for the creation and edit of years
    """

    if request.method == 'POST':
        form = YearFormSet(request.POST)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Séries atualizads!')

        else:
            return render(request, 'schools/update_years.html', {'formset': form})

    form = YearFormSet()
    return render(request, 'schools/update_years.html', {'formset': form})


@user_passes_test(is_admin)
def update_student(request, school_id):
    """Update Students
    Allows for the creation and edit of students
    Takes a school ID as URL parameter
    """

    if request.method == 'POST':
        form = StudentFormSet(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Alunos atualizados!')

        else:
            return render(request, 'schools/update_students.html', {'formset': form, 'school_id': school_id})

    form = StudentFormSet(queryset=School.objects.get(id=school_id).students.all())
    return render(request, 'schools/update_students.html', {'formset': form, 'school_id': school_id, 'school': School.objects.get(id=school_id).name})


@user_passes_test(is_teacher)
def quick_add_student(request):
    """Quick add student
    Allows for the quick creation of students
    """
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Pronto! Peça que o aluno acesse seu email agora para confirmar a inscrição.')

        else:
            return render(request, 'schools/quick_add_student.html', {'form': form})

    form = StudentForm()
    return render(request, 'schools/quick_add_student.html', {'form': form})


@user_passes_test(is_student)
def student_info(request):
    """Student Info
    Allows the student to change their info
    Visible at the Student Dashboard
    """

    if request.method == 'POST':
        form = StudentInfo(request.POST, instance=request.user.student)
        if form.is_valid():
            form.save()
            form.apply(request)
            messages.add_message(request, messages.SUCCESS, 'Informações atualizadas!')
    else:
        form = StudentInfo(instance=request.user.student)

    return render(request, 'schools/student_info.html', {'form': form})


@user_passes_test(is_student)
def change_courses(request):
    """Change Courses
    Allows for the changing of the enrolled courses
    """

    if request.method == 'POST':
        form = ChangeCoursesStudentForm(request.POST, instance=request.user.student)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Cursos atualizados!')
    else:
        form = ChangeCoursesStudentForm(instance=request.user.student)
    return render(request, 'schools/student_courses.html', {'form': form})
