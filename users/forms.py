from django import forms
from django.contrib.auth import get_user_model


class UserForm(forms.Form):
    user = forms.ModelChoiceField(get_user_model().objects.all())

    def __init__(self, *args, me=None, **kwargs):
        super().__init__(*args, **kwargs)
        if me is not None:
            self.fields['user'].queryset = get_user_model().objects.exclude(pk=me.pk)
