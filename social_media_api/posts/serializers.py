from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='auther.username')
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author',
                  'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     post_id = self.context.get('post_id')

    #     if not post_id:
    #         raise serializers.ValidationError(
    #             'Post_id is required to create a comment')

    #     try:
    #         post = Post.objects.get(id=post_id)
    #     except Post.DoesNotExist:
    #         raise serializers.ValidationError('Invalid post_id')

    #     comment = Comment.objects.create(
    #         author=user, post=post, **validated_data)

    #     return comment

    # def validate_content(self, value):
    #     if len(value.strip()) < 3:
    #         raise serializers.ValidationError(
    #             'Content must be 3 character long at least')
    #     return value


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='auther.username')

    class Meta:
        model = Post
        fields = ['id', 'author', 'title',
                  'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     post = Post.objects.create(author=user, **validated_data)
    #     return post

    # def validate_title(self, value):
    #     if len(value.strip()) < 5:
    #         raise serializers.ValidationError(
    #             "Title must be at least 5 characters long")
    #     return value

    # def validate_content(self, value):
    #     if len(value.strip()) < 10:
    #         raise serializers.ValidationError(
    #             "Content must be at least 10 characters long")
    #     return value

    # def get_comment_count(self, obj):
    #     return obj.comments.count()
