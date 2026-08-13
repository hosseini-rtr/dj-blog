from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from .views import contact_view, home_view, link_page, short_redirect

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    # Redirect non-prefixed blog root to the language-prefixed path
    path("blog/", RedirectView.as_view(url=f"/{settings.LANGUAGE_CODE}/blog/")),
]

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", home_view, name="home"),
    path("contact/", contact_view, name="contact"),
    path("blog/", include("apps.blog.urls")),
    path("link/", link_page, name="link_page"),
    path("s/<str:code>", short_redirect, name="short_url"),
)

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
