from django.db import models
from project.choices import *
from schools.models import City, Student, Year
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
    city = models.ForeignKey(City, related_name="courses", null=True)
    years = models.ManyToManyField(Year, related_name="courses", blank=True)
    limit = models.IntegerField(null=True)

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
        return self.datetime

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

    @property
    def spots_left(self):
        return self.limit - len(self.students.all())

    @property
    def has_spots(self):
        return self.spots_left > 0

    @property
    def next_event(self):
        from .date_comparisons import AllEvents
        for event in AllEvents(course=self).generate():
            if event >= now:
                return event

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
    city = models.ForeignKey(City, related_name="events", null=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='events',
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

        students = Student.objects.filter(school__city=self.city)
        if self.course:
            students = students.filter(Q(courses__in=[self.course]))
        return students

    @property
    def end(self):
        time = datetime(hour=self.time.hour, minute=self.time.minute, year=now.year, month=1, day=1) + timedelta(hours=self.duration.hour, minutes=self.duration.minute)
        res = self.datetime
        return res.replace(hour=time.hour, minute=time.minute)

    # True if the event is in the past, False otherwise
    @property
    def is_past(self):
        return now >= self.end

    # True if the event is in the next 2 weeks, False otherwise
    @property
    def is_near_future(self):
        return not self.is_past and self.datetime < (now + timedelta(days=14))

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
    instance.city = instance.course.city if instance.course.city else None


@receiver(pre_save, sender=Course, dispatch_uid="pre_save_course")
def pre_save_course(sender, instance, **kwargs):
    instance.datetime = datetime.strptime(instance.date, "%Y-%m-%d").replace(hour=instance.time.hour, minute=instance.time.minute, tzinfo=now.tzinfo)
