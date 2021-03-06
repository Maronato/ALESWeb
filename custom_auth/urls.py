"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib.auth.views import logout
from . import views

urlpatterns = [
    # /custom_auth/+
    # Receives a key and verifies the user if the key is valid. Redirects to facebook login screen
    url(r'^fb/(?P<key>[\w]+)', views.confirm_facebook, name='confirm_facebook'),

    url(r'facebook/remove_facebook/$', views.remove_facebook, name='remove_facebook'),
    url(r'facebook/add_facebook/$', views.add_facebook, name='add_facebook'),

    url(r'facebook/login/$', views.facebook_login, name='facebook_login'),
    url(r'facebook/login/(?P<key>\w+)$', views.facebook_login, name='facebook_login'),
    url(r'facebook/login_response/$', views.facebook_login_response, name='facebook_login_response'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
]
