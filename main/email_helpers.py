from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.core import mail


# https://github.com/mailgun/transactional-email-templates
def confirmation_email(user):
    context = {
        'username': user.user.name,
        'url': settings.SITE_URL + reverse('password_set', args={user.key}),
        'project_url': settings.SITE_URL
    }
    to = user.active_email
    fr = str(settings.DEFAULT_FROM_EMAIL)
    msg_plain = render_to_string('main/email/confirm_email.txt', context)
    msg_html = render_to_string('main/email/confirm_email.html', context)

    send_mail(
        'Confirmação de email',
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
