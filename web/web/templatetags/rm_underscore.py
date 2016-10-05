from django import template

register = template.Library()

@register.filter
def rm_underscore(value):
    return value.replace('_', ' ')
