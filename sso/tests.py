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

    def test_a11y_url_calls_correct_view(self):
        match = resolve("/accessibilite/")
        self.assertEqual(match.func, views.view_accessibilite)

    def test_a11y_url_calls_right_template(self):
        response = self.client.get("/accessibilite/")
        self.assertTemplateUsed(response, "sso/accessibilite.html")

    def test_a11y_response_contains_title(self):
        response = self.client.get("/accessibilite/")
        self.assertContains(response, "Déclaration d’accessibilité")
