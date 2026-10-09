import logging
from typing import Any, cast

import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.blog.models import Post

from apps.common.models import ContactMessage, ShortURL

logger = logging.getLogger(__name__)


def home_view(request):
    return render(
        request,
        "home/home.html",
    )


def robots_txt(request):
    sitemap_url = request.build_absolute_uri(reverse("sitemap"))
    return HttpResponse(
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /red-line/\n"
        "Disallow: /ckeditor5/\n"
        "Disallow: /i18n/\n"
        f"Sitemap: {sitemap_url}\n",
        content_type="text/plain",
    )


def sitemap_xml(request):
    urls = [
        (request.build_absolute_uri(reverse("home")), None),
        (request.build_absolute_uri(reverse("blog:home")), None),
        (request.build_absolute_uri(reverse("connect")), None),
        (request.build_absolute_uri(reverse("afshin_page")), None),
    ]
    urls.extend(
        (
            request.build_absolute_uri(post.get_absolute_url()),
            post.updated_at,
        )
        for post in Post.objects.filter(is_published=True).only(
            "slug", "updated_at"
        )
    )

    entries = []
    for url, lastmod in urls:
        lastmod_tag = (
            f"<lastmod>{lastmod.date().isoformat()}</lastmod>"
            if lastmod
            else ""
        )
        entries.append(f"<url><loc>{url}</loc>{lastmod_tag}</url>")

    return HttpResponse(
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join(entries)
        + "</urlset>",
        content_type="application/xml",
    )


def llms_txt(request):
    return HttpResponse(
        "# Seyed Hossein Hosseini\n\n"
        "Software engineer writing about backend systems, AI, architecture, "
        "Python, and technically difficult products.\n\n"
        "## Important pages\n"
        f"- Home: {request.build_absolute_uri(reverse('home'))}\n"
        f"- Blog: {request.build_absolute_uri(reverse('blog:home'))}\n"
        f"- Contact: {request.build_absolute_uri(reverse('contact'))}\n",
        content_type="text/plain",
    )


def agent_txt(request):
    return HttpResponse(
        "# Agent access policy\n\n"
        "Public pages may be crawled and summarized with attribution to Seyed "
        "Hossein Hosseini. Do not crawl admin, editor, language-action, or "
        "private endpoints. Prefer canonical URLs and respect robots.txt.\n",
        content_type="text/plain",
    )


def home(request):
    return home_view(request)


def short_redirect(request, code):
    short = get_object_or_404(ShortURL, short_code=code)
    content_object = cast(Any, short.content_object).get_absolute_url()
    return redirect(content_object)


def link_page(request):
    # Something like linktree
    return render(request, "connect/index.html")


def teacher_links(request):
    return render(request, "connect/afshin.html")


def _slack_notify(name: str, email: str, subject: str) -> None:
    webhook_url = getattr(settings, "SLACK_WEBHOOK_URL", "")
    if not webhook_url:
        return

    payload = {"text": f"New message from {name} <{email}>: {subject}"}
    try:
        requests.post(webhook_url, json=payload, timeout=5)
    except requests.RequestException:
        logger.warning(
            "Slack notification failed for contact message",
            exc_info=True,
        )


@require_POST
def contact_view(request):
    name = (request.POST.get("name") or "").strip()
    email = (request.POST.get("email") or "").strip()
    subject = (request.POST.get("subject") or "Website contact").strip()
    message = (request.POST.get("message") or "").strip()

    if not all([name, email, message]):
        return JsonResponse(
            {
                "success": False,
                "message": _("Please fill out all required fields."),
            },
            status=400,
        )

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse(
            {
                "success": False,
                "message": _("Please enter a valid email address."),
            },
            status=400,
        )

    ContactMessage.objects.create(
        name=name,
        email=email,
        subject=subject,
        message=message,
    )
    _slack_notify(name=name, email=email, subject=subject)

    return JsonResponse(
        {
            "success": True,
            "message": _(
                "Thanks for reaching out. I will get back to you soon."
            ),
        }
    )
