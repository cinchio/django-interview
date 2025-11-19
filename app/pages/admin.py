from django.contrib import admin
from .models import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    """
    Admin configuration for Page model
    """
    list_display = ('title', 'slug', 'author', 'published', 'show_in_navigation', 'order', 'created_at')
    list_filter = ('published', 'show_in_navigation', 'created_at', 'author')
    search_fields = ('title', 'content', 'meta_description', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('order', 'title')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('order', 'published', 'show_in_navigation')

    fieldsets = (
        ('Page Information', {
            'fields': ('title', 'slug', 'author', 'content', 'meta_description')
        }),
        ('Display Settings', {
            'fields': ('published', 'show_in_navigation', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        Set author to current user if creating new page
        """
        if not change:  # If creating new object
            obj.author = request.user
        super().save_model(request, obj, form, change)
