from django.shortcuts import redirect, reverse
from .facebook_methods import auth_url, login_successful, login_canceled

from .helpers import get_user_from_key, remove_key_from_user, get_obj_from_key

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.conf import settings

from schools.models import Student
from teachers.models import Teacher

# Create your views here.


def facebook_login(request, key=None):

    # Generate auth_url and redirect to it
    return redirect(auth_url(request, key))


def facebook_login_response(request, key=None):
    """Facebook Login Response

    Try to access 'code' from the response. If found, the login was successful. Unsuccessful otherwise
    """

    user = get_user_from_key(key)

    try:
        code = request.GET['code']
    except:
        # User cancelled login
        request = login_canceled(request)
        return redirect(reverse('index'))

    request = login_successful(code, request, user, key)
    remove_key_from_user(key)
    return redirect(reverse('dashboard'))


def confirm_facebook(request, key):
    """Confirm Facebook
    receives a key and checks if a user has it
    it someone does, redirect them to the facebook login page

    if does not, tell them that and redirect to index
    """
    if get_obj_from_key(key) is not None:
        return redirect('custom_auth:facebook_login', key=key)
    messages.add_message(request, messages.SUCCESS, 'Chave de ativação inválida ou já usada.')
    return redirect('index')


@login_required
def remove_facebook(request):
    """Remove Facebook
    """
    if request.user.is_teacher:
        obj = request.user.teacher
    elif request.user.is_student:
        obj = request.user.student
    else:
        messages.add_message(request, messages.ERROR, 'Usuário tem que ser aluno ou professor')
        return redirect('dashboard')
    if obj.has_facebook:
        obj.has_facebook = False
        obj.save()
        obj.facebookuser.delete()
        messages.add_message(request, messages.SUCCESS, 'Facebook desvinculado com sucesso!')
        return redirect('dashboard')
    messages.add_message(request, messages.ERROR, 'Usuário tem que ter associado o Facebook')
    return redirect('dashboard')


@login_required
def add_facebook(request):
    """add facebook account
    """
    if request.user.is_teacher:
        obj = request.user.teacher
    elif request.user.is_student:
        obj = request.user.student
    else:
        messages.add_message(request, messages.ERROR, 'Usuário tem que ser aluno ou professor')
        return redirect('dashboard')

    if not obj.has_facebook:
        # get a unique random string for the url
        url = get_random_string(length=5)
        while Student.objects.filter(facebook_create_url=url).exists() or Teacher.objects.filter(facebook_create_url=url).exists():
            url = get_random_string(length=5)
        obj.facebook_create_url = url
        obj.save()
    else:
        url = False
    url = settings.SITE_URL + reverse('custom_auth:confirm_facebook', kwargs={"key": url})
    return redirect(url)
