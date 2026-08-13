from django.shortcuts import render

from apps.connect.models import Link

# Create your views here.


def connect(request):
    links = Link.objects.filter(is_active=True)

    return render(
        request,
        "connect/index.html",
        {"links": links},
    )
