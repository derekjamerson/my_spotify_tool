from django import template

register = template.Library()


@register.simple_tag
def display_timedelta(delta):
    days = delta.days
    hours, remain_from_hours = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remain_from_hours, 60)
    day_string = ''
    if days:
        day_string += f'{days} days,'
    time_string = ':'.join(
        [str(hours).zfill(2), str(minutes).zfill(2), str(seconds).zfill(2)]
    )
    return ' '.join([day_string, time_string])


@register.simple_tag
def display_timedelta_only_mins(delta):
    _, remain = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remain, 60)
    return ':'.join([str(minutes).zfill(2), str(seconds).zfill(2)])
