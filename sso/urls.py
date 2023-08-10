from django.urls import include, path

from sso import views

urlpatterns = [
    path("", views.view_index, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accessibilite/", views.view_accessibilite, name="accessibilite"),
]
