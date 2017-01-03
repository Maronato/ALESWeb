from django.db import models
from teachers.models import Teacher

# Create your models here.


class Post(models.Model):
    name = models.CharField(max_length=200)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        Teacher,
        related_name='posts',
    )
