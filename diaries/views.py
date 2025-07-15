from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request

from drf_spectacular.utils import extend_schema

from .models import Post, Subscription, User, Comment, Like, Dislike
from .serializers import PostSerializer, CommentSerializer


# ------------ Post Views ------------

@extend_schema(tags=['Posts'])
class CreatePostView(generics.CreateAPIView):
    '''Create a new post.'''

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['Posts'])
class ListPostView(generics.ListAPIView):
    '''List all publicly available posts.'''

    queryset = Post.objects.filter(is_public=True)
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['Posts'])
class ListMyPostView(generics.ListAPIView):
    '''List posts authored by the authenticated user.'''

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        posts = Post.objects.filter(author=request.user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


@extend_schema(tags=['Posts'])
class UpdatePostView(generics.UpdateAPIView):
    '''Update a post (author or admin only).'''

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def put(self, request: Request, *args, **kwargs) -> Response:
        post = self.get_object()
        if request.user != post.author and request.user.role != '2':
            raise PermissionDenied('You do not have permission to edit this post.')
        serializer = self.get_serializer(instance=post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


@extend_schema(tags=['Posts'])
class DeletePostView(generics.DestroyAPIView):
    '''Delete a post (author or admin only).'''

    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def delete(self, request: Request, *args, **kwargs) -> Response:
        post = self.get_object()
        if request.user != post.author and request.user.role != '2':
            raise PermissionDenied('You do not have permission to delete this post.')
        post.delete()
        return Response('Post deleted successfully.', status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['Subscriptions'])
class SubscribeView(APIView):
    '''Subscribe to another user.'''

    permission_classes = [IsAuthenticated]

    def post(self, request: Request, uuid: str) -> Response:
        target = get_object_or_404(User, uuid=uuid)
        subscriber = request.user
        if target == subscriber:
            return Response('Cannot subscribe to yourself.', status=status.HTTP_400_BAD_REQUEST)
        sub, created = Subscription.objects.get_or_create(subscriber=subscriber, subscribed_to=target)
        if not created:
            return Response('Already subscribed.', status=status.HTTP_400_BAD_REQUEST)
        target.subscribers += 1
        target.save()
        return Response('Successfully subscribed.', status=status.HTTP_201_CREATED)


@extend_schema(tags=['Subscriptions'])
class UnsubscribeView(APIView):
    '''Unsubscribe from a user.'''

    permission_classes = [IsAuthenticated]

    def delete(self, request: Request, uuid: str) -> Response:
        target = get_object_or_404(User, uuid=uuid)
        user = request.user
        if target == user:
            return Response('Cannot unsubscribe from yourself.', status=status.HTTP_400_BAD_REQUEST)
        subscription = get_object_or_404(Subscription, subscriber=user, subscribed_to=target)
        subscription.delete()
        target.subscribers = max(target.subscribers - 1, 0)
        target.save()
        return Response('Successfully unsubscribed.', status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['Posts'])
class FilterPostsView(APIView):
    '''Filter public posts by category.'''

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, category_name: str) -> Response:
        posts = Post.objects.filter(category=category_name, is_public=True)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


# ------------ Comment Views ------------

@extend_schema(tags=['Comments'])
class CreateCommentView(generics.CreateAPIView):
    '''Create a comment on a post.'''

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['Comments'])
class CommentsListView(generics.ListAPIView):
    '''List all comments.'''

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['Comments'])
class CommentUpdateView(generics.UpdateAPIView):
    '''Update a comment (author or admin only).'''

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def get_object(self) -> Comment:
        comment = super().get_object()
        user = self.request.user
        if user != comment.author and user.role != '2':
            raise PermissionDenied('You do not have permission to edit this comment.')
        return comment


@extend_schema(tags=['Comments'])
class CommentDeleteView(APIView):
    '''Delete a comment (author or admin only).'''

    permission_classes = [IsAuthenticated]

    def delete(self, request: Request, uuid: str) -> Response:
        comment = get_object_or_404(Comment, uuid=uuid)
        user = request.user
        if user != comment.author and user.role != '2':
            raise PermissionDenied('You do not have permission to delete this comment.')
        comment.delete()
        return Response('Comment deleted successfully.', status=status.HTTP_204_NO_CONTENT)


# ------------ Like & Dislike Views ------------

@extend_schema(tags=['Reactions'])
class LikeView(APIView):
    '''Like a post.'''

    permission_classes = [IsAuthenticated]

    def post(self, request: Request, uuid: str) -> Response:
        post = get_object_or_404(Post, uuid=uuid)
        like, created = Like.objects.get_or_create(post=post, author=request.user)
        if not created:
            return Response('Already liked this post.', status=status.HTTP_400_BAD_REQUEST)
        post.likes += 1
        post.save()
        return Response('Post liked.', status=status.HTTP_201_CREATED)


@extend_schema(tags=['Reactions'])
class DislikeView(APIView):
    '''Dislike a post.'''

    permission_classes = [IsAuthenticated]

    def post(self, request: Request, uuid: str) -> Response:
        post = get_object_or_404(Post, uuid=uuid)
        dislike, created = Dislike.objects.get_or_create(post=post, author=request.user)
        if not created:
            return Response('Already disliked this post.', status=status.HTTP_400_BAD_REQUEST)
        post.dislikes += 1
        post.save()
        return Response('Post disliked.', status=status.HTTP_201_CREATED)