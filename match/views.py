from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Student, Mentor, Skill, Person
from rest_framework import viewsets
from rest_framework import permissions
from match.serializers import StudentSerializer, MentorSerializer, SkillSerializer
from match.forms import SelectForm


def matchmaker(request):
    """Simplifies the matching process by presenting suitable combinations and quick repaeatable steps."""
    if request.method == 'POST':
        form = SelectForm(request.POST)
        if form.is_valid():
            # filter all candidates that are in similar timezones +/- 1 of their timezone
            time_match = Person.objects.filter(timezone__gte=int(form.cleaned_data['timezone'])-1)\
                                       .filter(timezone__lte=int(form.cleaned_data['timezone'])+1)
            # filter all candidates that have the selected skill among their skills
            candidates = time_match.filter(skills__in=form.cleaned_data['skill'])
            # --- GET MENTORS ---
            all_mentors = candidates.filter(mentor__isnull=False)
            # keep only mentors that have capacity to take students
            mentors = [mentor for mentor in all_mentors if mentor.mentor.has_capacity()]
            # --- GET STUDENTS ---
            all_students = candidates.filter(mentor__isnull=True)
            # keep only students that don't currently have a mentor assigned to them
            students = [student for student in all_students if not student.student.current_mentor]
            """TODO:
            ========
            - button to click "next" for another match?
            """
            context = {'form': form, 'mentors': mentors, 'students': students}
            return render(request, 'match/match.html', context)
    form = SelectForm()
    context = {'form': form}
    return render(request, 'match/match.html', context)


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

    def create(self, request, *args, **kwargs):
        response = super(AddStudentViewSet, self).create(request, *args, **kwargs)
        return HttpResponseRedirect("https://codingnomads.github.io/stayathome-mentorship/success.html")

    def perform_create(self, serializer):
        serializer.partial = True
        serializer.save()


class AddMentorViewSet(viewsets.ModelViewSet):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    http_method_names = ['post', 'head']

    def create(self, request, *args, **kwargs):
        response = super(AddMentorViewSet, self).create(request, *args, **kwargs)
        return HttpResponseRedirect("https://codingnomads.github.io/stayathome-mentorship/success.html")

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
    queryset = Skill.objects.all().order_by('id')
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]
