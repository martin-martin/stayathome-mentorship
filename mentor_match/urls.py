"""mentor_match URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from match import views


router = routers.DefaultRouter()
router.register(r'students', views.StudentViewSet)
router.register(r'mentors', views.MentorViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('apply/mentor', views.show_mentor_form, name='mentor'),
    path('apply/student', views.show_student_form, name='student'),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('add-student/', views.StudentCreateView.as_view(), name='add_student'),
    path('add-mentor/', views.MentorCreateView.as_view(), name='add_mentor'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

