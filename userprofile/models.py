from django.db import models
from django.conf import settings


class Teacher(models.Model):
    profile_img = models.ImageField(upload_to='profile_images/', blank=True, null=True)  # Profile image
    cover_image = models.ImageField(upload_to='cover_images/', blank=True, null=True)  # Cover image
    major_subject = models.CharField(max_length=100)  # Major subject taught by the teacher
    is_teacher = models.BooleanField(default=False)  # Flag to indicate if user is a teacher
    description = models.TextField(default='No description provided')  # Description of the teacher
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Links to Django's User model

    def __str__(self):
        return f"Teacher {self.id}"
