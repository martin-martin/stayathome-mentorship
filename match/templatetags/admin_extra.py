from django import template
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
    return len(Student.objects.filter(current_mentor=None))


@register.simple_tag
def count_leftover_capacity():
    return sum([mentor.capacity() for mentor in Mentor.objects.all()])
