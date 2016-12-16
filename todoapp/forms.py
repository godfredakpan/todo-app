from django import forms
from django.forms import ModelForm

from .models import TodoList, Label


class SearchForm(forms.Form):
    q = forms.CharField(max_length=255)


class DateInput(forms.DateInput):
    input_type = 'date'


class TodoForm(ModelForm):

    class Meta:
        model = TodoList
        fields = ['title', 'details', 'due_date', 'label', 'status']
        widgets = {
            'due_date': DateInput(),
            'details': forms.Textarea(
                attrs={'class': 'materialize-textarea'}
            )
        }

class LabelForm(ModelForm):

    class Meta:
        model = Label
        fields = ['name']