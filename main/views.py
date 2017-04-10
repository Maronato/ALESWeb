from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from .models import Email_Manager
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from schools.models import School, Student
from courses.models import Course
from courses.date_comparisons import AllEvents
from teachers.models import Teacher
from .forms import ContactForm
import re
import json
# Create your views here.


def index(request, contactform=None):
    # Index page

    schools = School.objects.all()
    students = Student.objects.all()
    teachers = Teacher.objects.all()
    courses = Course.objects.all()
    if contactform is None:
        contactform = ContactForm()
    return render(request, 'main/index.html', {
        'contactform': contactform,
        'schools': schools,
        'students': students,
        'teachers': teachers,
        'courses': courses
    })


def how_it_works(request):
    # How it Works.

    return render(request, 'main/how_it_works.html')


def enroll(request):
    # Enrollment page
    return render(request, 'main/enroll.html', {'courses': Course.objects.all().order_by('name')})


def simulation_check(request):
    options = dict(request.POST)
    selected = []
    for i in options:
        id = re.findall(r'options\[(.+?)\]\[status\]', i)
        if id and json.loads(options[i][0]):
            selected.append(Course.objects.get(id=int(id[0])))

    messages = []
    for index, course in enumerate(selected):
        gen_1 = AllEvents(course=course)
        for kourse in selected[index + 1:]:
            gen_2 = AllEvents(course=kourse)
            if gen_1.compare(gen_2):
                messages.append("Você não pode se inscrever ao mesmo tempo em " + course.name + " e " + kourse.name)
    return JsonResponse({'messages': messages})


def contact(request):

    if request.method == 'POST':

        form = ContactForm(request.POST)

        if form.is_valid():
            form.send()
            messages.add_message(request, messages.SUCCESS, 'Mensagem enviada com sucesso!')
        else:
            return index(request, form)

    return redirect('index')


def login_user(request):
    # Custom login method
    context = {}
    if request.method == 'POST':
        # Recover username and password
        username = request.POST['username'].lower()
        password = request.POST['password']
        # Authenticates them
        user = authenticate(username=username, password=password)
        # If the user exists
        if user is not None:
            # and has confirmed their emails
            if user.is_active:
                # Login them and redirect to the dashboard
                login(request, user)
                return redirect('dashboard')
            # If the user has not verified their emails, tell them that
            messages.add_message(request, messages.SUCCESS, 'Seu usuário está inativo. Procure pelo email de confirmação em sua caixa de entrada.')
        # If the user does not exist, tell them that
        else:
            messages.add_message(request, messages.SUCCESS, 'Usuário ou senha incorretos.')
        # Reload the username and pass it as the context so that ppl dont have to retype it
        context = {'username': username}
    return render(request, 'main/login.html', context)


@login_required
def dashboard(request):
    # Dashboard. Requires the user to be logged

    # Load the context
    context = {
        'school_list': School.objects.all()
    }

    # If the user is a teacher, load their events
    if request.user.is_teacher:
        context['event_list'] = request.user.teacher.events.all()

    return render(request, 'main/dashboard.html', context)


@login_required
def logout_user(request):
    logout(request)
    return redirect('index')


def confirm_email(request, key):
    """Confirm Email
    receives a key and tries to confirm it
    if the key is valid, reload the page with a form to set their passwords
    when the user submits the password, set it as key's owner password, confirm the key and login the user
    """

    # Get the key's owner
    manager = Email_Manager.find_key(key)
    # If the key does not exist or was already used, redirect to index and tell them that
    if not manager or manager.is_active:
        messages.add_message(request, messages.SUCCESS, 'Chave de ativação inválida ou já usada.')
        return redirect('index')

    # If the user is submitting their new passwords(POST)
    if request.method == 'POST':
        # Load the data
        form = SetPasswordForm(manager.user.user, request.POST)
        # If the password is valid
        if form.is_valid():
            form.save()
            # Login the new user and validate their accounts
            login(request, manager.user.user)
            Email_Manager.confirm(key)
            messages.add_message(request, messages.SUCCESS, 'Sua conta foi ativada com sucesso!')
            return redirect('dashboard')
    # If the user just clicked the activation link, generate a password form
    else:
        form = SetPasswordForm(manager.user.user)
    return render(request, 'main/set_password.html', {'form': form, 'key': key})


def unsubscribe(request, key):
    """Unsubscribe
    receives a key and unsubscribes the user from the email list
    """

    # Get the key's owner
    manager = Email_Manager.find_key(key)
    # If the key does not exist or was already used, redirect to index and tell them that
    if not manager:
        messages.add_message(request, messages.SUCCESS, 'Chave inválida.')
        return redirect('index')

    manager.user.is_subscribed = False
    manager.user.save()

    messages.add_message(request, messages.SUCCESS, 'Pronto! Você não receberá mais emails como aquele.')
    return redirect('index')


def change_email(request, key):
    """Change Email
    receives a key and changes their email
    """

    # Get the key's owner
    manager = Email_Manager.find_key(key)
    # If the key does not exist or was already used, redirect to index and tell them that
    if not manager:
        messages.add_message(request, messages.SUCCESS, 'Chave inválida.')
        return redirect('index')

    # Confirm the key
    Email_Manager.confirm(key)

    messages.add_message(request, messages.SUCCESS, 'Pronto! Email confirmado!')
    return redirect('index')


@login_required
def change_password(request):
    # Allows users to change their passwords

    if request.method == 'POST':
        # Do all the good stuff
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Senha alterada com sucesso!')
            return redirect('dashboard')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'main/change_password.html', {'form': form})


def redirect_to_sites(request):
    """Redirect to Sites

    Redirects to the Sites course github page
    """

    return redirect("https://github.com/ProjetoALES/AulasWeb")


def redirect_to_games(request):
    """Redirect to Games

    Redirects to the Games course github page
    """

    return redirect("https://github.com/ProjetoALES/AulasGames")
