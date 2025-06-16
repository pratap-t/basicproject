from django import template
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
register = template.Library()
User = get_user_model()

class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    fellows = models.ManyToManyField(User, through="GenreFellow")

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = self.description
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('genre:single', kwargs={"slug": self.slug})
    
    class Meta:
        ordering = ["name"]

class Genrefellow(models.Model):
    genre = models.ForeignKey(Genre, related_name="fellowships", on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name='user_genre', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
    class Meta:
        unique_together = ("genre", "user")