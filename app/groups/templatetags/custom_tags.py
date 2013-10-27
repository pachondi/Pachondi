
from django import template

register = template.Library()

@register.filter
def dircust(value):
    newvalue = dir(value)
    return newvalue