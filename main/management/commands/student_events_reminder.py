from django.core.management.base import BaseCommand
from schools.models import Student
from datetime import datetime, timedelta
from main.email_helpers import event_warning_students
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
import locale
locale.setlocale(locale.LC_TIME, "pt_BR")


class Command(BaseCommand):
    help = 'Send email to students about future events'

    # Checks each students' events and creates an email with all the future events' infos

    def add_arguments(self, parser):
        parser.add_argument('days', )

    def handle(self, *args, **options):

        # get the lookup days from args or set as default=7
        if int(options['days']) is None:
            days = 7
        else:
            days = int(options['days'])

        # Get all students
        students = Student.objects.all()

        # initialize the emails' data
        data = []

        for student in students:

            # Only send emails to students that are subscribed to the reminders
            if student.is_subscribed:

                # get all of the student's events in the coming week
                # if x.datetime > datetime.now() and x.datetime < (datetime.now() + timedelta(days=days))
                events = [x for x in student.events if x.datetime.day == (datetime.now() + timedelta(days=days)).day]

                # if there are any events in the coming week
                if len(events) > 0:

                    html = ''
                    plain = ''

                    # generate the unsubscribe url
                    unsubscribe = str(settings.SITE_URL) + reverse('unsubscribe', kwargs={'key': student.emailmanager.key})
                    dashboard = str(settings.SITE_URL) + reverse('dashboard')

                    # generate single events' html and plain
                    for event in events:
                        event_link = str(settings.SITE_URL) + reverse('event-view', kwargs={'event_id': event.id})
                        html += render_to_string('main/email/student_event_single.html', {'event_link': event_link, 'event': event, 'date': event.datetime.strftime("%a, %d de %b às %H:%M")})
                        plain += render_to_string('main/email/student_event_single.txt', {'event_link': event_link, 'event': event, 'date': event.datetime.strftime("%a, %d de %b às %H:%M")})

                    # gather everything on the final email body
                    html = render_to_string('main/email/student_event_full.html', {'html': html, 'student': student, 'days': days, 'unsubscribe': unsubscribe, 'dashboard': dashboard})
                    plain = render_to_string('main/email/student_event_single.txt', {'txt': plain, 'student': student, 'days': days, 'unsubscribe': unsubscribe, 'dashboard': dashboard})

                    # append the data to a list of emails
                    data.append({'student': student, 'html': html, 'plain': plain})

        # email away
        event_warning_students(data)

        return 'Sent ' + str(len(data)) + ' emails successfully.'
