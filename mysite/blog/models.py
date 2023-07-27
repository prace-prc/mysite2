from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager


# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', '게시되지 않음'
        PUBLISHED = 'PB', '게시됨'

    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    slug = models.SlugField(max_length=200)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager(blank=True)
    status = models.CharField(
        choices=Status.choices, max_length=2, default=Status.DRAFT
    )

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=25)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]

    def __str__(self):
        return self.body

