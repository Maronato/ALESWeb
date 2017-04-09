from django.shortcuts import render, get_object_or_404, redirect
from .forms import TeacherFormSet, TeacherForm, ChangeCoursesTeacherForm, TeacherInfo, EmailListForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from main.decorators import *
from courses.models import Event
from teachers.models import EmailList
from django.conf import settings
from django.http import Http404, JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from main.email_helpers import generic_message
from django.utils import timezone
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
        form = TeacherInfo(request.POST, instance=request.user.teacher)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            form.apply(request)
            messages.add_message(request, messages.SUCCESS, 'Informações atualizadas!')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TeacherInfo(instance=request.user.teacher)

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


def download_presence(request, event_id):
    """Download Presence

    returns the presence list for a given event in PDF form
    """
    event = get_object_or_404(Event, id=event_id)

    fevent = []
    for student in event.students.order_by('name'):
        status = False
        if student in event.students_attended.all():
            status = True
        fevent.append(
            {
                'name': student.name,
                'year': student.year,
                'school': student.school.name,
                'status': status
            }
        )

    return render(request, 'teachers/pdf_presence.html', {'fevent': fevent, 'event': event})


@user_passes_test(is_teacher)
def email_lists(request):
    """List of Email Lists

    returns a list of created email lists and allows the teacher to send them
    """

    return render(request, 'teachers/email_lists.html', {'emails': request.user.teacher.email_lists.all().order_by('-created')})


@user_passes_test(is_teacher)
def create_email_list(request):
    """Create email lists view
    """

    if request.method == 'POST':
        form = EmailListForm(request.POST)
        if form.is_valid():
            new = form.save()

            new.teacher = request.user.teacher

            new.save()
            messages.add_message(request, messages.SUCCESS, 'Lista Criada!')
            form = EmailListForm()
            return redirect('email-lists')
    else:
        form = EmailListForm()

    form.fields["courses"].queryset = request.user.teacher.courses.all()

    return render(request, 'teachers/create_email_list.html', {'form': form})


@user_passes_test(is_teacher)
def edit_email_list(request, email_id):
    """Create email lists view
    """
    instance = get_object_or_404(EmailList, id=email_id)

    if instance not in request.user.teacher.email_lists.all():
        raise Http404

    if request.method == 'POST':
        form = EmailListForm(request.POST, instance=instance)
        if form.is_valid():
            new = form.save()

            new.teacher = request.user.teacher

            new.save()
            messages.add_message(request, messages.SUCCESS, 'Lista editada!')
            form = EmailListForm(instance=instance)
            return redirect("email-lists")
    else:
        form = EmailListForm(instance=instance)

    form.fields["courses"].queryset = request.user.teacher.courses.all()

    return render(request, 'teachers/edit_email_list.html', {'form': form, 'id': email_id})


@user_passes_test(is_teacher)
def preview_email_list(request):
    """Preview email list
    """
    try:
        email_id = request.POST['email_id']
    except MultiValueDictKeyError:
        email_id = None

    if email_id:
        instance = get_object_or_404(EmailList, id=email_id)
    else:
        instance = EmailList(
            title=request.POST['title'],
            subject=request.POST['subject'],
            message=request.POST['message'],
            theme=request.POST['theme'],
            teacher=request.user.teacher,
            greeting=request.POST['greeting'],
            html=True if request.POST['html'] == 'true' else False
        )

    instance.message = instance.message.replace('$$nome$$', "NOME DO ALUNO")
    instance.message = instance.message.replace('$$curso$$', "NOME DO CURSO")
    instance.title = instance.title.replace('$$nome$$', "NOME DO ALUNO")
    instance.title = instance.title.replace('$$curso$$', "NOME DO CURSO")

    context = {
        'instance': instance,
        'project_url': settings.SITE_URL
    }

    return render(request, 'main/email/generic_message.html', context)


@user_passes_test(is_teacher)
def send_email_list(request, email_id):
    """Send email list
    """
    instance = get_object_or_404(EmailList, id=email_id)
    sent = int(request.POST['sent'])

    if instance not in request.user.teacher.email_lists.all():
        raise Http404

    sent, total = generic_message(instance, sent)

    instance.sent = timezone.localtime(timezone.now())
    instance.save()

    return JsonResponse({'sent': sent, 'total': total})
