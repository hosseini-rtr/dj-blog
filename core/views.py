from django.shortcuts import get_object_or_404, redirect

from apps.common.models import ShortURL


def short_redirect(request, code):
    short = get_object_or_404(ShortURL, short_code=code)
    return redirect(short.content_object.get_absolute_url())
