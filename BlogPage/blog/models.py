from taggit.managers import TaggableManager

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse


# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return (
                super().get_queryset().filter(status=Post.Status.PUBLISHED)
                )

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete = models.CASCADE,
            related_name = 'blog_posts'
            )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
            max_length=2,
            choices=Status,
            default=Status.DRAFT
            )
    
    tags = TaggableManager()
    objects = models.Manager() # default manager
    published = PublishedManager()


    class Meta:
        ordering = ['-publish']
        indexes = [
                models.Index(fields=['-publish']),
                ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

            original_slug = self.slug
            counter = 1
            while Post.objects.filter(slug=self.slug).exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
                'blog:post_detail',
                args=[self.slug]
                )

class Comment(models.Model):
    post = models.ForeignKey(
            Post,
            on_delete=models.CASCADE,
            related_name='comments'
            )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
                models.Index(fields=['created']),
                ]
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

