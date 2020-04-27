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


class ExportActiveEmailsMixin:
    """
    Filters email addresses of active students/mentors and exports them in a format that can easily
    be used in CC fields of email programs.
    """
    def export_active_emails(self, request, queryset):

        meta = self.model._meta

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.txt'.format(meta)

        # TODO: fix the hacky way of filtering out students/mentors that shouldn't receive an email
        #       that's the ones currently binned via "WON'T ASSIGN" AND "UNRESPONSIVE" mentor objects
        if meta.model_name == 'mentor':  # get only active mentors
            filtered_queryset = [mentor for mentor in queryset if mentor.current_students()
                                 and mentor.name not in ("WON'T ASSIGN", "UNRESPONSIVE")]
        elif meta.model_name == 'student':  # get only students with mentors
            filtered_queryset = [student for student in queryset if student.has_mentor()
                                 and student.current_mentor.name not in ("WON'T ASSIGN", "UNRESPONSIVE")]
        else:  # no filtering if it is applied somewhere else
            filtered_queryset = queryset

        for obj in filtered_queryset:
            response.write(getattr(obj, 'email') + ',')

        return response

    export_active_emails.short_description = "Export Active Emails"


class StudentInLine(admin.TabularInline):
    model = Student
    fk_name = 'current_mentor'
    fields = ['name', 'email', 'timezone', 'daytime']
    extra = 0


# # uncomment below class (+ reference) to display editable Skill objects
# class SkillInLine(admin.StackedInline):
#     model = Person.skills.through
#     extra = 0


class StudentAdmin(admin.ModelAdmin, ExportCsvMixin, ExportActiveEmailsMixin):

    def skills_display(self, obj):
        """Displays all skills associated with current person as a clickable string.

        Skill objects are separated by commas and access the Skill object's change page.
        """
        display_text = " | ".join(skill.name for skill in obj.skills.all())
        if display_text:
            return display_text
        return "-"

    skills_display.short_description = 'Interests'

    def date_created(self, obj):
        return obj.timestamp.strftime("%b %d %Y")

    date_created.admin_order_field = 'timestamp'
    date_created.short_description = 'Date Created'

    list_display = ('name', 'email', 'skills_display', 'timezone',
                    'has_mentor', 'current_mentor', 'is_active', 'date_created')
    list_filter = ['skills', 'timezone', 'lost_job', 'timestamp']
    search_fields = ['name', 'email', 'skills__name']
    fieldsets = [
        (None, {'fields': ['name', 'email', 'info', 'current_mentor', 'lost_job']}),
        ('Interests', {'fields': ['skills']}),
        ('Time Info', {'fields': ['timezone', 'daytime', 'start_date', 'end_date']}),
    ]  # omitting field 'timestamp' (for when the form was submitted)

    actions = ["export_as_csv", "export_active_emails"]


class MentorAdmin(admin.ModelAdmin, ExportCsvMixin, ExportActiveEmailsMixin):

    def skills_display(self, obj):
        """Displays all skills associated with current person as a clickable string.

        Skill objects are separated by commas and access the Skill object's change page.
        """
        display_text = " | ".join(skill.name for skill in obj.skills.all())
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

    def date_created(self, obj):
        return obj.timestamp.strftime("%b %d %Y")

    date_created.admin_order_field = 'timestamp'
    date_created.short_description = 'Date Created'

    list_display = ('name', 'email', 'skills_display', 'timezone', 'weeks',
                    'student_display', 'capacity', 'has_capacity', 'date_created')
    list_filter = ['skills', 'timezone', 'weeks', 'timestamp']
    search_fields = ['name', 'email', 'skills__name']

    inlines = (StudentInLine, )  # SkillInLine (if wanting to add the Skills)

    fieldsets = [
        (None, {'fields': ['name', 'email', 'info']}),
        ('Mentorship', {'fields': ['students', 'weeks']}),
        ('Skills', {'fields': ['skills', 'details']}),
        ('Time Info', {'fields': ['timezone', 'daytime']}),
    ]  # omitting field 'timestamp' (for when the form was submitted)

    actions = ["export_as_csv", "export_active_emails"]


class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    readonly_fields = ('id',)
    fields = ['id', 'name']


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
                skill.name)
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

    def date_created(self, obj):
        return obj.timestamp.strftime("%b %d %Y")

    date_created.admin_order_field = 'timestamp'
    date_created.short_description = 'Date Created'

    list_display = ('is_mentor', 'name_display', 'email', 'skills_display', 'timezone', 'is_active', 'date_created')
    list_filter = ['skills', 'timezone', 'timestamp']
    search_fields = ['name', 'email', 'skills__name']

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
