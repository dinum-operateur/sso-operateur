from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from sso.models import AutologinClient


def view_index(request):
    return render(request, "sso/accueil.html")


def view_accessibilite(request):
    return render(request, "sso/accessibilite.html")


@login_required
def view_multilogin(request):
    """
    View to log in all oidc autologin clients at once.
    Partially similar to hook do_autologin_after_successful_login
    """
    # avoid endless loop in iframes, like the hook
    request.session["autologin_initiated"] = True
    # get all autologin clients, unlike the hook
    autologin_clients = AutologinClient.objects.all()

    response = render(
        request,
        "sso/oidc/multi-login.html",
        {"uri": "", "other_autologin_clients": autologin_clients},
    )
    # allow all clients to be displayed in iframes
    response._csp_update = {
        "frame-src": " ".join(c.autologin_url for c in autologin_clients)
    }
    return response
