from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from match import views


# customize admin text
admin.site.site_header = "🏠 CodingNomads Admin"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "#StayAt🏠 Mentorship Admin"

router = routers.DefaultRouter()
router.register(r'students', views.StudentViewSet, basename='students')
router.register(r'mentors', views.MentorViewSet, basename='mentors')
router.register(r'skills', views.SkillViewSet)
router.register(r'add-student', views.AddStudentViewSet)
router.register(r'add-mentor', views.AddMentorViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('match', views.matchmaker, name='match'),
    # path('apply/mentor', views.show_mentor_form, name='mentor'),
    # path('apply/student', views.show_student_form, name='student'),
    # path('success/', views.show_success_page, name='success'),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    # path('add-student/', views.StudentCreateView.as_view(), name='add_student'),
    # path('add-mentor/', views.MentorCreateView.as_view(), name='add_mentor'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

