import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLES = (
        ('1', 'member'),
        ('2', 'admin')
    )

    role = models.CharField(max_length=255, choices=ROLES)
    subscribers = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


class Post(models.Model):
    CATEGORY = (
        ('personal_life', 'Personal life'),
        ('traveling', 'Traveling'),
        ('education', 'Education'),
        ('career', 'Career'),
        ('psychology', 'Psychology'),
        ('health', 'Health'),
        ('hobbys', 'Hobbys'),
        ('art', 'Art'),
        ('music', 'Music'),
        ('films', 'Films'),
        ('books', 'Books'),
        ('technology', 'Technology'),
        ('science', 'Science'),
        ('sport', 'Sport'),
        ('cooking', 'Cooking'),
        ('policy', 'Policy'),
        ('philosophy', 'Philosophy'),
        ('self_development', 'Self-development'),
        ('motivation', 'Motivation'),
        ('social', 'Social'),
    )

    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField()
    category = models.CharField(max_length=255, choices=CATEGORY)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class Subscription(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriber')
    subscribed_to = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('subscriber', 'subscribed_to')


class Comment(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class Like(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='liked_posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        unique_together = ('author', 'post')


class Dislike(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='disliked_posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dislikes')

    class Meta:
        verbose_name = 'Dislike'
        verbose_name_plural = 'Dislikes'
        unique_together = ('author', 'post')