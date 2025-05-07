from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied

from .models import Post, Subscription, User, Comment, Like, Dislike
from .serializers import PostSerializer, CommentSerializer

class CreatePostView(generics.CreateAPIView):
    ''' View to create a post '''

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


class ListPostView(generics.ListAPIView):
    ''' View to list publicly available posts '''

    queryset = Post.objects.filter(is_public=True)
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


class ListMyPostView(generics.ListAPIView):
    ''' View to list posts authored by the authenticated user '''

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.filter(author=request.user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class UpdatePostView(generics.UpdateAPIView):
    ''' View to update a post '''

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def put(self, request, *args, **kwargs):
        post = self.get_object()
        user = request.user

        if user != post.author and user.role != '2':  # Assuming role '2' is an admin
            raise PermissionDenied('You do not have permission to edit this post.')

        serializer = self.get_serializer(instance=post, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class DeletePostView(generics.DestroyAPIView):
    ''' View to delete a post '''

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        user = request.user

        if user != post.author and user.role != '2':
            raise PermissionDenied('You do not have permission to delete this post.')

        post.delete()
        return Response('Post successfully deleted')


class SubscribeView(APIView):
    ''' View to subscribe to a user '''

    permission_classes = [IsAuthenticated]

    def post(self, request, uuid):
        subscribed_to = get_object_or_404(User, uuid=uuid)
        subscriber = request.user

        if subscribed_to == subscriber:
            return Response('Cannot subscribe to yourself')

        # Use get_or_create to avoid duplicate subscriptions
        subscription, created = Subscription.objects.get_or_create(subscriber=subscriber, subscribed_to=subscribed_to)

        if not created:
            return Response('Already subscribed')

        subscribed_to.subscribers += 1
        subscribed_to.save()

        return Response('Successfully subscribed to the user')


class UnsubscribeView(APIView):
    ''' View to unsubscribe from a user '''

    permission_classes = [IsAuthenticated]

    def delete(self, request, uuid):
        unsubscribed_to = get_object_or_404(User, uuid=uuid)
        unsubscriber = request.user

        if unsubscribed_to == unsubscriber:
            return Response('Cannot unsubscribe from yourself')

        # Ensure subscription exists before deleting
        subscription = Subscription.objects.get(subscriber=unsubscriber, subscribed_to=unsubscribed_to)
        subscription.delete()

        unsubscribed_to.subscribers -= 1
        unsubscribed_to.save()

        return Response('Successfully unsubscribed from the user')


class FilterPosts(APIView):
    ''' View to filter posts by category '''

    permission_classes = [IsAuthenticated]

    def get(self, request, category_name):
        posts = Post.objects.filter(category=category_name, is_public=True)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class CreateCommentView(generics.CreateAPIView):
    ''' View to create a comment on a post '''

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


class CommentsListView(generics.ListAPIView):
    ''' View to list all comments '''

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


class CommentUpdateView(generics.UpdateAPIView):
    ''' View to update a comment '''

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        comment = super().get_object()
        user = self.request.user

        if user != comment.author and user.role != '2':
            raise PermissionDenied('You do not have permission to edit this comment.')

        return comment


class CommentDeleteView(generics.DestroyAPIView):
    ''' View to delete a comment '''

    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, uuid):
        instance = get_object_or_404(Comment, uuid=uuid)

        if request.user != instance.author and request.user.role != '2':
            raise PermissionDenied('You do not have permission to delete this comment.')

        instance.delete()
        return Response('Comment deleted successfully')


class LikeView(APIView):
    ''' View to like a post '''

    permission_classes = [IsAuthenticated]

    def post(self, request, uuid):
        post = get_object_or_404(Post, uuid=uuid)

        like, created = Like.objects.get_or_create(post=post, author=request.user)

        if not created:
            return Response('You have already liked this post')

        post.likes += 1
        post.save()

        return Response('You have successfully liked the post')


class DislikeView(APIView):
    ''' View to dislike a post '''

    permission_classes = [IsAuthenticated]

    def post(self, request, uuid):
        post = get_object_or_404(Post, uuid=uuid)

        dislike, created = Dislike.objects.get_or_create(post=post, author=request.user)

        if not created:
            return Response('You have already disliked this post')

        post.dislikes += 1
        post.save()

        return Response('You have successfully disliked the post')