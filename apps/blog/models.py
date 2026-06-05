from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

from apps.common.models import (AuthoredModel, Comment, CommentableModel,
                                PublishableModel, ReviewableModel, SEOModel,
                                ShortURL, SluggedModel, TimeStampedModel,
                                ViewCountModel)
from core.utils import post_image_path


class LanguageOptions(models.TextChoices):
    FARSI = ("fa", _("Farsi"))
    ENGLISH = ("en", _("English"))
    ITALIAN = ("it", _("Italian"))


class Post(
    AuthoredModel,
    SEOModel,
    CommentableModel,
    ViewCountModel,
    PublishableModel,
    SluggedModel,
    ReviewableModel,
    TimeStampedModel
):
    title = models.CharField(max_length=255, unique=True)
    subtitle = models.CharField(max_length=100, null=True, blank=True)
    content = CKEditor5Field(config_name="default")
    image = models.ImageField(upload_to=post_image_path)
    thumbnail = models.ImageField(
        upload_to='posts/thumbnails/', null=True, blank=True)
    short_urls = GenericRelation('common.ShortURL', related_query_name='post')

    comments = GenericRelation(Comment, related_query_name='post')
    lang = models.CharField(
        _("Post's Language"), max_length=4, choices=LanguageOptions.choices
    )
    tags = TaggableManager()

    @cached_property
    def short_url(self):
        return self.short_urls.first()

    @property
    def short_code(self):
        obj = self.short_url
        return obj.short_code if obj else None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.short_urls.exists():
            ShortURL.objects.create(
                content_object=self,
                short_code=ShortURL.generate_code(self)
            )

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"post": self.slug})

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title
