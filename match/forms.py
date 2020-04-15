from django import forms
from .models import Skill, Mentor, Student


class SelectForm(forms.Form):
    SKILLS = [(skill.id, skill.name) for skill in Skill.objects.all()]
    TIMEZONES = [(tz, "UTC{}".format(tz)) for tz in range(-12, 13)]
    MENTORS = [(mentor.id, mentor.name) for mentor in Mentor.objects.all() if mentor.has_capacity()]
    MENTORS.insert(0, (None, '----'))
    STUDENTS = [(student.id, student.name) for student in Student.objects.all() if not student.current_mentor]
    STUDENTS.insert(0, (None, '----'))
    skill = forms.ChoiceField(choices=SKILLS)
    timezone = forms.ChoiceField(choices=TIMEZONES)
    change_mentor = forms.ChoiceField(choices=MENTORS, required=False)
    change_student = forms.ChoiceField(choices=STUDENTS, required=False)
