from django.db import models


class Album(models.Model):
    name = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Album: " + str(self.name)


class Picture(models.Model):
    album = models.ForeignKey(
        'Album',
        on_delete=models.CASCADE,
    )
    url = models.URLField(max_length=200)

    def __str__(self):
        return "Picture: " + str(self.id) + " from " + str(self.album.name)
