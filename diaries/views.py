from django.core.exceptions import PermissionDenied

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

from .models import Post, Subscription, User, Comment
from .serializers import PostSerializer, CommentSerializer


class CreatePostView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


class ListPostView(generics.ListAPIView):
    queryset = Post.objects.filter(is_public=True)
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


class ListMyPostView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.filter(author_id=request.user.id)
        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)


class UpdatePostView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        post = self.get_object()
        user = request.user

        if user != post.author and user.role != '2':
            raise PermissionDenied('У вас немає прав на редагування цього запису.')

        serializer = self.get_serializer(instance=post, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class DeletePostView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        user = request.user

        if user != post.author and user.role != '2':
            raise PermissionDenied('У вас немає прав на видалення цього запису.')

        post.delete()
        post.save()
        return Response('Запис успішно видалений')


class SubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            subscribed_to = User.objects.get(id=pk)
        except User.DoesNotExist:
            raise NotFound('Користувача не знайдено.')

        subscriber = request.user

        if subscribed_to.id == subscriber.id:
            return Response('Неможливо підписатись на самого себе')

        subscription, created = Subscription.objects.get_or_create(
            subscriber=subscriber,
            subscribed_to=subscribed_to,
        )

        print(created)

        if not created:
            return Response('Неможливо підписатися двічі')

        subscribed_to.subscribers += 1
        subscribed_to.save()

        return Response('Ви успішно підписались на користувача')


class UnsubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            unsubscribed_to = User.objects.get(id=pk)
        except User.DoesNotExist:
            raise NotFound('Користувача не знайдено.')
        unsubscriber = request.user

        if unsubscribed_to.id == unsubscriber.id:
            return Response('Неможливо відписатись від самого себе')

        subscription = Subscription.objects.get(
            subscriber=unsubscriber,
            subscribed_to=unsubscribed_to,
        )

        subscription.delete()
        if unsubscribed_to.subscribers > 0:
            unsubscribed_to.subscribers -= 1
            unsubscribed_to.save()

        return Response('Ви успішно відписались від користувача')


class FilterPosts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, category_name):
        posts = Post.objects.filter(
            category=category_name,
            is_public=True,
        )
        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)


class CreateCommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


class CommentsListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


class CommentUpdateView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        comment = super().get_object()
        user = self.request.user

        if user != comment.author and user.role != '2':
            raise PermissionDenied('У вас немає прав на редагування цього запису.')

        return comment


class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            instance = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response({'detail': 'Не знайдено.'})

        if request.user != instance.author and request.user.role != '2':
            raise PermissionDenied('У вас немає прав на видалення цього запису.')

        instance.delete()
        return Response({'detail': 'Коментар видалено.'})