import logging
from typing import Any, cast

import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.common.models import ContactMessage, ShortURL

logger = logging.getLogger(__name__)


def home_view(request):
    return render(
        request,
        "home/home.html",
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
            "message": _("Thanks for reaching out. I will get back to you soon."),
        }
    )
