from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying author information
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')
        read_only_fields = fields


class PostListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing blog posts (minimal fields)
    """
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'author', 'published', 'created_at', 'updated_at')
        read_only_fields = ('id', 'slug', 'created_at', 'updated_at')


class PostDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed blog post view
    """
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'content', 'author', 'published', 'created_at', 'updated_at')
        read_only_fields = ('id', 'slug', 'author', 'created_at', 'updated_at')


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating blog posts
    """
    class Meta:
        model = Post
        fields = ('title', 'content', 'published')

    def create(self, validated_data):
        # Author is set automatically from request.user in the view
        return Post.objects.create(**validated_data)
