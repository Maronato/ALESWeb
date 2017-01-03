from django.db import models

# Create your models here.


class Article(models.Model):
    name = models.CharField(max_length=200)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=200)
    url = models.URLField()
