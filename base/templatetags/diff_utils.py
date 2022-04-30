from datetime import timedelta

from django import template

register = template.Library()


@register.simple_tag
def calc_diff(thing_1, thing_2):
    try:
        return thing_1 - thing_2
    except TypeError:
        return timedelta()
