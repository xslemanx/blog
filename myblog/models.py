from django.db import models
from django import forms
from django.utils import timezone


class PublishedPostManager(models.Manager):
    def published(self):
        return self.filter(post_status='Published')

class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    post_title=models.CharField(max_length=100)
    post_author = models.CharField(max_length=100)
    post_slug=models.CharField(max_length=100)
    post_body = models.TextField(max_length=1000,default="")
    post_publish_date = models.DateTimeField("date published", default=timezone.now)
    post_create_date = models.DateTimeField("date created", default=timezone.now)
    post_update_date = models.DateTimeField("date updated", default=timezone.now)
    STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Published', 'Published'),
    )

    post_status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    objects = PublishedPostManager()

    def __str__(self):
        return self.post_title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

class CustomCommentForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    body = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))

