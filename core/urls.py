from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from .views import (
    agent_txt,
    contact_view,
    home_view,
    link_page,
    llms_txt,
    robots_txt,
    short_redirect,
    sitemap_xml,
    teacher_links,
)

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("robots.txt", robots_txt, name="robots"),
    path("sitemap.xml", sitemap_xml, name="sitemap"),
    path("llms.txt", llms_txt, name="llms"),
    path("agent.txt", agent_txt, name="agent"),
    # Redirect non-prefixed blog root to the language-prefixed path
    path(
        "blog/",
        RedirectView.as_view(url=f"/{settings.LANGUAGE_CODE}/blog/"),
    ),
]

urlpatterns += i18n_patterns(
    path("red-line/", admin.site.urls),
    path("", home_view, name="home"),
    path("contact/", contact_view, name="contact"),
    path("blog/", include("apps.blog.urls")),
    path("afshin/", teacher_links, name="afshin_page"),
    path("link/", link_page, name="link_page"),
    path("s/<str:code>", short_redirect, name="short_url"),
    path("connect/", link_page, name="connect"),
)

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
