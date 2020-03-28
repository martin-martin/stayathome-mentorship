from django.contrib import admin
from .models import Student, Mentor, Skill #, Person


class StudentInLine(admin.TabularInline):
    model = Student
    fk_name = 'current_mentor'
    fields = ['name', 'email', 'timezone', 'daytime']
    extra = 0


# # uncomment below class (+ reference) to display editable Skill objects
# class SkillInLine(admin.StackedInline):
#     model = Person.skills.through
#     extra = 0


class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'timezone', 'has_mentor', 'is_active')
    list_filter = ['timezone', 'lost_job', 'timestamp', 'skills']
    search_fields = ['name', 'email', 'skills']
    fieldsets = [
        (None, {'fields': ['name', 'email', 'info', 'current_mentor']}),
        ('Interests', {'fields': ['skills']}),
        ('Time Info', {'fields': ['timezone', 'daytime', 'start_date', 'end_date']}),
    ]  # omitting field 'timestamp' (for when the form was submitted) and 'lost_job'


class MentorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'timezone', 'weeks', 'capacity', 'has_capacity')
    list_filter = ['timezone', 'weeks', 'timestamp', 'skills']
    search_fields = ['name', 'email', 'skills']

    inlines = (StudentInLine, )  # SkillInLine (if wanting to add the Skills)

    fieldsets = [
        (None, {'fields': ['name', 'email', 'info']}),
        ('Mentorship', {'fields': ['students', 'weeks']}),
        ('Skills', {'fields': ['skills', 'details']}),
        ('Time Info', {'fields': ['timezone', 'daytime']}),
    ]  # omitting field 'timestamp' (for when the form was submitted)


class SkillAdmin(admin.ModelAdmin):
    list_display = ('type', 'form_value')


# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Mentor, MentorAdmin)
admin.site.register(Skill, SkillAdmin)
