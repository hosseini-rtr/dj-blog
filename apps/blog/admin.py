from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils import timezone
from django.utils.html import format_html

from apps.blog.models import Post
from apps.common.models import Comment


class CommentInline(GenericTabularInline):
    model = Comment
    extra = 0
    fields = ('author', 'content', 'is_approved', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'title', 'author', 'lang', 'is_published',
                    'allow_comments', 'created_at', 'comment_count', 'get_view_count')

    list_filter = ('review_status', 'is_published', 'lang', 'author',
                   'allow_comments',)

    search_fields = ('title', 'content')
    readonly_fields = ('image_preview', 'get_view_count')

    def get_view_count(self, obj):
        return obj.view_count
    get_view_count.short_description = 'Views'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "No Image"

    prepopulated_fields = {'slug': ('title',)}
    inlines = [CommentInline]
    actions = ['make_published', 'make_unpublished']

    def make_published(self, request, queryset):
        updated = queryset.update(
            is_published=True, published_at=timezone.now())
        self.message_user(
            request, f"{updated} post(s) published successfully.")
    make_published.short_description = "Publish selected posts"

    def make_unpublished(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(
            request, f"{updated} post(s) unpublished successfully.")
    make_unpublished.short_description = "Unpublish selected posts"

    fieldsets = (
        ('Content', {'fields': ('title', 'subtitle',
         'slug', 'content', 'lang', 'image', 'image_preview', 'thumbnail', 'created_at')}),
        ('Author', {'fields': ('author',)}),
        ('publish', {'fields': ('review_status',
         "is_published", 'published_at')}),
        ('SEO', {'fields': ('meta_title', 'meta_description',
         'meta_keywords', 'canonical_url', 'noindex')}),
        ('Checking', {'fields': ('reviewed_by', 'reviewed_at',
         'review_note'), 'classes': ('collapse',)}),
        ('Comments', {'fields': ('allow_comments',)}),
        ('tags', {'fields': ('tags',)}),
    )

    def comment_count(self, obj):
        return obj.comment_count
    comment_count.short_description = 'Comments'
