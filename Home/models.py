from django.db import models

class RegisterUser(models.Model):
    name = models.CharField(max_length=250)
    userName = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.name + '-' + self.userName + '-' + self.email + '-' + self.password

class Workshop(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    SDate = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    fee = models.CharField(max_length=250)
    venue = models.TextField()
    instructor = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default=None, blank=True)
    report = models.PositiveIntegerField(default=None, blank=True)

    def __str__(self):
        return self.title + '-' + self.description + '-' + self.SDate + '-' + self.time + '-' + self.duration + '-' + self.fee
        + '-' + self.venue + '-' + self.instructor

    def __int__(self):
        return self.report

class ShortCourse(models.Model):
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=5000)
    SDate = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    fee = models.CharField(max_length=250)
    venue = models.CharField(max_length=1000)
    instructor = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default=None, blank=True)
    report = models.PositiveIntegerField(default=None, blank=True)

    def __str__(self):
        return self.title + '-' + self.description + '-' + self.SDate + '-' + self.time + '-' + self.duration + '-' + self.fee
        + '-' + self.venue + '-' + self.instructor

    def __int__(self):
        return self.report


class SurveyPost(models.Model):
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=5000)
    link = models.URLField(max_length=500)
    status = models.CharField(max_length=50, default=None, blank=True)

    def __str__(self):
        return self.title + '-' + self.description + '-' + self.link

class News(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    link = models.URLField(max_length=500)

    def __str__(self):
        return self.title + '-' + self.description + '-' + self.link

class Feedback(models.Model):
    name = models.CharField(max_length=250)
    comment = models.TextField(blank=True)
    eventType = models.CharField(max_length=50, blank=True)
    eventId = models.PositiveIntegerField(default=None, blank=True)

    def __str__(self):
        return self.name + '-' + self.comment + '-' + self.eventType
    def __int__(self):
        return self.eventId



