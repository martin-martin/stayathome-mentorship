from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    info = models.TextField()
    job = models.BooleanField(default=True)
    flattening = models.BooleanField(default=True)
    skills = models.ManyToManyField('Skills')
    timezone = models.IntegerField()
    daytime = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    mentor = models.ForeignKey('Mentor', on_delete=models.SET_NULL, default=None, null=True, blank=True)
    has_mentor = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Mentor(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    info = models.TextField()
    skills = models.ManyToManyField('Skills')
    details = models.TextField()
    students = models.IntegerField()
    weeks = models.IntegerField()
    timezone = models.IntegerField()
    daytime = models.CharField(max_length=10)
    current_students = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def has_capacity(self):
        return self.current_students < self.students

    def __str__(self):
        return self.name


class Skills(models.Model):
    type = models.CharField(max_length=20)

    def __str__(self):
        return self.type
