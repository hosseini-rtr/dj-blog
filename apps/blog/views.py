from typing import Any

from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from apps.blog.forms import PostSearchForm
from apps.blog.models import Post


class HomeView(ListView):
    model = Post
    # template_name = "blog/index.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_template_names(self):
        if self.request.htmx:
            return "blog/components/post-list-elements.html"
        return "blog/index.html"


def post_detail(request, post):
    post = get_object_or_404(Post, slug=post, is_published=True)
    post.record_view(
        user=request.user if request.user.is_authenticated else None,
        viewer_ip=request.META.get('REMOTE_ADDR')
    )
    short_url = post.short_urls.first()
    return render(request, "blog/single.html", {'post': post,
                                                'short_url': short_url,
                                                })


class TagListView(ListView):
    model = Post
    paginate_by = 10
    context_object_name = "posts"

    def get_queryset(self):
        # return Post.objects.filter(tags__name=self.kwargs['tag'])
        return Post.objects.filter(tags__slug__in=[self.kwargs['tag']])

    def get_template_names(self):
        return 'blog/tags.html'


class PostSearchView(ListView):
    model = Post
    paginate_by = 10
    context_object_name = "posts"
    form_class = PostSearchForm

    def get_queryset(self) -> QuerySet[Any]:
        form = self.form_class(self.request.GET)

        if form.is_valid():
            return Post.objects.filter(title__icontains=form.cleaned_data['q'])
        return []

    def get_template_names(self):
        return "blog/search.html"
