from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    STATUS = (
        ('draft','Draft'),
        ('published','Published'),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,unique_for_date = 'publish')
    author = models.ForeignKey(User,related_name='blog_post',on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS,default='draft')

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title