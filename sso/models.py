from django.contrib.auth.models import AbstractUser
from django.db import models
from oidc_provider.models import Client as OidcClient


class User(AbstractUser):
    pass


class AutologinClient(models.Model):
    enable_autologin = models.BooleanField(
        default=True,
        verbose_name="Activer l’autologin ?",
        help_text=(
            "En cas de succès du login sur un client autologin, activer la connexion "
            "automatique pour tous les autres clients autologin"
        ),
    )

    autologin_url = models.URLField(
        "URL pour l’autologin",
        blank=True,
        help_text="URL à insérer dans l’iframe qui servira à faire l'autologin",
    )

    oidc_client = models.OneToOneField(OidcClient, on_delete=models.CASCADE)
