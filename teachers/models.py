from django.db import models
from schools.models import City
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from main.models import Email_Manager
from django.utils.crypto import get_random_string

from custom_auth.models import FacebookUser


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
    cities = models.ManyToManyField(City, related_name="teachers")

    # Facebook stuff
    has_facebook = models.BooleanField(default=False, blank=True)
    facebook_create_url = models.CharField(max_length=20, blank=True)
    facebookuser = models.OneToOneField(
        FacebookUser,
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING
    )

    # Method that updates the teacher, used when updated through the admin page
    def update_teacher(self):
        try:
            self.user.id
            self.user.username = self.email.lower()
            self.user.email = self.email.lower()
            self.user.save()
        except:
            user = User.objects.create_user(self.email.lower(), self.email.lower(), get_random_string())
            user.teacher = self
            user.is_active = False
            user.save()
        return self.user

    def __str__(self):
        return str(self.name)

    @property
    def schools(self):
        res = self.cities.all()[0].schools.all()
        for city in self.cities.all()[1:]:
            res = res | city.schools.all()
        return res.order_by('name')


class EmailList(models.Model):

    COLORS = (
        ('#7c8cff', 'Azul'),
        ('#03A9F4', 'Azul Claro'),
        ('#2196F3', 'Outro Azul'),
        ('#ff2323', 'Vermelho'),
        ('#E91E63', 'Rosa'),
        ('#4CAF50', 'Verde'),
        ('#009688', 'Teal'),
        ('#FFEB3B', 'Amarelo'),
        ('#FF9800', 'Laranja'),
        ('#795548', 'Marrom'),
        ('#607D8B', 'Cinza'),
    )

    GREETINGS = (
        ('Love', 'Love'),
        ('Atenciosamente', 'Atenciosamente'),
        ('Cordialmente', 'Cordialmente'),
        ('Saudações', 'Saudações'),
        ('Regards', 'Regards'),
        ('Yours truly', 'Yours truly'),
        ('Sincerely', 'Sincerely'),
        ('Abraço', 'Abraço'),
        ('Obrigado', 'Obrigado'),
        ('Obrigada', 'Obrigada'),
        ('Obrigadx', 'Obrigadx'),
        ('Beijos', 'Beijos'),
        ('XOXO', 'XOXO'),
        ('Vida longa e próspera', 'Vida longa e próspera')
    )

    from courses.models import Course

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='email_lists',
        null=True
    )

    created = models.DateTimeField(auto_now_add=True)
    sent = models.DateTimeField(default=None, null=True)

    theme = models.CharField(choices=COLORS, default='#7c8cff', max_length=7)
    greeting = models.CharField(choices=GREETINGS, default='Love', max_length=25)

    courses = models.ManyToManyField(Course, blank=True)

    subject = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    message = models.TextField()
    html = models.BooleanField(default=False)

    is_conversation = models.BooleanField(default=True)
    to_all = models.BooleanField(default=False)

    sent_amount = models.IntegerField(default=0)

    @property
    def students(self):
        from schools.models import Student
        return Student.objects.filter(courses__in=self.courses.all()).distinct() if not self.to_all else Student.objects.all()

    @property
    def total_to_be_sent(self):
        if self.to_all:
            from schools.models import Student
            return len(Student.objects.all())
        else:
            counter = 0
            for student in self.students:
                counter += len(student.courses.filter(id__in=[x.id for x in self.courses.all()]))
            return counter

    @property
    def last_sent_total(self):
        if self.total_to_be_sent > self.sent_amount:
            return self.sent_amount
        else:
            self.sent_amount = 0
            self.save()


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
