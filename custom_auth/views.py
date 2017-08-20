from django.shortcuts import redirect, reverse
from .facebook_methods import auth_url, login_successful, login_canceled

from .helpers import get_user_from_key, remove_key_from_user, get_obj_from_key

from django.contrib import messages

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
