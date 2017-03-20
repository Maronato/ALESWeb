from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.core import mail
import time


# https://github.com/mailgun/transactional-email-templates
def welcome_email(user):
    context = {
        'username': user.user.name,
        'url': settings.SITE_URL + reverse('password_set', args={user.key}),
        'project_url': settings.SITE_URL
    }
    to = user.active_email
    fr = str(settings.DEFAULT_FROM_EMAIL)
    msg_plain = render_to_string('main/email/welcome_email.txt', context)
    msg_html = render_to_string('main/email/welcome_email.html', context)

    send_mail(
        'Confirmação do ALES',
        msg_plain,
        fr,
        [to],
        html_message=msg_html,
    )


def send_change_email(user, email):
    context = {
        'username': user.user.name,
        'url': settings.SITE_URL + reverse('change_email', args={user.key}),
        'project_url': settings.SITE_URL
    }
    print(context['url'])
    to = email
    fr = str(settings.DEFAULT_FROM_EMAIL)
    msg_plain = render_to_string('main/email/change_email.txt', context)
    msg_html = render_to_string('main/email/change_email.html', context)

    send_mail(
        'Alteração de email',
        msg_plain,
        fr,
        [to],
        html_message=msg_html,
    )


def event_warning_students(data):
    """Event Warning Students
    Takes a list of dicts containing a Student, the html body of an email and the plain email body
    and sends the emails to all of them using a single SMTP connection
    Accessed through the students_event_reminder command
    """

    # get the smtp connection
    connection = mail.get_connection()

    # Manually open the connection
    connection.open()

    # for each email in data
    for email in data:

        # get the from field
        fr = str(settings.DEFAULT_FROM_EMAIL)

        # construct the message
        msg = EmailMultiAlternatives(
            'Lembrete de eventos',
            email['plain'],
            fr,
            [email['student'].email],
        )
        # attach the html version
        msg.attach_alternative(email['html'], "text/html")

        # email away
        msg.send()

    # close the connection
    connection.close()


def event_warning_teachers(data):
    """Event Warning Teachers
    Takes a list of dicts containing a Teacher, the html body of an email and the plain email body
    and sends the emails to all of them using a single SMTP connection
    Accessed through the teachers_event_reminder command
    """

    # get the smtp connection
    connection = mail.get_connection()

    # Manually open the connection
    connection.open()

    # for each email in data
    for email in data:

        # get the from field
        fr = str(settings.DEFAULT_FROM_EMAIL)

        # construct the message
        msg = EmailMultiAlternatives(
            'Lembrete de eventos',
            email['plain'],
            fr,
            [email['teacher'].email],
        )
        # attach the html version
        msg.attach_alternative(email['html'], "text/html")

        # email away
        msg.send()

    # close the connection
    connection.close()


def generic_message(instance, sent=0):
    """Event Warning Teachers
    Takes a list of dicts containing a Teacher, the html body of an email and the plain email body
    and sends the emails to all of them using a single SMTP connection
    Accessed through the teachers_event_reminder command
    """

    start_time = time.time()

    emails = []
    for course in instance.courses.all():
        for student in course.students.all():

            context = {
                'instance': instance,
                'project_url': settings.SITE_URL
            }

            msg_plain = render_to_string('main/email/generic_message.txt', context)
            msg_html = render_to_string('main/email/generic_message.html', context)

            msg_plain = msg_plain.replace('$$nome$$', student.name)
            msg_plain = msg_plain.replace('$$curso$$', course.name)
            msg_html = msg_html.replace('$$nome$$', student.name)
            msg_html = msg_html.replace('$$curso$$', course.name)

            emails.append({'html': msg_html, 'plain': msg_plain, 'student': student})

    # get the smtp connection
    connection = mail.get_connection()

    # Manually open the connection
    connection.open()

    # From field
    fr = str(settings.DEFAULT_FROM_EMAIL)

    # for each email in data
    for i, email in enumerate(emails[sent:]):

        # construct the message
        msg = EmailMultiAlternatives(
            instance.subject,
            email['plain'],
            fr,
            [email['student'].email],
        )
        # attach the html version
        msg.attach_alternative(email['html'], "text/html")

        # email away
        msg.send()

        # Mind timeouts
        if time.time() - start_time >= 25:

            # close the connection
            connection.close()

            return i + 1 + sent, len(emails)

    # close the connection
    connection.close()

    return len(emails), len(emails)
