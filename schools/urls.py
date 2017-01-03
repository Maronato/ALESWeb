from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'update-cities/', views.update_city, name='update-cities'),
    url(r'update-schools/', views.update_school, name='update-schools'),
    url(r'update-years/', views.update_year, name='update-years'),
    url(r'update-students/(?P<school_id>\d+)', views.update_student, name='update-students'),
    url(r'student-info/$', views.student_info, name='student-info'),
    url(r'student-courses/$', views.change_courses, name='student-courses'),
]

# (?P<school_id>\d+)
