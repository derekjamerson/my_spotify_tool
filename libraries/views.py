from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from libraries.models import Library
from users.forms import UserForm
from users.models import CustomUser


def library_stats(request, user_id):
    if user_id is None:
        library = request.user.library
    else:
        library = get_object_or_404(Library, user=user_id)
    return render(request, 'library_stats.html', {'library': library})


@login_required
def compare_stats(request):
    form = UserForm(me=request.user)
    context = {
        'my_library': request.user.library,
        'users': CustomUser.objects.exclude(pk=request.user.pk),
    }
    if request.GET:
        form = UserForm(request.GET)
        if form.is_valid():
            context['their_library'] = form.cleaned_data['user'].library
    context['form'] = form
    return render(request, 'compare_stats.html', context)


def browse_libraries(request):
    form = UserForm()
    library = None
    if request.GET:
        form = UserForm(request.GET)
        if form.is_valid():
            user = form.cleaned_data['user']
            library = user.library
    context = {
        'form': form,
        'library': library,
    }
    return render(request, 'library_stats.html', context)
