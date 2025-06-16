from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
from . models import Genre, Genrefellow
from . import models
# Create your views here.

class CreateGenre(LoginRequiredMixin, generic.CreateView):
    fields = ("name", "description")
    model = Genre

class SingleGenre(generic.DetailView) :
    model = Genre

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