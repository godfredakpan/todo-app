from django.test import Client, TestCase
from django.urls import reverse

from todoapp.models import Label


class HomeViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_home_page_route(self):
        """ Tests that home page route can be successfully loaded."""

        response = self.client.get(reverse('todoapp:home'))
        self.assertEqual(response.status_code, 200)

    def test_labels(self):
        """ Tests that the context contains labels. """
        Label.objects.create(name='all')
        response = self.client.get(reverse('todoapp:home'))
        self.assertQuerysetEqual(response.context['labels'], ['<Label: all>'])