from datetime import timedelta

from django import template

register = template.Library()


@register.simple_tag
def calc_diff(thing_1, thing_2):
    return thing_1 - thing_2
