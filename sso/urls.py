from django.urls import path

from sso import views

urlpatterns = [
    path("", views.view_index, name="index"),
    path("oidc/multi-login/", views.view_multilogin, name="multi-login"),
    path("accessibilite/", views.view_accessibilite, name="accessibilite"),
    path("accounts/login/", views.view_login, name="login"),
    path("accounts/logout/", views.view_logout, name="logout"),
]
