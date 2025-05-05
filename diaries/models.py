import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ''' Model for User '''

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
    '''
    Model for creating posts.

    This model is used for storing posts, including information about the author, title, content,
    creation and update time, visibility, category, and the number of likes and dislikes.

    Attributes:
    uuid (UUID): A unique identifier for the post, generated automatically.
    author (ForeignKey): A foreign key to the User model, indicating the post's author.
    title (str): The title of the post.
    content (str): The content of the post.
    created_at (datetime): The timestamp when the post was created.
    updated_at (datetime): The timestamp of the last update to the post.
    is_public (bool): Indicates whether the post is public.
    category (str): The category of the post, selected from a predefined list of categories.
    likes (int): The number of likes on the post.
    dislikes (int): The number of dislikes on the post.

    Methods:
    __str__(): Returns the title of the post as its string representation.

    Meta:
    verbose_name (str): The human-readable name of the model in the admin interface.
    verbose_name_plural (str): The plural form of the model name in the admin interface.
    '''

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
    '''
    Model for managing subscriptions between users.

    This model represents the relationship where one user subscribes to another user.
    A user can subscribe to another user, and this subscription is unique for each pair
    of subscribers.

    Attributes:
    uuid (UUID): A unique identifier for the subscription.
    subscriber (ForeignKey): A foreign key to the `User` model, representing the user who subscribes.
    subscribed_to (ForeignKey): A foreign key to the `User` model, representing the user being subscribed to.

    Meta:
    unique_together (tuple): Ensures that each subscription (between a subscriber and a subscribed user) is unique.
    '''

    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriber')
    subscribed_to = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('subscriber', 'subscribed_to')


class Comment(models.Model):
    '''
    Model for storing comments on posts.

    This model represents a comment left by a user on a specific post. Each comment has an
    author, content, and timestamp indicating when it was created.

    Attributes:
    uuid (UUID): A unique identifier for the comment.
    author (ForeignKey): A foreign key to the `User` model, indicating the comment's author.
    post (ForeignKey): A foreign key to the `Post` model, indicating which post the comment belongs to.
    content (str): The text content of the comment.
    created_at (datetime): The timestamp when the comment was created.

    Meta:
    verbose_name (str): The human-readable name for the model in the admin interface.
    verbose_name_plural (str): The plural form of the model name in the admin interface.
    '''

    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class Like(models.Model):
    '''
    Model for storing likes on posts.

    This model represents a like given by a user on a specific post. Each like is unique
    per user and per post.

    Attributes:
    uuid (UUID): A unique identifier for the like.
    post (ForeignKey): A foreign key to the `Post` model, indicating which post was liked.
    author (ForeignKey): A foreign key to the `User` model, indicating which user liked the post.

    Meta:
    verbose_name (str): The human-readable name for the model in the admin interface.
    verbose_name_plural (str): The plural form of the model name in the admin interface.
    unique_together (tuple): Ensures that each user can only like a post once.
    '''

    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='liked_posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        unique_together = ('author', 'post')


class Dislike(models.Model):
    """
    Model for storing dislikes on posts.

    This model represents a dislike given by a user on a specific post. Each dislike is unique
    per user and per post.

    Attributes:
    uuid (UUID): A unique identifier for the dislike.
    post (ForeignKey): A foreign key to the `Post` model, indicating which post was disliked.
    author (ForeignKey): A foreign key to the `User` model, indicating which user disliked the post.

    Meta:
    verbose_name (str): The human-readable name for the model in the admin interface.
    verbose_name_plural (str): The plural form of the model name in the admin interface.
    unique_together (tuple): Ensures that each user can only dislike a post once.
    """

    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='disliked_posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dislikes')

    class Meta:
        verbose_name = 'Dislike'
        verbose_name_plural = 'Dislikes'
        unique_together = ('author', 'post')