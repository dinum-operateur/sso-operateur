from django.test import TestCase
from django.urls import resolve

from sso import views


class TestStaticPages(TestCase):
    def test_index_url_calls_correct_view(self):
        match = resolve("/")
        self.assertEqual(match.func, views.view_index)

    def test_index_url_calls_right_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "sso/accueil.html")

    def test_index_response_contains_welcome_message(self):
        response = self.client.get("/")
        self.assertContains(response, "Single Sign-On Opérateur")
        self.assertContains(response, "Suite numérique collaborative")

    def test_a11y_url_calls_correct_view(self):
        match = resolve("/accessibilite/")
        self.assertEqual(match.func, views.view_accessibilite)

    def test_a11y_url_calls_right_template(self):
        response = self.client.get("/accessibilite/")
        self.assertTemplateUsed(response, "sso/accessibilite.html")

    def test_a11y_response_contains_title(self):
        response = self.client.get("/accessibilite/")
        self.assertContains(response, "Déclaration d’accessibilité")

    def test_login_page_is_not_broken(self):
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Connexion")
        self.assertTemplateUsed(response, "registration/login.html")


class TestDSFR(TestCase):
    def test_dsfr_is_correctly_loaded(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "dsfr/global_css.html")
        self.assertTemplateUsed(response, "dsfr/favicon.html")
        self.assertTemplateUsed(response, "dsfr/skiplinks.html")
        self.assertTemplateUsed(response, "dsfr/header.html")
        self.assertTemplateUsed(response, "dsfr/theme_modale.html")
        self.assertTemplateUsed(response, "dsfr/breadcrumb.html")
        self.assertTemplateUsed(response, "dsfr/global_js.html")
