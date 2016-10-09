from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


class Label(models.Model):
    """Model that defines app labels."""

    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True, editable=False)

    def raise_validation_error(self, value):
        raise ValidationError(_("This label already exists."))

    def clean(self):
        self.slug = slugify(self.name)

        if Label.objects.filter(slug=self.slug).exists():
            # If pk exists, object exists in db and is being edited by user.
            if self.pk:
                try:
                    self.validate_unique()
                except ValidationError:
                    self.raise_validation_error(self.slug)
            else:
                self.raise_validation_error(self.slug)

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ToDoList(models.Model):
    """Core model of the app defining the ToDo list."""

    title = models.CharField(max_length=150, unique=True)
    details = models.TextField(blank=True)
    due_date = models.DateTimeField(blank=True)
    labels = models.ForeignKey(Label)

    PENDING = 'P'
    COMPLETED = 'C'
    MISSED = 'M'
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (MISSED, 'Missed'),
    )

    status = models.CharField(max_length=2, choices=STATUS_CHOICES,
                              default=PENDING)

    def __str__(self):
        return self.title
