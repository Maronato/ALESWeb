from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from main.models import Email_Manager
from django.utils.crypto import get_random_string
from custom_auth.models import FacebookUser


DOCUMENT_TYPE = (
    ('RG', 'RG'),
    ('CPF', 'CPF'),
    ('RA', 'RA')
)


class City(models.Model):
    """City
    Model for the cities.
    """

    name = models.CharField(max_length=100)
    short = models.CharField(max_length=2, unique=True)

    verbose_name = "Cidade"

    def __str__(self):
        return str(self.name)


class School(models.Model):
    """School
    Model for the schools.
    """

    name = models.CharField(max_length=200)
    short = models.CharField(max_length=2, unique=True)
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="schools",
    )

    def __str__(self):
        return str(self.name)


class Year(models.Model):
    """Year
    Model for the years.
    """

    name = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)


class Student(models.Model):
    """Student
    Model for the students.
    """

    user = models.OneToOneField(
        User,
        blank=True,
        null=True
    )
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    born = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    document = models.CharField(max_length=20, null=True, blank=True)
    document_type = models.CharField(choices=DOCUMENT_TYPE, max_length=5, default='RG')
    emailmanager = models.OneToOneField(Email_Manager, null=True)
    is_subscribed = models.BooleanField(default=True)
    phone = models.CharField(max_length=20, unique=False)
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='students',
    )
    year = models.ForeignKey(
        Year,
        on_delete=models.CASCADE,
        related_name='students',
    )

    is_authorized = models.BooleanField(default=False, blank=True)

    # Facebook stuff
    has_facebook = models.BooleanField(default=False, blank=True)
    facebook_create_url = models.CharField(max_length=20, blank=True)
    facebookuser = models.OneToOneField(
        FacebookUser,
        blank=True,
        null=True
    )

    # Returns the events that the student should attend(only in the near future)
    @property
    def events(self):
        from courses.models import Event
        return [event for event in Event.objects.all() if self in event.students and event.is_near_future]

    # Method that updates the student, used when updated through the admin page
    def update_student(self):
        try:
            self.user.id
            self.user.username = self.email.lower()
            self.user.email = self.email.lower()
            self.user.save()
        except:
            user = User.objects.create_user(self.email.lower(), self.email.lower(), get_random_string())
            user.student = self
            user.is_active = False
            user.save()
        return self.user

    def __str__(self):
        return str(self.name)


# Apply student changes
@receiver(post_save, sender=Student, dispatch_uid="post_save_student")
def post_save_student(sender, instance, **kwargs):
    instance.update_student()
    Email_Manager.create(instance)


# Delete EmailManager and User if Student is deleted
@receiver(post_delete, sender=Student, dispatch_uid="delete_student")
def delete_student(sender, instance, **kwargs):
    instance.emailmanager.delete()
    instance.user.delete()
