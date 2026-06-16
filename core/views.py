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


HOME_CONTEXT = {
    "hero": {
        "name": _("Seyed Hossein Hosseini"),
        "initials": _("SHH"),
        "roles": [
            _("Backend Engineer"),
            _("AI/ML Researcher"),
            _("Systems Architect"),
        ],
        "tagline": _(
            "Building resilient platforms, applied intelligence, and "
            "interfaces with a strong sense of motion."
        ),
        "primary_cta": _("View Projects"),
        "secondary_cta": _("Contact Me"),
        "eyebrow": _("Personal homepage and work journal"),
    },
    "about": {
        "title": _("About Me"),
        "bio": _(
            "I design dependable backend systems, practical AI workflows, "
            "and product experiences that stay fast under pressure. This "
            "page is sample content and is ready for your real bio, metrics, "
            "and case studies."
        ),
        "stats": [
            {"value": 6, "label": _("Years of Experience")},
            {"value": 28, "label": _("Projects Shipped")},
            {"value": 4, "label": _("Research Papers")},
            {"value": 12, "label": _("Open Source Repos")},
        ],
    },
    "resume": {
        "title": _("Resume"),
        "tabs": [
            {"id": "experience", "label": _("Experience")},
            {"id": "education", "label": _("Education")},
            {"id": "certificates", "label": _("Certificates")},
            {"id": "skills", "label": _("Skills")},
        ],
        "experience": [
            {
                "role": _("Senior Backend Engineer"),
                "org": _("Northstar Labs"),
                "period": _("2023 - Present"),
                "bullets": [
                    _(
                        "Led API and data platform work for products that "
                        "serve thousands of daily requests with predictable "
                        "latency."
                    ),
                    _(
                        "Introduced background job orchestration, "
                        "observability, and deployment hygiene across the "
                        "stack."
                    ),
                    _(
                        "Partnered with product and research teams to turn "
                        "prototypes into shipping systems."
                    ),
                ],
            },
            {
                "role": _("Machine Learning Engineer"),
                "org": _("Signal Forge"),
                "period": _("2020 - 2023"),
                "bullets": [
                    _(
                        "Built training pipelines, feature stores, and "
                        "evaluation tooling for applied NLP and ranking "
                        "systems."
                    ),
                    _(
                        "Reduced experiment turnaround time by automating "
                        "dataset versioning and reproducibility checks."
                    ),
                ],
            },
        ],
        "education": [
            {
                "role": _("M.S. in Computer Science"),
                "org": _("Tehran Tech University"),
                "period": _("2018 - 2020"),
                "bullets": [
                    _(
                        "Focused on distributed systems, information "
                        "retrieval, and applied machine learning."
                    ),
                    _(
                        "Completed a thesis on efficient model serving under "
                        "constrained infrastructure."
                    ),
                ],
            },
            {
                "role": _("B.S. in Software Engineering"),
                "org": _("Azad University"),
                "period": _("2014 - 2018"),
                "bullets": [
                    _(
                        "Built a foundation in algorithms, databases, and "
                        "software architecture."
                    ),
                ],
            },
        ],
        "certificates": [
            {
                "name": _("Cloud Architecture Professional"),
                "issuer": _("Cloud Guild"),
                "date": _("2024"),
            },
            {
                "name": _("Applied Machine Learning Specialization"),
                "issuer": _("Deep Learn Academy"),
                "date": _("2023"),
            },
            {
                "name": _("Advanced Python Systems"),
                "issuer": _("Open Source Institute"),
                "date": _("2022"),
            },
        ],
        "skills": [
            {
                "category": _("Backend"),
                "items": [
                    {"name": _("Python"), "percent": 96},
                    {"name": _("Django"), "percent": 94},
                    {"name": _("PostgreSQL"), "percent": 88},
                    {"name": _("Redis"), "percent": 84},
                    {"name": _("Celery"), "percent": 82},
                ],
            },
            {
                "category": _("AI/ML"),
                "items": [
                    {"name": _("PyTorch"), "percent": 86},
                    {"name": _("Transformers"), "percent": 83},
                    {"name": _("scikit-learn"), "percent": 89},
                ],
            },
            {
                "category": _("DevOps"),
                "items": [
                    {"name": _("Docker"), "percent": 91},
                    {"name": _("Nginx"), "percent": 84},
                    {"name": _("Linux"), "percent": 90},
                    {"name": _("Git"), "percent": 95},
                ],
            },
        ],
    },
    "services": [
        {
            "title": _("Backend Architecture"),
            "description": _(
                "Designing reliable APIs, data models, queues, and "
                "deployment flows for growing products."
            ),
        },
        {
            "title": _("AI Integration"),
            "description": _(
                "Shipping practical ML features that fit real product "
                "constraints, metrics, and latency budgets."
            ),
        },
        {
            "title": _("Technical Consulting"),
            "description": _(
                "Helping teams make better system decisions, from "
                "architecture reviews to delivery plans."
            ),
        },
    ],
    "projects": [
        {
            "name": _("Atlas Queue"),
            "tags": ["backend", "oss"],
            "stack": ["Django", "Celery", "PostgreSQL"],
            "description": _(
                "A resilient task orchestration service with retries, "
                "visibility, and operator-friendly tooling."
            ),
            "github": "https://github.com/example/atlas-queue",
            "live": "https://example.com/atlas-queue",
        },
        {
            "name": _("PaperSignal"),
            "tags": ["ai", "research"],
            "stack": ["PyTorch", "Transformers", "FastAPI"],
            "description": _(
                "A research companion that clusters papers, extracts "
                "insights, and surfaces related work instantly."
            ),
            "github": "https://github.com/example/papersignal",
            "live": "https://example.com/papersignal",
        },
        {
            "name": _("Vector Harbor"),
            "tags": ["backend", "ai"],
            "stack": ["Django", "Redis", "scikit-learn"],
            "description": _(
                "A semantic search backend for product catalogs, knowledge "
                "bases, and internal docs."
            ),
            "github": "https://github.com/example/vector-harbor",
            "live": "https://example.com/vector-harbor",
        },
        {
            "name": _("Open Orbit Toolkit"),
            "tags": ["oss"],
            "stack": ["Python", "GitHub Actions", "Docker"],
            "description": _(
                "A small open-source set of deployment helpers, release "
                "scripts, and monitoring snippets."
            ),
            "github": "https://github.com/example/open-orbit-toolkit",
            "live": "https://example.com/open-orbit-toolkit",
        },
    ],
    "groups": [
        {
            "name": _("Autonomous Vehicle Research Team"),
            "role": _("Backend and data systems contributor"),
            "description": _(
                "Supporting telemetry ingestion, experiment tracking, and "
                "research dashboards for autonomy work."
            ),
        },
        {
            "name": _("Applied Intelligence Studio"),
            "role": _("Systems architect"),
            "description": _(
                "Shaping the infra and internal tools that keep experiments "
                "reproducible and fast to review."
            ),
        },
        {
            "name": _("Founders Collective"),
            "role": _("Technical advisor"),
            "description": _(
                "Helping product teams translate ideas into secure, "
                "maintainable systems with clear delivery paths."
            ),
        },
    ],
    "contact": {
        "title": _("Contact"),
        "intro": _(
            "If you want to talk about backend systems, AI experiments, "
            "or a product that needs a sturdier foundation, send a "
            "message."
        ),
    },
}


def _home_context():
    hero_name = str(HOME_CONTEXT["hero"]["name"])
    context = dict(HOME_CONTEXT)
    context["hero"] = dict(HOME_CONTEXT["hero"])
    context["hero"]["letters"] = list(hero_name)
    return context


def home_view(request):
    return render(request, "home/home.html", _home_context())


def home(request):
    return home_view(request)


def short_redirect(request, code):
    short = get_object_or_404(ShortURL, short_code=code)
    content_object = cast(Any, short.content_object).get_absolute_url()
    return redirect(content_object)


def link_page(request):
    # Something like linktree
    return JsonResponse({"message": "This is the link page!"})


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
    subject = (request.POST.get("subject") or "").strip()
    message = (request.POST.get("message") or "").strip()

    if not all([name, email, subject, message]):
        return JsonResponse(
            {
                "status": "error",
                "message": _(
                    "Please fill out all required fields."
                ),
            },
            status=400,
        )

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse(
            {
                "status": "error",
                "message": _(
                    "Please enter a valid email address."
                ),
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

    return JsonResponse({"status": "ok"})
