from django.db import models
from project.choices import *
from schools.models import School, Student, Year
from teachers.models import Teacher
from django.db.models import Q
from datetime import datetime, timedelta
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
import pytz
now = timezone.localtime(timezone.now())

DAYS = {
    '1': 'Sábados',
    '2': 'Domingos'
}


class Course(models.Model):
    """Course
    Model for the courses.
    """

    name = models.CharField(max_length=200)
    description = models.TextField()
    teachers = models.ManyToManyField(Teacher, related_name="courses", blank=True)
    students = models.ManyToManyField(Student, related_name="courses", blank=True)
    schools = models.ManyToManyField(School, related_name="courses", blank=True)
    years = models.ManyToManyField(Year, related_name="courses", blank=True)

    duration = models.TimeField(null=True)

    date = models.CharField(max_length=20, null=True)
    datetime = models.DateTimeField(default=datetime.strptime('1972-01-01', "%Y-%m-%d"))
    time = models.TimeField(null=True)
    weeks_apart = models.IntegerField(null=True)
    months_apart = models.IntegerField(null=True)

    @property
    def day(self):
        return self.begin.weekday() - 4

    @property
    def begin(self):
        return self.datetime.replace(tzinfo=now.tzinfo)

    @property
    def frequency(self):
        text = DAYS[str(self.day)]

        if self.time.hour < 12:
            text = text + ' de manhã'
        else:
            text = text + ' de tarde'

        if self.weeks_apart == 1 and self.months_apart == 0:
            text = text + ' semanalmente'
        elif self.weeks_apart == 0 and self.months_apart == 1:
            text = text + ' mensalmente'
        elif self.weeks_apart > 0 and self.months_apart == 0:
            text = text + ' a cada ' + str(self.weeks_apart) + ' semanas'
        elif self.weeks_apart == 0 and self.months_apart > 0:
            text = text + ' a cada ' + str(self.months_apart) + ' meses'
        elif self.weeks_apart > 0 and self.months_apart > 0:
            text = text + ' a cada ' + str(self.weeks_apart) + ' semanas e ' + str(self.months_apart) + ' meses'

        return text

    def __str__(self):
        return str(self.name)


class Event(models.Model):
    """Event
    Model for the events.
    """

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    file = models.URLField(blank=True, null=True)
    date = models.CharField(max_length=20)
    datetime = models.DateTimeField(default=datetime.strptime('1972-01-01', "%Y-%m-%d"))
    time = models.TimeField()
    duration = models.TimeField()
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='events',
        blank=True,
        null=True,
    )
    schools = models.ManyToManyField(School, related_name="events")
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='events',
        blank=True,
        null=True,
    )

    # Category may be upgraded into a model as well
    category = models.CharField(
        max_length=2,
        choices=EVENT_CHOICES,
        default='AU',
    )

    students_attended = models.ManyToManyField(Student, related_name="events_attended", blank=True)
    students_missed = models.ManyToManyField(Student, related_name="events_missed", blank=True)

    # Represents all the students that CAN attend the event. Students shown here will be notified of the event beforehand
    @property
    def students(self):
        students = Student.objects.filter(Q(school__events__in=[self]))
        if self.course:
            students = students.filter(Q(courses__in=[self.course]))
        return students

    # True if the event is in the next 2 weeks, False otherwise
    @property
    def is_near_future(self):
        return self.datetime > (now - timedelta(days=1)) and self.datetime < (now + timedelta(days=14))

    # True if the event is in the past, False otherwise
    @property
    def is_past(self):
        return self.datetime <= (now - timedelta(days=1))

    # True if the event is more than 2 weeks in the future, False otherwise
    @property
    def is_far_future(self):
        return not (self.is_near_future or self.is_past)

    def __str__(self):
        if self.course:
            return str(self.name) + " de " + str(self.course.name)
        return str(self.name)


# Apply datetime at save
@receiver(pre_save, sender=Event, dispatch_uid="pre_save_event")
def pre_save_event(sender, instance, **kwargs):
    tz = pytz.timezone(timezone.get_default_timezone_name())
    instance.datetime = tz.localize(datetime.strptime(instance.date, "%Y-%m-%d").replace(hour=instance.time.hour, minute=instance.time.minute))


@receiver(pre_save, sender=Course, dispatch_uid="pre_save_course")
def pre_save_course(sender, instance, **kwargs):
    instance.datetime = datetime.strptime(instance.date, "%Y-%m-%d").replace(hour=instance.time.hour, minute=instance.time.minute, tzinfo=now.tzinfo)
