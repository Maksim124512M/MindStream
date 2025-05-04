from django.core.exceptions import PermissionDenied

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer


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


