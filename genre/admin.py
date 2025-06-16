from django.contrib import admin
from . import models
# Register your models here.

class GenreFellowInline(admin.TabularInline):
    model = models.Genrefellow
admin.site.register(models.Genre)