from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from genre.models import Genre

# Create your models here.
User = get_user_model()

class Post(models.Model):
    name = models.CharField(max_length=255, unique=False)
    user = models.ForeignKey(User, related_name="posts",
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    content_html = models.TextField(editable=False)
    genre = models.ForeignKey(Genre, related_name="posts", null=True,
                              blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.content_html = self.content
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "posts:single",
            kwargs={
                "username": self.user.username,
                "pk": self.pk
            }
        )
    
    class Meta:
        ordering = ["-created_at"]
        unique_together = ["user", "name"]