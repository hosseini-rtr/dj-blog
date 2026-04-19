from io import BytesIO

from celery import shared_task
from django.core.files.base import ContentFile
from PIL import Image

from apps.blog.models import Post


@shared_task
def generate_thumbnail(post_id):
    post = Post.objects.get(id=post_id)
    if not post.image:
        return

    img = Image.open(post.image)
    img.thumbnail((1200, 630), Image.Resampling.LANCZOS)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    buffer = BytesIO()
    img.save(buffer, format='JPEG', quality=85, optimize=True)
    buffer.seek(0)

    filename = f'thumb_{post.image.name.split('/')[-1]}'
    post.thumbnail.save(filename, ContentFile(buffer.read()), save=True)

    return f"Thumbnail created for post {post_id}"
