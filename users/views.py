from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from users.models import CustomUser


@login_required
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
