from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Title : {self.title}"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Posts'


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Comments'


class Like(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name='likes')
