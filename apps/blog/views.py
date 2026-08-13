from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET
from django.views.generic import ListView

from apps.blog.forms import PostSearchForm
from apps.blog.models import Post


class PublishedPostListMixin:
    def get_queryset(self):
        return Post.objects.filter(is_published=True)


class HomeView(PublishedPostListMixin, ListView):
    context_object_name = "posts"
    paginate_by = 10

    def get_template_names(self):
        if self.request.htmx:
            return "blog/components/post-list-elements.html"

        return "blog/index.html"


def post_detail(request, post):
    post = get_object_or_404(
        Post.objects.prefetch_related(
            "tags",
            "comments",
        ),
        slug=post,
        is_published=True,
    )

    post.record_view(
        user=request.user if request.user.is_authenticated else None,
        viewer_ip=request.META.get("REMOTE_ADDR"),
    )

    return render(
        request,
        "blog/single.html",
        {
            "post": post,
            "short_url": post.short_url,
        },
    )


class TagListView(PublishedPostListMixin, ListView):
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                tags__slug=self.kwargs["tag"],
            )
        )

    def get_template_names(self):
        return ["blog/tags.html"]


class PostSearchView(PublishedPostListMixin, ListView):
    context_object_name = "posts"
    paginate_by = 10
    form_class = PostSearchForm

    def get_queryset(self):
        form = self.form_class(self.request.GET)

        if not form.is_valid():
            return Post.objects.none()

        query = form.cleaned_data["q"]

        return (
            super()
            .get_queryset()
            .filter(Q(title__icontains=query) | Q(subtitle__icontains=query))
        )

    def get_template_names(self):
        return ["blog/search.html"]


@require_GET
def latest_posts_api(request):
    posts = Post.objects.filter(is_published=True).order_by("-created_at")[:5]

    data = [
        {
            "title": post.title,
            "slug": post.slug,
            "thumbnail": (post.thumbnail.url if post.thumbnail else None),
            "lang": post.lang,
            "date": post.created_at.strftime("%Y-%m-%d"),
        }
        for post in posts
    ]

    return JsonResponse(data, safe=False)
