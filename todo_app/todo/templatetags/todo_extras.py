from django import template
from django.template.defaultfilters import stringfilter

from todo.models import Task

register = template.Library()


@register.filter(name="is_completed")
@stringfilter
def is_completed(status):
    return status == Task.COMPLETED