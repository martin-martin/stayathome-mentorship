from django.db import models
from django.utils import timezone


class Skill(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "Technologies"

    def __str__(self):
        return self.name


# TODO: figure out how to migrate with circular imports in views and admin. drop db? how to do that in production?
class Person(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    info = models.TextField()
    notes = models.TextField(null=True, blank=True)
    skills = models.ManyToManyField('Skill', blank=True)
    timezone = models.IntegerField()
    daytime = models.CharField(max_length=10)
    start_date = models.DateTimeField(default=None, null=True, blank=True)
    end_date = models.DateTimeField(default=None, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "All Users"

    def is_active(self):
        if self.end_date:
            return timezone.now() < self.end_date
        else:
            return False

    is_active.boolean = True


# what about inheriting from a shared Person model
class Student(Person):
    class Status(models.TextChoices):
        lead = "lead", "lead"
        hot_lead = "hot-lead", "hot-lead"
        beta = "beta", "beta"
        pro_bono = "pro-bono", "pro-bono"
        student = "student", "student"
        paused = "paused", "paused"
        drop_out = "drop-out", "drop-out"
        unresponsive = "unresponsive", "unresponsive"
        retainer = "retainer", "retainer"
        alum = "alum", "alum"  # https://www.grammarly.com/blog/alumna-alumnae-alumni-alumnus/

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.student)
    lost_job = models.BooleanField(default=True)
    current_mentor = models.ForeignKey('Mentor', on_delete=models.SET_NULL, default=None, null=True, blank=True)
    completed = models.BooleanField(default=False)  # when a student has completed the 4-week free access

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
    class Status(models.TextChoices):
        retainer = "retainer", "retainer"
        active = "active", "active"
        paused = "paused", "paused"
        volunteer = "volunteer", "volunteer"
        unresponsive = "unresponsive", "unresponsive"
        alum = "alum", "alum"  # https://www.grammarly.com/blog/alumna-alumnae-alumni-alumnus/

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.volunteer)
    details = models.TextField(default=None, null=True, blank=True)
    students = models.IntegerField()  # how many they take on totally
    students_graduated = models.IntegerField(default=0)  # how many students they took through a successful mentorship
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
