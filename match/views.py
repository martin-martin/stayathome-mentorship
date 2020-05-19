from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Length
from django.http import HttpResponseRedirect
from .models import Student, Mentor, Skill, Person
from rest_framework import viewsets
from rest_framework import permissions
from match.serializers import StudentSerializer, MentorSerializer, SkillSerializer
from match.forms import SelectForm, FollowUpForm


def safe_list_get(my_list, idx, default):
    """Provides a safe fallback when list index is out of range."""
    try:
        return my_list[idx]
    except IndexError:
        return default


@login_required
def browse_students(request):
    students = Student.objects.filter(current_mentor=None)
    return render(request, 'match/browse_students.html', {'students': students})


@login_required
def browse_mentors(request):
    all_mentors = Mentor.objects.all()
    mentors = [mentor for mentor in all_mentors if mentor.mentor.has_capacity()]
    return render(request, 'match/browse_mentors.html', {'mentors': mentors})


@login_required
def followup(request):
    """Shows students that didn't leave a lot of information to allow for quick follow-up emails."""
    student = None
    form = FollowUpForm()
    low_info_students = Student.objects.annotate(text_len=Length('info')).filter(text_len__lt=80)\
                                       .filter(current_mentor=None)
    if request.method == 'POST':
        form = FollowUpForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['student']
            student = Student.objects.get(pk=student_id)
    context = {"students": low_info_students, "student": student, 'form': form}
    return render(request, 'match/followup.html', context)


@login_required
def matchmaker(request):
    """Simplifies the matching process by presenting suitable combinations and quick repeatable steps."""
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
            # logic below allows for selecting different mentors if the match isn't great
            if form.cleaned_data['change_mentor'] and form.cleaned_data['change_student']:
                context = {'form': form, 'mentors': mentors, 'students': students,
                           'mentor': Person.objects.get(pk=form.cleaned_data['change_mentor']),
                           'student': Person.objects.get(pk=form.cleaned_data['change_student'])
                           }
                print(context)
            elif form.cleaned_data['change_mentor']:
                context = {'form': form, 'mentors': mentors, 'students': students,
                           'mentor': Person.objects.get(pk=form.cleaned_data['change_mentor']),
                           'student': safe_list_get(students, 0, None)
                           }
                print(context)
            elif form.cleaned_data['change_student']:
                context = {'form': form, 'mentors': mentors, 'students': students,
                           'mentor': safe_list_get(mentors, 0, None),
                           'student': Person.objects.get(pk=form.cleaned_data['change_student'])
                           }
                print(context)
            else:
                context = {'form': form, 'mentors': mentors, 'students': students,
                           'mentor': safe_list_get(mentors, 0, None),
                           'student': safe_list_get(students, 0, None)
                           }
                print(context)
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
