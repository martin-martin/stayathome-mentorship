from .models import Student, Mentor
from rest_framework import serializers


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'email', 'info', 'timezone', 'timestamp', 'mentor', 'has_mentor']


class MentorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mentor
        fields = ['name', 'email', 'info', 'timezone', 'timestamp', 'weeks', 'students', 'current_students']
