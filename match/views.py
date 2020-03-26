from copy import copy
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
    print('-----> hello there')  # runs on server reload

    # def create(self, request, *args, **kwargs):
    #     # response = super(AddStudentViewSet, self).create(request, *args, **kwargs)
    #     if request.method == 'POST':
    #         # # get keys in POST that relate to selected skills
    #         # selected_skills = dict(filter(lambda s: s[0].startswith('skill'), request.data.items()))
    #         # print(selected_skills)
    #         # # fetch skill objects from database
    #         # skill_set = []
    #         # for k, v in selected_skills.items():
    #         #     skill = Skill.objects.get(form_value=int(k[-1:]))
    #         #     skill_set.append(skill)
    #         # print(skill_set)
    #         # request_copy = copy(request)
    #         # request_copy.data['skill_set'] = skill_set
    #         # print(request_copy)
    #         print(request.POST.getlist('skills[]'))
    #         print(request.data)
    #
    #
    #
    #     return HttpResponseRedirect(reverse('success'))

    def perform_create(self, serializer):
        serializer.partial = True
        serializer.save()

    # class someview(modelviewset):   queryset = mymodel.objects.all()
    #
    # serializer_class = mymodelserializer  # want override , change post data
    # def perform_create(self, serializer):
    #     user = self.request.user.id       # form field manually entered user id
    #     # want default logged in user
    #     serializer.data['user'] = user       # returns original user entered form field
    #     print serializer.data


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
    queryset = Skill.objects.all().order_by('form_value')
    serializer_class = SkillSerializer
    print(dir(serializer_class))
    print(serializer_class.url_field_name)
    print(serializer_class.serializer_url_field)


    permission_classes = [permissions.IsAuthenticated]
