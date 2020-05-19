from django import template
from django.db.models import Q
from match.models import Mentor, Student

register = template.Library()


@register.simple_tag
def count_mentors():
    return len(Mentor.objects.all())


@register.simple_tag
def count_students():
    return len(Student.objects.all())


@register.simple_tag
def count_total_capacity():
    return sum([mentor.students for mentor in Mentor.objects.all()])


@register.simple_tag
def count_unassigned_students():
    return len(Student.objects.filter(current_mentor=None)\
                              .exclude(Q(status='drop-out') | Q(status='unresponsive') | Q(status='retainer')
                                       | Q(status='alum') | Q(status='paused')))


@register.simple_tag
def count_leftover_capacity():
    return sum([mentor.capacity() for mentor in Mentor.objects.all()])
