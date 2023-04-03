from django import template

register = template.Library()

@register.filter
def with_index(iterable, start=0):
    return enumerate(iterable, start)
