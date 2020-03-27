from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    info = models.TextField()
    skills = models.ManyToManyField('Skill', null=True, blank=True)
    timezone = models.IntegerField()
    daytime = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)


# what about inheriting from a shared Person model
class Student(Person):
    lost_job = models.BooleanField(default=True)
    current_mentor = models.ForeignKey('Mentor', on_delete=models.SET_NULL, default=None, null=True, blank=True)

    def has_mentor(self):
        if self.current_mentor:
            return True
        else:
            return False

    has_mentor.admin_order_field = '-timestamp'
    has_mentor.boolean = True
    has_mentor.short_description = 'Has mentor?'

    def __str__(self):
        return self.name


class Mentor(Person):
    details = models.TextField(default=None, null=True, blank=True)
    students = models.IntegerField()
    weeks = models.IntegerField()

    def has_capacity(self):
        return self.current_students() < self.students

    def current_students(self):
        """How many students are currently assigned to this mentor."""
        return len(self.student_set.all())

    def capacity(self):
        """How many students can this mentor still take on?"""
        return self.students - self.current_students()

    has_capacity.admin_order_field = '-timestamp'
    has_capacity.boolean = True
    has_capacity.short_description = 'Has capacity?'

    def __str__(self):
        return self.name


class Skill(models.Model):
    form_value = models.IntegerField()
    type = models.CharField(max_length=20)

    def __str__(self):
        return self.type
