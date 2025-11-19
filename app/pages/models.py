from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from app.shared.models import TimestampMixin


class Page(TimestampMixin):
    """
    Static page model for content like About, Contact, Terms, etc.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO meta description")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pages')
    published = models.BooleanField(default=False)
    order = models.IntegerField(default=0, help_text="Order for displaying in navigation")
    show_in_navigation = models.BooleanField(default=True, help_text="Show this page in navigation menu")

    class Meta:
        ordering = ['order', 'title']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['published']),
            models.Index(fields=['order']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure uniqueness
            original_slug = self.slug
            counter = 1
            while Page.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
