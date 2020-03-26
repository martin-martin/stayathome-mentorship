from django.contrib import admin
from .models import Student, Mentor, Skill

# Register your models here.
admin.site.register(Student)
admin.site.register(Mentor)
admin.site.register(Skill)
