from .models import Student, Mentor, Skill
from rest_framework import serializers


class StudentSerializer(serializers.HyperlinkedModelSerializer):  # ModelSerializer might fix the hardcoded stuff

    class Meta:
        model = Student
        fields = ['name', 'email', 'info', 'skills', 'timezone', 'daytime', 'timestamp',
                  'lost_job']


class MentorSerializer(serializers.HyperlinkedModelSerializer):  # ModelSerializer might fix the hardcoded stuff

    class Meta:
        model = Mentor
        fields = ['name', 'email', 'info', 'skills', 'timezone', 'daytime', 'timestamp',
                  'details', 'students', 'weeks']


class SkillSerializer(serializers.HyperlinkedModelSerializer):  # ModelSerializer might fix the hardcoded stuff

    class Meta:
        model = Skill
        fields = ['id', 'name']
