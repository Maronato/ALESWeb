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
now = timezone.now()

DAYS = (
    (1, 'Sábado'),
    (2, 'Domingo')
)


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

    day = models.IntegerField(choices=DAYS, null=True)
    time = models.TimeField(null=True)
    duration = models.TimeField(null=True)
    # frequency = models.IntegerField(choices=FREQ, null=True)


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
        return Student.objects.filter(Q(school__events__in=[self]) & Q(courses__in=[self.course]))

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
        return str(self.name) + " de " + str(self.course.name)


# Apply datetime at save
@receiver(pre_save, sender=Event, dispatch_uid="pre_save_event")
def pre_save_event(sender, instance, **kwargs):
    tz = pytz.timezone(timezone.get_default_timezone_name())
    instance.datetime = tz.localize(datetime.strptime(instance.date, "%Y-%m-%d").replace(hour=instance.time.hour, minute=instance.time.minute))
