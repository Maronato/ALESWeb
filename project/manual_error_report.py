import sys
from django.core import mail
from django.views.debug import ExceptionReporter
from django.core.mail import send_mail
from django.conf import settings


def exception_email(request, e):
    try:
        exc_info = sys.exc_info()
        reporter = ExceptionReporter(request, is_email=True, *exc_info)
        subject = e.message.replace('\n', '\\n').replace('\r', '\\r')[:989] if getattr(e, 'message', False) else 'Erro não identificado'
        message = reporter.get_traceback_text()
        mail.mail_admins(
            subject, message, fail_silently=False,
            html_message=reporter.get_traceback_html()
        )
    except Exception as ee:
        to = str(settings.ADMINS[0][1])
        fr = str(settings.DEFAULT_FROM_EMAIL)
        try:
            mail.mail_admins(
                "Unexpected error " + e + " and " + ee,
                '"' + e + '" and "' + ee + '"',
                fail_silently=False,
                html_message=reporter.get_traceback_html()
            )
        except Exception as eee:
            send_mail(
                'Really Unexpected Error',
                '"' + e + '" and "' + ee + '" and "' + eee + '"',
                fr,
                [to],
            )
