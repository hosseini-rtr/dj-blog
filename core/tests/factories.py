import factory
from django.contrib.auth.models import User

from apps.blog.models import Post


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    password = "test"
    username = "test"
    is_superuser = True
    is_staff = True


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = "X"
    subtitle = "X"
    slug = "X"
    author = factory.SubFactory(UserFactory)
    content = "X"
    is_published = True

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.tags.add(*extracted)
