from .models import Student, Mentor, Skill
from rest_framework import serializers

class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ['form_value', 'type']
        extra_kwargs = {'url': {'view_name': 'rest_framework:skill-detail', 'lookup_field': 'form_value'}}


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ['name', 'email', 'info', 'skills', 'timezone', 'daytime', 'timestamp',
                  'lost_job']


class MentorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mentor
        fields = ['name', 'email', 'info', 'skills', 'timezone', 'daytime', 'timestamp',
                  'details', 'students', 'weeks']


