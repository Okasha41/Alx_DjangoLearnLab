from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register('posts', PostViewSet, basename='post')
router.register('comments', CommentViewSet, basename='comment')


urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_id>/comments',
         CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-comments'),
    path('posts/<int:post_id>/like',
         CommentViewSet.as_view({'post': 'create'}), name='post-likes'),
    path('posts/feed/',
         PostViewSet.as_view({'get': 'feed'}), name='posts-feed')
]
