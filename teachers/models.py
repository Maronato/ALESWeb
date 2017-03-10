from django.db import models
from schools.models import School
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from main.models import Email_Manager
from django.utils.crypto import get_random_string


class Teacher(models.Model):
    """Teacher
    Model for the teachers.
    """

    user = models.OneToOneField(
        User,
        blank=True,
        null=True
    )
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    nickname = models.CharField(max_length=30, unique=False)
    email = models.EmailField(unique=True)
    emailmanager = models.OneToOneField(Email_Manager, null=True)
    is_subscribed = models.BooleanField(default=True)
    phone = models.CharField(max_length=20, unique=True)
    schools = models.ManyToManyField(School, related_name="teachers")

    # Method that updates the teacher, used when updated through the admin page
    def update_teacher(self):
        try:
            self.user.id
            self.user.username = self.email
            self.user.email = self.email
            self.user.save()
        except:
            user = User.objects.create_user(self.email, self.email, get_random_string())
            user.teacher = self
            user.is_active = False
            user.save()
        return self.user

    def __str__(self):
        return str(self.name)


# Apply teacher changes
@receiver(post_save, sender=Teacher, dispatch_uid="post_save_teacher")
def post_save_teacher(sender, instance, **kwargs):
    instance.update_teacher()
    Email_Manager.create(instance)


# Delete EmailManager and User if Teacher is deleted
@receiver(post_delete, sender=Teacher, dispatch_uid="delete_teacher")
def delete_teacher(sender, instance, **kwargs):
    instance.emailmanager.delete()
    instance.user.delete()
