import csv
from django.http import HttpResponse
from django.shortcuts import reverse
from django.utils.safestring import mark_safe
from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Student, Mentor, Skill, Person


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected to CSV"


class StudentInLine(admin.TabularInline):
    model = Student
    fk_name = 'current_mentor'
    fields = ['name', 'email', 'timezone', 'daytime']
    extra = 0


# # uncomment below class (+ reference) to display editable Skill objects
# class SkillInLine(admin.StackedInline):
#     model = Person.skills.through
#     extra = 0


class StudentAdmin(admin.ModelAdmin, ExportCsvMixin):

    def skills_display(self, obj):
        """Displays all skills associated with current person as a clickable string.

        Skill objects are separated by commas and access the Skill object's change page.
        """
        display_text = " | ".join(skill.type for skill in obj.skills.all())
        if display_text:
            return display_text
        return "-"

    skills_display.short_description = 'Interests'

    list_display = ('name', 'email', 'skills_display', 'timezone', 'has_mentor', 'current_mentor', 'is_active')
    list_filter = ['skills', 'timezone', 'lost_job', 'timestamp']
    search_fields = ['name', 'email', 'skills']
    fieldsets = [
        (None, {'fields': ['name', 'email', 'info', 'current_mentor']}),
        ('Interests', {'fields': ['skills']}),
        ('Time Info', {'fields': ['timezone', 'daytime', 'start_date', 'end_date']}),
    ]  # omitting field 'timestamp' (for when the form was submitted) and 'lost_job'

    actions = ["export_as_csv"]


class MentorAdmin(admin.ModelAdmin, ExportCsvMixin):

    def skills_display(self, obj):
        """Displays all skills associated with current person as a clickable string.

        Skill objects are separated by commas and access the Skill object's change page.
        """
        display_text = " | ".join(skill.type for skill in obj.skills.all())
        if display_text:
            return display_text
        return "-"

    skills_display.short_description = 'Skills'

    def student_display(self, obj):
        """Displays all students associated with current mentor as a clickable string.

        Student objects are separated by commas and access the Student object's change page.
        """
        display_text = ", ".join([
            "<a href={}>{}</a>".format(
                    reverse('admin:{}_{}_change'.format(obj._meta.app_label, Student._meta.model_name),
                    args=(student.pk,)),
                student.name)
             for student in obj.student_set.all()
        ])
        if display_text:
            return mark_safe(display_text)
        return "-"

    student_display.short_description = "Students"

    list_display = ('name', 'email', 'skills_display', 'timezone', 'weeks', 'student_display', 'capacity', 'has_capacity')
    list_filter = ['skills', 'timezone', 'weeks', 'timestamp']
    search_fields = ['name', 'email', 'skills']

    inlines = (StudentInLine, )  # SkillInLine (if wanting to add the Skills)

    fieldsets = [
        (None, {'fields': ['name', 'email', 'info']}),
        ('Mentorship', {'fields': ['students', 'weeks']}),
        ('Skills', {'fields': ['skills', 'details']}),
        ('Time Info', {'fields': ['timezone', 'daytime']}),
    ]  # omitting field 'timestamp' (for when the form was submitted)

    actions = ["export_as_csv"]


class SkillAdmin(admin.ModelAdmin):
    list_display = ('type', 'form_value')


class PersonAdmin(admin.ModelAdmin, ExportCsvMixin):
    """The PersonAdmin allows to view Mentors and Students in one shared table.

    This gives the opportunity to filter by shared skills etc. and aids to find matches.
    """
    def skills_display(self, obj):
        """Displays all skills associated with current person as a clickable string.

        Skill objects are separated by commas and access the Skill object's change page.
        """
        display_text = " | ".join([
            "<a href={}>{}</a>".format(
                    reverse('admin:{}_{}_change'.format(obj._meta.app_label, Skill._meta.model_name),
                    args=(skill.pk,)),
                skill.type)
             for skill in obj.skills.all()
        ])
        if display_text:
            return mark_safe(display_text)
        return "-"

    def name_display(self, obj):
        """Displays Student or Mentor object associated with current person as a clickable string.

        NOTE: Relies on every Person being either a Student or a Mentor. Returns a string if neither applies.
        TODO: Refactor to improve.
        """
        try:
            display_text = "<a href={}>{}</a>".format(
                        reverse('admin:{}_{}_change'.format(obj._meta.app_label, Mentor._meta.model_name),
                                args=(obj.mentor.pk,)),
                        obj.mentor.name
            )
            if display_text:
                return mark_safe(display_text)
            return "-"
        # except obj.mentor.RelatedObjectDoesNotExist as e:
        except Exception as e:  # it's a RelatedObjectDoesNotExist, but somehow doesn't catch when using above
            try:
                display_text = "<a href={}>{}</a>".format(
                            reverse('admin:{}_{}_change'.format(obj._meta.app_label, Student._meta.model_name),
                                    args=(obj.student.pk,)),
                            obj.student.name
                )
                if display_text:
                    return mark_safe(display_text)
                return "-"
            except:
                return "* no object *"

    name_display.short_description = 'Name'

    def is_mentor(self, obj):
        """Creates a boolean response on whether a Person object is linked to a Mentor object or not."""
        try:
            mentor = obj.mentor
            return True
        except:
            return False

    is_mentor.boolean = True  # display as a symbol
    is_mentor.short_description = 'Mentor?'

    list_display = ('is_mentor', 'name_display', 'email', 'skills_display', 'timezone', 'is_active')
    list_filter = ['skills', 'timezone', 'timestamp']
    search_fields = ['name', 'email', 'skills']

    fieldsets = [
        (None, {'fields': ['name', 'email', 'info']}),
        ('Skills', {'fields': ['skills']}),
        ('Time Info', {'fields': ['timezone', 'daytime', 'start_date', 'end_date']}),
    ]  # omitting field 'timestamp' (for when the form was submitted)

    actions = ["export_as_csv"]


# Remove default models we don't use
admin.site.unregister(User)
admin.site.unregister(Group)
# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Mentor, MentorAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Person, PersonAdmin)
