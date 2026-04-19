def post_image_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'posts/images/{instance.slug}.{ext}'


def post_thumbnail_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'posts/thumbnails/thumb_{instance.slug}.{ext}'
