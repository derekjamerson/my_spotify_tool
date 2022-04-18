from django.shortcuts import get_object_or_404, render
from users.models import CustomUser


def user_info(request, user_id=None):
    if user_id:
        display_user = get_object_or_404(CustomUser, pk=user_id)
    else:
        display_user = request.user
    return render(
        request,
        'user_info.html',
        {'display_user': display_user},
    )
