from django.shortcuts import get_object_or_404, render

from libraries.models import Library


def library_stats(request, user_id):
    if user_id is None:
        library = request.user.library
    else:
        library = get_object_or_404(Library, user=user_id)
    return render(request, 'library_stats.html', {'library': library})
