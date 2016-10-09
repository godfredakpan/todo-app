from django.test import TestCase
from django.core.exceptions import ValidationError

from todoapp.models import Label


class LabelTestCase(TestCase):
    """Tests Label method."""

    def setUp(self):
        self.label1 = Label.objects.create(name='Chore')
        self.label2 = Label.objects.create(name='Work')

    def test_duplicate_label_cannot_be_saved(self):
        label = Label(name='chore')

        self.assertRaises(ValidationError, label.save)

    def test_existing_label_can_be_edited_and_saved(self):
        self.label1.name = 'travel'
        self.label1.save()

        self.assertEqual(self.label1.name, 'travel')

    def test_existing_label_cannot_be_edited_with_another_label_name(self):
        self.label1.name = 'work'

        self.assertRaises(ValidationError, self.label1.save)
