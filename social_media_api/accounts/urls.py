from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UserViewSet, FollowView, UnFollowView


# login/ // register/
router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('user/follow/<int:user_id>/', FollowView.as_view(), name='follow-user'),
    path('user/unfollow/<int:user_id>/',
         UnFollowView.as_view(), name='unfollow-user'),
]
