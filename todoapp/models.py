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


# class ToDoListManager(models.Manager):

#     def due_date_to_num(self, todo):
#         if todo.due_date is None:
#             return 0
#         return todo.due_date.timestamp()

#     def order_by_due_date(self):
#         ordered = sorted(self.get_queryset(),
#                          key=self.due_date_to_num,
#                          reverse=False)
#         return ordered


class TodoList(models.Model):
    """Core model of the app defining the ToDo list."""

    title = models.CharField(max_length=150, unique=True)
    details = models.TextField(blank=True)
    due_date = models.DateTimeField(blank=True, null=True)
    label = models.ForeignKey(Label)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    # objects = models.Manager()
    # custom_manager = ToDoListManager()

    PENDING = 'Pending'
    COMPLETED = 'Completed'
    MISSED = 'Missed'
    STATUS_CHOICES = (
        (PENDING, PENDING),
        (COMPLETED, COMPLETED),
        (MISSED, MISSED),
    )

    status = models.CharField(max_length=50, choices=STATUS_CHOICES,
                              default=PENDING)

    def __str__(self):
        return self.title
