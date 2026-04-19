from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from apps.blog.models import Post
from apps.common.models import ShortURL


class Command(BaseCommand):
    help = 'Create short URLs for existing posts'

    def handle(self, *args, **kwargs):
        posts = Post.objects.all()
        ct = ContentType.objects.get_for_model(Post)
        created_count = 0

        for post in posts:
            _, created = ShortURL.objects.get_or_create(
                content_type=ct,
                object_id=post.pk,
                defaults={'short_code': ShortURL.generate_code(post)}
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created short URL for: {post.title}")

        self.stdout.write(
            self.style.SUCCESS(f'Done! {created_count} short URLs created.')
        )
