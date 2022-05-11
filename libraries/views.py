from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from libraries.models import Library
from users.models import CustomUser


@login_required
def library_stats(request, user_id):
    if user_id is None:
        library = request.user.library
    else:
        library = get_object_or_404(Library, user=user_id)
    return render(request, 'library_stats.html', {'library': library})


@login_required
def compare_stats(request):
    context = {
        'my_library': request.user.library,
        'users': CustomUser.objects.exclude(pk=request.user.pk),
    }
    user_id = request.GET.get('user_id', None)
    if user_id:
        context['their_library'] = get_object_or_404(Library, user=user_id)
    return render(request, 'compare_stats.html', context)
