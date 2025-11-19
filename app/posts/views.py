from rest_framework import generics, permissions, filters
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Post
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    PostCreateUpdateSerializer
)
from .permissions import IsAuthorOrReadOnly


@extend_schema_view(
    get=extend_schema(
        summary="List all blog posts",
        description="Get a paginated list of blog posts. Public users see only published posts. Authors can see their own drafts."
    ),
    post=extend_schema(
        summary="Create a new blog post",
        description="Create a new blog post. Requires authentication."
    )
)
class PostListCreateView(generics.ListCreateAPIView):
    """
    List all blog posts or create a new post
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['published', 'author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']

    def get_queryset(self):
        """
        Return published posts for anonymous users,
        but allow authenticated users to see their own drafts
        """
        queryset = Post.objects.select_related('author')

        if self.request.user.is_authenticated:
            # Authenticated users see all published posts + their own posts
            return queryset.filter(
                models.Q(published=True) | models.Q(author=self.request.user)
            )
        else:
            # Anonymous users only see published posts
            return queryset.filter(published=True)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateUpdateSerializer
        return PostListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@extend_schema_view(
    get=extend_schema(
        summary="Get a blog post",
        description="Retrieve a single blog post by ID"
    ),
    put=extend_schema(
        summary="Update a blog post",
        description="Update a blog post. Only the author can update their posts."
    ),
    patch=extend_schema(
        summary="Partially update a blog post",
        description="Partially update a blog post. Only the author can update their posts."
    ),
    delete=extend_schema(
        summary="Delete a blog post",
        description="Delete a blog post. Only the author can delete their posts."
    )
)
class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a blog post
    """
    queryset = Post.objects.select_related('author')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PostCreateUpdateSerializer
        return PostDetailSerializer

    def get_queryset(self):
        """
        Allow users to view published posts or their own posts
        """
        queryset = super().get_queryset()

        if self.request.user.is_authenticated:
            return queryset.filter(
                models.Q(published=True) | models.Q(author=self.request.user)
            )
        else:
            return queryset.filter(published=True)


@extend_schema(
    summary="List user's own posts",
    description="Get all posts created by the authenticated user"
)
class MyPostsListView(generics.ListAPIView):
    """
    List all posts by the authenticated user
    """
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).select_related('author')


# Import models for Q queries
from django.db import models
