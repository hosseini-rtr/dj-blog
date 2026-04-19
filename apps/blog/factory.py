import random

import factory
from django.contrib.auth.models import User
from factory.faker import faker

from apps.blog.models import Post

FAKE = faker.Faker()

CODE_SNIPPETS = [
    "def hello():\n    return 'world'",
    "for i in range(10):\n    print(i)",
    "class MyModel(models.Model):\n    name = models.CharField(max_length=100)",
    "qs = Post.objects.filter(lang='en').order_by('-created_at')",
]


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Faker("sentence", nb_words=12)
    subtitle = factory.Faker("sentence", nb_words=12)
    slug = factory.Faker("slug")
    author = factory.LazyFunction(
        lambda: User.objects.get_or_create(username="admin")[0])
    image = factory.django.ImageField(color='blue', width=1200, height=630)
    thumbnail = factory.django.ImageField(color='gray', width=400, height=300)
    lang = factory.LazyFunction(lambda: random.choice(['en', 'fa', 'it']))

    @factory.lazy_attribute
    def allow_comments(self):
        return False

    @factory.lazy_attribute
    def content(self):
        sections = []
        for i in range(3):
            sections.append(f"## {FAKE.sentence(nb_words=5)}\n")
            sections.append(FAKE.paragraph(nb_sentences=5))
            sections.append(f"```python\n{random.choice(CODE_SNIPPETS)}\n```")

            items = "\n".join(f"- {FAKE.sentence()}" for _ in range(4))
            sections.append(items)
            sections.append(f"> {FAKE.sentence(nb_words=10)}")

        return "\n\n".join(sections)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.tags.add(extracted)
        else:
            self.tags.add(
                "Python",
                "Back end",
                "Django",
                "Database",
                "ORM",
                "Deployment",
                "LLM",
                "AI",
                "BCI"
            )
