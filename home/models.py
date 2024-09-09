# models.py

from django.db import models

class Slider(models.Model):
    image = models.ImageField(upload_to='slider_images/')
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title
