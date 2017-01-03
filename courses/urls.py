from django.conf.urls import url
from . import views

urlpatterns = [
    # Admin view, update and add courses
    url(r'^update-courses/', views.update_course, name='update-courses'),
    # Teacher view, create events
    url(r'^create-event/', views.create_event, name='create-event'),
    # Teacher view, edit and delete events
    url(r'^update-events/', views.update_event, name='update-events'),
    # Teacher view, view and modify presence list of event_id
    url(r'presence-list/(?P<event_id>\d+)', views.presence_list, name='presence-list'),
]
