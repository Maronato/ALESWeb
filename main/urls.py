from django.conf.urls import url
from main import views
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete

urlpatterns = [
    # Index page
    url(r'^$', views.index, name='index'),
    # Contact view
    url(r'contact/', views.contact, name='contact'),
    # Dashboard
    url(r'dashboard/', views.dashboard, name='dashboard'),
    # How it works
    url(r'como-funciona/', views.how_it_works, name='how_it_works'),
    # Simulation page
    url(r'simulate/', views.enroll, name='enroll'),
    url(r'simulation_check/', views.simulation_check, name='simulation_check'),
    # login flow
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    # Receives a key and verifies the user if the key is valid. Also asks the user to create a password
    url(r'^confirm-email/(?P<key>[\w]+)', views.confirm_email, name='password_set'),
    # Receives a key and verifies the user if the key is valid. If is, changes their active email
    url(r'^change-email/(?P<key>[\w]+)', views.change_email, name='change_email'),
    # Receives a key and unsubscribes the key owner from the email list
    url(r'^unsubscribe/(?P<key>[\w]+)', views.unsubscribe, name='unsubscribe'),
    # Allows the user to change their password
    url(r'^change-password/', views.change_password, name='password_change'),
    # Django's built-in password reset method
    url(r'^reset-password/$', password_reset, {'html_email_template_name': 'main/email/reset_password.html', 'template_name': 'main/reset_password.html'}, name='password_reset'),
    url(r'^reset-password-done/$', password_reset_done, {'template_name': 'main/reset_password_done.html'}, name='password_reset_done'),
    url(r'^reset-password-confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm, {'template_name': 'main/reset_password_confirm.html'}, name='password_reset_confirm'),
    url(r'^reset-password-complete/$', password_reset_complete, {'template_name': 'main/reset_password_complete.html'}, name='password_reset_complete'),

]
