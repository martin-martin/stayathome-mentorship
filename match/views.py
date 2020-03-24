from django.shortcuts import render
from .models import Student, Mentor
from rest_framework import viewsets, generics
from rest_framework import permissions
from match.serializers import StudentSerializer, MentorSerializer


def show_mentor_form(request):
    return render(request, 'mentors.html', {'color': 'success'})


def show_student_form(request):
    return render(request, 'students.html', {'color': 'info'})


# two public-facing POST endpoints to catch the form submissions
class StudentCreateView(generics.CreateAPIView):
    """Public POST API-endpoint that creates a new Student entry."""
    serializer_class = StudentSerializer


class MentorCreateView(generics.CreateAPIView):
    """Public POST API-endpoint that creates a new Mentor entry."""
    serializer_class = MentorSerializer


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
