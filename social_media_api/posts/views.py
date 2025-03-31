from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, serializers
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def feed(self, request):
        user = request.user
        following_users = user.following.all()
        posts = Post.objects.filter(
            author__in=following_users).order_by('-created_at')
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, post_id):
        user = request.user
        post = Post.objects.get(id=post_id)
        like = Like.objects.create(user=user, post=post)
        like.save()

        return Response({'message': 'You liked this post'}, status=status.HTTP_201_CREATED)

# Post.objects.filter(author__in=following_users).order_by


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Option to filter comments by post_id if provided in query params
        post_id = self.kwargs.get('post_id', None)
        if post_id:
            return Comment.objects.filter(post_id=post_id)
        return Comment.objects.all()

    def perform_create(self, serializer):
        # Check if this is a nested route with post_id in the URL
        post_id = self.kwargs.get('post_id')

        # Validate that post_id is provided
        if not post_id:
            raise serializers.ValidationError(
                {"post_id": "This field is required."})

        # Try to get the post
        post = get_object_or_404(Post, id=post_id)

        # Save the comment with the author and post
        serializer.save(author=self.request.user, post=post)
