"""project URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import TemplateView
import main.urls

handler404 = 'main.views.handler404'
handler500 = 'main.views.handler500'

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^school/', include('schools.urls')),
    url(r'^teachers/', include('teachers.urls')),
    url(r'^courses/', include('courses.urls')),
    url(r'^auth/', include('custom_auth.urls', namespace='custom_auth')),

    # Logo
    url(r'^logo$', TemplateView.as_view(template_name='main/misc/logo.html')),
    # Alt Logo
    url(r'^altlogo$', TemplateView.as_view(template_name='main/misc/altlogo.html')),

    # Google search verification
    url(r'^google7db2e931cb4e4f1b\.html$', TemplateView.as_view(template_name='main/misc/google.html', content_type='text/plain')),

    # SSL verification
    url(r'^\.well-known/acme-challenge/xtCko2G6DyrAKxyo_uBouEi3ZB1PvkFSbdy2ZPf_O-E', TemplateView.as_view(template_name="main/misc/ssl.html")),
]
urlpatterns += main.urls.urlpatterns
