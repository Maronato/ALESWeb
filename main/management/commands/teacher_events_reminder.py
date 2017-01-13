from django.core.management.base import BaseCommand
from teachers.models import Teacher
from datetime import datetime, timedelta
from main.email_helpers import event_warning_teachers
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
import locale
locale.setlocale(locale.LC_TIME, "pt_BR")


class Command(BaseCommand):
    help = 'Send email to teachers about future events'

    # Checks each teachers' events and creates an email with all the future events' infos

    def add_arguments(self, parser):
        parser.add_argument('days', )

    def handle(self, *args, **options):

        # get the lookup days from args or set as default=7
        if int(options['days']) is None:
            days = 7
        else:
            days = int(options['days'])

        # Get all teachers
        teachers = Teacher.objects.all()

        # initialize the emails' data
        data = []

        for teacher in teachers:

            # Only send emails to teachers that are subscribed to the reminders
            if teacher.is_subscribed:

                # get all of the teacher's events in the coming week
                # if x.datetime > datetime.now() and x.datetime < (datetime.now() + timedelta(days=days))
                events = [x for x in teacher.events.all() if x.datetime.day == (datetime.now() + timedelta(days=days)).day]

                # if there are any events in the coming days
                if len(events) > 0:

                    html = ''
                    plain = ''

                    # generate the unsubscribe url
                    unsubscribe = str(settings.SITE_URL) + reverse('unsubscribe', kwargs={'key': teacher.emailmanager.key})
                    dashboard = str(settings.SITE_URL) + reverse('dashboard')

                    # generate single events' html and plain
                    for event in events:
                        event_link = str(settings.SITE_URL) + reverse('event-view', kwargs={'event_id': event.id})
                        html += render_to_string('main/email/teacher_event_single.html', {'event_link': event_link, 'event': event, 'date': event.datetime.strftime("%a, %d de %b às %H:%M")})
                        plain += render_to_string('main/email/teacher_event_single.txt', {'event_link': event_link, 'event': event, 'date': event.datetime.strftime("%a, %d de %b às %H:%M")})

                    # gather everything on the final email body
                    html = render_to_string('main/email/teacher_event_full.html', {'html': html, 'teacher': teacher, 'days': days, 'unsubscribe': unsubscribe, 'dashboard': dashboard})
                    plain = render_to_string('main/email/teacher_event_single.txt', {'plain': plain, 'teacher': teacher, 'days': days, 'unsubscribe': unsubscribe, 'dashboard': dashboard})

                    # append the data to a list of emails
                    data.append({'teacher': teacher, 'html': html, 'plain': plain})

        # email away
        event_warning_teachers(data)

        return 'Sent ' + str(len(data)) + ' emails successfully.'
