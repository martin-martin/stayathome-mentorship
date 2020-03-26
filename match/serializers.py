from .models import Student, Mentor, Skill
from rest_framework import serializers


class StudentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Student
        fields = ['name', 'email', 'info', 'skill_set', 'timezone', 'daytime', 'timestamp',
                  'lost_job']


class MentorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Mentor
        fields = ['name', 'email', 'info', 'skill_set', 'timezone', 'daytime', 'timestamp',
                  'details', 'students', 'weeks']


class SkillSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Skill
        fields = ['form_value', 'type']
