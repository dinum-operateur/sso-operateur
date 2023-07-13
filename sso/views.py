from django.shortcuts import render


def view_index(request):
    return render(request, "sso/accueil.html")


def view_accessibilite(request):
    return render(request, "sso/accessibilite.html")
