from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^update-teacher/', views.update_teacher, name='update-teachers'),
    url(r'^profile/', views.update_info, name='teacher-info'),
    url(r'^change-courses/$', views.change_courses, name='teacher-courses'),
    url(r'^coordinate-courses/$', views.coordinate_courses, name='coordinate-courses'),
    url(r'^download-presence/(?P<event_id>\d+)', views.download_presence, name='download-presence'),
    url(r'adicionar/', views.quick_add_teacher, name='quick-add-teacher'),
    url(r'^email-lists/', views.email_lists, name='email-lists'),
    url(r'^create-email-list/', views.create_email_list, name='create-email-list'),
    url(r'^edit-email-list/(?P<email_id>\d+)', views.edit_email_list, name='edit-email-list'),
    url(r'^delete-email-list/(?P<email_id>\d+)', views.delete_email_list, name='delete-email-list'),
    url(r'^preview-email/', views.preview_email_list, name='preview-email'),
    url(r'^send-email-list/(?P<email_id>\d+)?', views.send_email_list, name='send-email-list'),
]
