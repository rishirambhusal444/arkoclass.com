from django.db import models

class Faculty(models.Model):
    faculty_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.faculty_name

class Level(models.Model):
    level_name = models.CharField(max_length=255)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.level_name

class Subject(models.Model):     'price','discount','offer_time',
    subject_name = models.CharField(max_length=255)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)


    def __str__(self):
        return self.subject_name

class Video(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    chapter_number = models.IntegerField()
    video_name = models.CharField(max_length=255)
    video = models.FileField(upload_to='videos/')
    description = models.TextField()

    def __str__(self):
        return self.video_name
