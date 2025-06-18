from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render
from django.views import generic, View
from . models import Genre, Genrefellow
from . import models
from posts.models import Post
# Create your views here.

class CreateGenre(LoginRequiredMixin, generic.CreateView):
    fields = ("name", "description")
    model = Genre

class SingleGenre(View) :
    def get(self, request, *args, **kwargs):
        genre_opened = get_object_or_404(Genre, slug=self.kwargs.get("slug"))
        post_to_displayed = []
        for item in Post.objects.all():
            if str(item.genre) == str(genre_opened.name):
                post_to_displayed.append(item)
        return render(request, 'genre/genre_details.html',
                      {'post_list': post_to_displayed, 'genre': genre_opened})

class ListGenre(generic.ListView) :
    model = Genre

class JoinGenre(LoginRequiredMixin, generic.RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):
        return reverse("genre:single", kwargs={"slug": self.kwargs.get("slug")})
    
    def get(self, request, *args, **kwargs):
        genre = get_object_or_404(Genre,
                                  slug=self.kwargs.get("slug"))
        try:
            Genrefellow.object.create(user=self.request.user,
                                      genre=genre)
        except IntegrityError:
            messages.warning(self.request,
                             ("Warning, already a fellow of {}".format(genre.name)))
        else:
            messages.success(self.request,
                             "You are now a fellow of the {} genre.".format(genre.name))
        return super().get(request, *args, **kwargs)
    
class LeaveGenre(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("gener:single", kwargs={"slug": self.kwargs.get("slug")})
    
    def get(self, request, *args, **kwargs):
        try:
            fellowship = models.Genrefellow.objects.filter(
                user=self.request.user,
                genere__slug=self.kwargs.get("slug")
            ).get()
        except models.Genrefellow.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this genre because you aren't in it."
            )
        else:
            fellowship.delete()
            messages.success(
                self.request,
                "You have successfully left this genre."
            )
        return super().get(request, *args, **kwargs)