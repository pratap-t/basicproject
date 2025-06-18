from django import forms

from . import models

class PostForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'content', 'genre')
        model = models.Post

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["genre"].queryset = (
                models.Genre.objects.filter(
                    pk__in=user.genre.values_list("genre__pk")
                )
            )