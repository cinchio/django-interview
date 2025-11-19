from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Page


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying author information
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')
        read_only_fields = fields


class PageListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing pages (minimal fields)
    """
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Page
        fields = ('id', 'title', 'slug', 'meta_description', 'author', 'published',
                  'order', 'show_in_navigation', 'created_at', 'updated_at')
        read_only_fields = ('id', 'slug', 'created_at', 'updated_at')


class PageDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed page view
    """
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Page
        fields = ('id', 'title', 'slug', 'content', 'meta_description', 'author',
                  'published', 'order', 'show_in_navigation', 'created_at', 'updated_at')
        read_only_fields = ('id', 'slug', 'author', 'created_at', 'updated_at')


class PageCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating pages
    """
    class Meta:
        model = Page
        fields = ('title', 'content', 'meta_description', 'published', 'order', 'show_in_navigation')

    def create(self, validated_data):
        # Author is set automatically from request.user in the view
        return Page.objects.create(**validated_data)


class NavigationPageSerializer(serializers.ModelSerializer):
    """
    Minimal serializer for navigation menu
    """
    class Meta:
        model = Page
        fields = ('id', 'title', 'slug', 'order')
        read_only_fields = fields
