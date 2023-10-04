from django.shortcuts import render
from django.utils.http import url_has_allowed_host_and_scheme


def view_index(request):
    return render(request, "sso/accueil.html")


def view_accessibilite(request):
    return render(request, "sso/accessibilite.html")


def sanitize_next_url_value(request):
    next = request.POST.get("next", request.GET.get("next"))

    if not url_has_allowed_host_and_scheme(
        url=next,
        allowed_hosts={
            request.get_host(),
        },
        require_https=request.is_secure(),
    ):
        return ""

    return next


def view_login(request):
    return render(
        request,
        "registration/login.html",
        {"user": request.user, "next": sanitize_next_url_value(request)},
    )
