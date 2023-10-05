import logging

from django.shortcuts import render
from oidc_provider.lib.endpoints.authorize import AuthorizeEndpoint

from sso.models import AutologinClient

logger = logging.getLogger(__name__)


def do_autologin_after_successful_login(request, user, client):
    logger.info(user)
    if request.session.get("autologin_initiated", False):
        return None

    # mandatory to avoid endless Loop
    request.session["autologin_initiated"] = True

    authorize = AuthorizeEndpoint(request)
    authorize.client = client
    redirect_uri = authorize.create_response_uri()

    other_autologin_clients = AutologinClient.objects.exclude(oidc_client=client)
    if other_autologin_clients.exists():
        response = render(
            request,
            "sso/oidc/multi-login.html",
            {"uri": redirect_uri, "other_autologin_clients": other_autologin_clients},
        )
        # allow all needed clients to be displayed in iframes!
        response._csp_update = {
            "frame-src": "'self' "
            + " ".join(c.autologin_url for c in other_autologin_clients)
        }
        return response

    return None
