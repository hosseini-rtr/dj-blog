from django.urls import path

from apps.blog import views

app_name = 'blog'
urlpatterns = [
    path("", views.HomeView.as_view(), name='home'),
    path("post/<slug:post>/", views.post_detail, name="post_detail"),
    path("search/", views.PostSearchView.as_view(), name="search"),
    path("tag/<slug:tag>/", views.TagListView.as_view(), name="by_tag"),
]
