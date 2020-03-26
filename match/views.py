from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from .models import Student, Mentor, Skill
from rest_framework import viewsets
from rest_framework import permissions
from match.serializers import StudentSerializer, MentorSerializer, SkillSerializer


def show_mentor_form(request):
    return render(request, 'mentors.html', {'color': 'success'})


def show_student_form(request):
    return render(request, 'students.html', {'color': 'info'})


def show_success_page(request):
    return render(request, 'success.html', {'color': 'primary'})


# two public-facing POST endpoints to catch the form submissions
class AddStudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    http_method_names = ['post', 'head']

    # def create(self, request, *args, **kwargs):
    #     response = super(AddStudentViewSet, self).create(request, *args, **kwargs)
    #     return HttpResponseRedirect(reverse('success'))
    #
    # def perform_create(self, serializer):
    #     serializer.partial = True
    #     serializer.save()


class AddMentorViewSet(viewsets.ModelViewSet):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    http_method_names = ['post', 'head']

    def create(self, request, *args, **kwargs):
        response = super(AddMentorViewSet, self).create(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('success'))

    def perform_create(self, serializer):
        serializer.partial = True
        serializer.save()


# the following endpoints require authentication
class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows students to be viewed or edited.
    """
    queryset = Student.objects.all().order_by('-timestamp')
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]


class MentorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows mentors to be viewed or edited.
    """
    queryset = Mentor.objects.all().order_by('-timestamp')
    serializer_class = MentorSerializer
    permission_classes = [permissions.IsAuthenticated]


class SkillViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows skills to be viewed or edited.
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]
