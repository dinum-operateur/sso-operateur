from django.shortcuts import render
from oidc_provider.lib.endpoints.authorize import AuthorizeEndpoint

from sso.models import AutologinClient


def do_autologin_after_successful_login(request, user, client):
    if request.session.get("autologin_initiated", False):
        return None

    request.session["autologin_initiated"] = True

    authorize = AuthorizeEndpoint(request)
    authorize.client = client
    redirect_uri = authorize.create_response_uri()

    other_autologin_clients = AutologinClient.objects.exclude(oidc_client=client)
    if other_autologin_clients.exists():
        return render(
            request,
            "sso/oidc/multi-login.html",
            {"uri": redirect_uri, "other_autologin_clients": other_autologin_clients},
        )

    return None
