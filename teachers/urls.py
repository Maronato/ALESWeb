from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^update-teacher/', views.update_teacher, name='update-teachers'),
    url(r'^profile/', views.update_info, name='teacher-info'),
    url(r'^change-courses/$', views.change_courses, name='teacher-courses'),
]
