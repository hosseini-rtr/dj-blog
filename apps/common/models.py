import hashlib
from typing import Any, Optional

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, models
from django.forms import ValidationError
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PublishableModel(TimeStampedModel):
    published_at = models.DateTimeField(
        null=True, blank=True, default=timezone.now)
    is_published = models.BooleanField(default=True)

    class Meta:
        abstract = True

    @property
    def is_live(self):
        return self.is_published and (
            self.published_at is None or self.published_at <= timezone.now()
        )


class SluggedModel(models.Model):
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(getattr(self, 'title', 'post'))
            slug = base_slug
            counter = 1

            while self.__class__.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


class AuthoredModel(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_set'
    )

    class Meta:
        abstract = True


class ReviewableModel(models.Model):
    review_status = models.CharField(
        max_length=20,
        choices=[
            ('draft', _('Draft')),
            ('pending', _('Pending Review')),
            ('approved', _('Approved')),
            ('rejected', _('Rejected')),
        ],
        default='approved'
    )
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_reviewed'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    review_note = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class SEOModel(models.Model):
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)

    canonical_url = models.URLField(blank=True)
    noindex = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.meta_title and hasattr(self, 'title'):
            self.meta_title = getattr(self, 'title')[:70]

        if not self.meta_description and hasattr(self, 'content'):
            text = getattr(self, 'content')
            self.meta_description = text[:160]

        super().save(*args, **kwargs)


class ViewCountModel(models.Model):
    views = GenericRelation('common.ContentView')

    class Meta:
        abstract = True

    @property
    def view_count(self):
        return self.views.count()

    def record_view(self, user: Optional[User] = None, viewer_ip: Optional[str] = None):
        ContentView.record_view(self, user, viewer_ip)


class CommentableModel(models.Model):
    comments = GenericRelation('common.Comment')
    allow_comments = models.BooleanField(default=True)

    class Meta:
        abstract = True

    @property
    def comment_count(self):
        return self.comments.filter(is_approved=True).count()


class ContentView(TimeStampedModel):
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, verbose_name=_("Content Type")
    )
    object_id = models.PositiveIntegerField(verbose_name=_("Object Id"))
    content_object = GenericForeignKey("content_type", "object_id")
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="content_views",
        verbose_name=_("User"),
    )
    viewer_ip = models.GenericIPAddressField(
        verbose_name=_("Viewer IP address"), null=True, blank=True
    )
    last_viewed = models.DateTimeField()

    class Meta:
        verbose_name = _("Content View")
        verbose_name_plural = _("Content Views")
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self) -> str:
        user_name = self.user.get_full_name() if self.user else "Anonymous"
        return f"{self.content_type} viewed by: {user_name} from IP {self.viewer_ip}"

    @classmethod
    def record_view(
        cls, content_object: Any, user: Optional[User], viewer_ip: Optional[str]
    ) -> None:
        content_type = ContentType.objects.get_for_model(content_object)

        try:
            view, created = cls.objects.get_or_create(
                content_type=content_type,
                object_id=content_object.id,
                defaults={
                    "user": user,
                    "viewer_ip": viewer_ip,
                    "last_viewed": timezone.now(),
                },
            )
            if not created:
                view.last_viewed = timezone.now()
                view.save()
        except IntegrityError:
            pass


class Comment(TimeStampedModel, AuthoredModel):
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, verbose_name=_("Content Type"),
        limit_choices_to={
            'model__in': ['post', 'event', 'product']
        })
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    content = models.TextField()
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    is_approved = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]

    def clean(self):
        if self.parent and self.parent.parent:
            raise ValidationError(_("Only one response surface is allowed."))

        if self.parent and self.parent.content_object != self.content_object:
            raise ValidationError(
                _("The answer must be for the same context."))

    @property
    def is_reply(self):
        return self.parent is not None

    def __str__(self):
        return f"Comment by {self.author.get_full_name()} on {self.content_object}"


class ShortURL(models.Model):
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, verbose_name=_("Content Type"))
    object_id = models.PositiveIntegerField(verbose_name=_("Object Id"))
    content_object = GenericForeignKey("content_type", "object_id")
    short_code = models.CharField(max_length=10, unique=True)

    class Meta:
        verbose_name = _("Short url")
        verbose_name_plural = _("short urls")
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['content_type', 'object_id'],
                name='unique_short_url_per_object'
            )
        ]

    def __str__(self):
        return f"short path {self.short_code} for {self.content_object}"

    @staticmethod
    def generate_code(obj):
        text = f"{obj.__class__.__name__}{obj.pk}"
        return hashlib.md5(text.encode()).hexdigest()[:6]
