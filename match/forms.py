from django import forms
from .models import Skill, Person


class SelectForm(forms.Form):
    SKILLS = [(skill.id, skill.name) for skill in Skill.objects.all()]
    TIMEZONES = [(tz, "UTC{}".format(tz)) for tz in range(-12, 13)]
    skill = forms.ChoiceField(choices=SKILLS)
    timezone = forms.ChoiceField(choices=TIMEZONES)
