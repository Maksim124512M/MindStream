from django.urls import path

from .views import (
    CreatePostView,
    ListPostView,
    ListMyPostView,
    UpdatePostView,
    DeletePostView,
)


urlpatterns = [
    path('post/create/', CreatePostView.as_view(), name='post_create'),
    path('post/list/', ListPostView.as_view(), name='post_list'),
    path('my_post/list/', ListMyPostView.as_view(), name='my_post_list'),
    path('post/delete/<int:pk>/', DeletePostView.as_view(), name='post_delete'),
    path('post/update/<int:pk>/', UpdatePostView.as_view(), name='post_update'),
]