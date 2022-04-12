from django.shortcuts import get_object_or_404, render
from libraries.models import Library


def library_stats(request, user_id):
    library = get_object_or_404(Library, user=user_id)
    return render(request, 'library_stats.html', {'library': library})
