from django.db import models
from project.choices import *
from schools.models import School, Student, Year
from teachers.models import Teacher
from django.db.models import Q
from datetime import datetime, timedelta


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
    stundets_missed = models.ManyToManyField(Student, related_name="events_missed", blank=True)

    # Represents all the students that CAN attend the event. Students shown here will be notified of the event beforehand
    @property
    def students(self):
        return Student.objects.filter(Q(school__events__in=[self]) & Q(courses__in=[self.course]))

    # Merges self.time and self.date into a datetime object
    # Returns an invalid date if the merging failed(invalid initial data)
    @property
    def datetime(self):
        try:
            return datetime.strptime(self.date, "%Y-%m-%d").replace(hour=self.time.hour, minute=self.time.minute)
        except ValueError:
            return datetime.strptime('1972-01-01', "%Y-%m-%d")

    # True if the event is in the next 2 weeks, False otherwise
    @property
    def is_near_future(self):
        return self.datetime > (datetime.now() - timedelta(days=1)) and self.datetime < (datetime.now() + timedelta(days=14))

    # True if the event is in the past, False otherwise
    @property
    def is_past(self):
        return self.datetime <= (datetime.now() - timedelta(days=1))

    # True if the event is more than 2 weeks in the future, False otherwise
    @property
    def is_far_future(self):
        return not (self.is_near_future or self.is_past)

    def __str__(self):
        return str(self.name) + " de " + str(self.course.name)
