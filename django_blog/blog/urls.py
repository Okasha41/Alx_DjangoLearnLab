from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('posts', views.posts, name='posts'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('posts/', views.ListView.as_view(), name='list-view'),
    path('posts/<int:pk>/', views.DetailView.as_view(), name='detail-view'),
    path('post/new/', views.CreateView.as_view(), name='create-view'),
    path('post/<int:pk>/update/', views.UpdateView.as_view(), name='update-view'),
    path('post/<int:pk>/delete/', views.DeleteView.as_view(), name='delete-view'),
    path('posts/<int:post_id>/comments',
         views.ListComments.as_view(), name='comment-list'),
    path('post/<int:pk>/comments/new/',
         views.CreateComment.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/',
         views.UpdateComment.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/',
         views.CommentDeleteView.as_view(), name='comment-delete')
]
