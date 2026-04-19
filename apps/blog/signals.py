from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.blog.models import Post
from apps.blog.tasks import generate_thumbnail


@receiver(post_save, sender=Post)
def create_thumbnail(sender, instance, created, **kwarg):
    if instance.image and not instance.thumbnail:
        generate_thumbnail.delay(instance.id)
