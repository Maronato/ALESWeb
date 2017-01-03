from django.db import models


class Video(models.Model):
    name = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    url = models.URLField()

    def __str__(self):
        return "Video: " + str(self.name)
