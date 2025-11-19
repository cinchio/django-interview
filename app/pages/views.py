from rest_framework import generics, permissions, filters
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Page
from .serializers import (
    PageListSerializer,
    PageDetailSerializer,
    PageCreateUpdateSerializer,
    NavigationPageSerializer
)
from .permissions import IsAuthorOrReadOnly


@extend_schema_view(
    get=extend_schema(
        summary="List all pages",
        description="Get a paginated list of pages. Public users see only published pages. Authors can see their own drafts."
    ),
    post=extend_schema(
        summary="Create a new page",
        description="Create a new page. Requires authentication."
    )
)
class PageListCreateView(generics.ListCreateAPIView):
    """
    List all pages or create a new page
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['published', 'author', 'show_in_navigation']
    search_fields = ['title', 'content', 'meta_description']
    ordering_fields = ['order', 'created_at', 'updated_at', 'title']

    def get_queryset(self):
        """
        Return published pages for anonymous users,
        but allow authenticated users to see their own drafts
        """
        queryset = Page.objects.select_related('author')

        if self.request.user.is_authenticated:
            # Authenticated users see all published pages + their own pages
            return queryset.filter(
                models.Q(published=True) | models.Q(author=self.request.user)
            )
        else:
            # Anonymous users only see published pages
            return queryset.filter(published=True)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PageCreateUpdateSerializer
        return PageListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@extend_schema_view(
    get=extend_schema(
        summary="Get a page by slug",
        description="Retrieve a single page by its slug"
    ),
    put=extend_schema(
        summary="Update a page",
        description="Update a page. Only the author can update their pages."
    ),
    patch=extend_schema(
        summary="Partially update a page",
        description="Partially update a page. Only the author can update their pages."
    ),
    delete=extend_schema(
        summary="Delete a page",
        description="Delete a page. Only the author can delete their pages."
    )
)
class PageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a page by slug
    """
    queryset = Page.objects.select_related('author')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PageCreateUpdateSerializer
        return PageDetailSerializer

    def get_queryset(self):
        """
        Allow users to view published pages or their own pages
        """
        queryset = super().get_queryset()

        if self.request.user.is_authenticated:
            return queryset.filter(
                models.Q(published=True) | models.Q(author=self.request.user)
            )
        else:
            return queryset.filter(published=True)


@extend_schema(
    summary="Get navigation pages",
    description="Get all published pages that should be shown in navigation, ordered by order field"
)
class NavigationPagesView(generics.ListAPIView):
    """
    List pages for navigation menu
    """
    serializer_class = NavigationPageSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None  # No pagination for navigation

    def get_queryset(self):
        return Page.objects.filter(
            published=True,
            show_in_navigation=True
        ).order_by('order', 'title')


@extend_schema(
    summary="List user's own pages",
    description="Get all pages created by the authenticated user"
)
class MyPagesListView(generics.ListAPIView):
    """
    List all pages by the authenticated user
    """
    serializer_class = PageListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Page.objects.filter(author=self.request.user).select_related('author')
