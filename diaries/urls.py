from django.urls import path

from .views import (
    CreatePostView, ListPostView, ListMyPostView, UpdatePostView,
    DeletePostView, SubscribeView, UnsubscribeView, FilterPosts,
    CreateCommentView, CommentsListView, CommentUpdateView,
    CommentDeleteView, LikeView, DislikeView,
)


urlpatterns = [
    path('post/create/', CreatePostView.as_view(), name='post_create'),
    path('post/list/', ListPostView.as_view(), name='post_list'),
    path('my_post/list/', ListMyPostView.as_view(), name='my_post_list'),
    path('post/delete/<uuid:uuid>/', DeletePostView.as_view(), name='post_delete'),
    path('post/update/<uuid:uuid>/', UpdatePostView.as_view(), name='post_update'),
    path('subscribe/<uuid:uuid>/', SubscribeView.as_view(), name='subscribe'),
    path('unsubscribe/<uuid:uuid>/', UnsubscribeView.as_view(), name='unsubscribe'),
    path('post/filter/<str:category_name>/', FilterPosts.as_view(), name='post_filter'),
    path('comment/create/', CreateCommentView.as_view(), name='comment_create'),
    path('comments/', CommentsListView.as_view(), name='comments_list'),
    path('comment/update/<uuid:uuid>/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/delete/<uuid:uuid>/', CommentDeleteView.as_view(), name='comment_delete'),
    path('post/like/<uuid:uuid>/', LikeView.as_view(), name='post_like'),
    path('post/dislike/<uuid:uuid>/', DislikeView.as_view(), name='post_dislike'),
]