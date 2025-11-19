from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin configuration for Post model
    """
    list_display = ('title', 'author', 'published', 'created_at', 'updated_at')
    list_filter = ('published', 'created_at', 'author')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'slug', 'author', 'content')
        }),
        ('Status', {
            'fields': ('published',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        Set author to current user if creating new post
        """
        if not change:  # If creating new object
            obj.author = request.user
        super().save_model(request, obj, form, change)
