
# videos/models.py
# In videos/models.py
from django.db import models
from django.conf import settings
from userprofile.models import Teacher  # Replace 'your_app' with the name of your app


class Faculty(models.Model):
    faculty_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.faculty_name

class Level(models.Model):
    level_name = models.CharField(max_length=255)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.level_name

class Subject(models.Model):
    subject_name = models.CharField(max_length=255)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    price = models.IntegerField(default='0')
    discount = models.IntegerField(default='100') 
    offer_time = models.IntegerField(default = '365')  # Default to one year from now
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)  # ForeignKey to Teacher


    def __str__(self):
        return self.subject_name

class Video(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    chapter_number = models.IntegerField()
    video_name = models.CharField(max_length=255)
    video = models.FileField(upload_to='videos/')
    thumbnil = models.ImageField(upload_to='thumbnils/', blank=True, null=True)  # Make sure this field is named correctly
    description = models.TextField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)  # ForeignKey to Teacher



    def __str__(self):
        return self.video_name
