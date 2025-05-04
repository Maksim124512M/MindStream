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

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField()
    category = models.CharField(max_length=255, choices=CATEGORY)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class Subscription(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriber')
    subscribed_to = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('subscriber', 'subscribed_to')