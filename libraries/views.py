from django.shortcuts import get_object_or_404, render

from libraries.models import Library
from users.models import CustomUser


def library_stats(request, user_id):
    if user_id is None:
        library = request.user.library
    else:
        library = get_object_or_404(Library, user=user_id)
    return render(request, 'library_stats.html', {'library': library})


def compare_stats(request, user_id):
    context = {
        'my_library': request.user.library,
        'users': CustomUser.objects.exclude(pk=request.user.pk),
    }
    if user_id:
        context['their_library'] = get_object_or_404(Library, user=user_id)
    return render(request, 'compare_stats.html', context)
