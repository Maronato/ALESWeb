from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.contrib import auth
from .email_helpers import confirmation_email


@property
def is_teacher(self):
    """Is Teacher
    User property to check if the user is a teacher
    """
    try:
        self.teacher.id
        return True
    except:
        return False


@property
def is_student(self):
    """Is Student
    User property to check if the user is a student
    """
    try:
        self.student.id
        return True
    except:
        return False


# Monkeypatch the properties
auth.models.User.add_to_class('is_teacher', is_teacher)
auth.models.User.add_to_class('is_student', is_student)


class Email_Manager(models.Model):
    """Email Manager
    Handles the email verification process
    Also handles the email sending process
    """

    other_email = models.EmailField(blank=True, null=True)
    active = models.BooleanField(default=False)
    key = models.CharField(max_length=40, unique=True)

    # Returns the User's active email
    @property
    def active_email(self):
        return self.user.email

    # Returns the User's obj
    @property
    def user(self):
        try:
            self.teacher.email
            return self.teacher
        except:
            self.student.email
            return self.student

    # True if the current active_email is the right one. False if there is an active verification process
    @property
    def is_active(self):
        return self.active

    def generate_key():
        """Generate Key
        Uses Django's built-in methods to generate a random key that is unique
        """
        key = get_random_string()
        try:
            Email_Manager.objects.get(key=key)
            return Email_Manager.generate_key()
        except:
            return key

    def create(user):
        """Create(Update) Email
        Check if the user has an emailmanager
        if does not, create one and return it.
        if does, return it.
        """
        try:
            user.emailmanager.key
        except:
            new = Email_Manager(
                key=Email_Manager.generate_key()
            )
            new.save()
            user.emailmanager = new
            user.save()

            # Send confirmation email
            confirmation_email(new)
        return user.emailmanager

    def confirm(key):
        """Confirms an email using key
        Confirms the email, changing the active email or activating it
        only does so if the future active email is not being used by nobody else
        """
        manager = Email_Manager.find_key(key)
        if not manager:
            # If key is wrong, return False
            return False

        if manager.is_active:
            # Does not reactivate users
            return False

        if manager.other_email:
            # If other_email
            if Email_Manager.email_used(manager.other_email):
                # Other_email already being used by someone
                return False
            # Other email is not being used by anybody else, make it the active one
            manager.user.email = manager.other_email
            manager.user.user.is_active = True
            manager.user.user.save()
            manager.user.save()
        else:
            manager.user.user.is_active = True
            manager.user.user.save()

        # Activate email
        manager.active = True
        manager.save()

        # Returns the activated User's obj
        return manager.user

    def change_email(self, email):
        """Change Email
        Allows users to change their email, gerating a key
        """
        self.active = False
        self.other_email = email
        self.key = Email_Manager.generate_key()
        self.save()
        return self.key

    def email_used(email):
        # True if user exists and is active (email taken and being used)
        try:
            user = User.objects.get(username=email)
            if not user.is_active:
                return False
            return True
        except:
            return False

    def find_key(key):
        # Returns an Email_Manager obj if a key exists, False otherwise
        try:
            return Email_Manager.objects.get(key=key)
        except:
            return False

    def __str__(self):
        return "Manager de " + self.user.user.username
