from django.shortcuts import render
from django.views import View
from django.db.models import Q

from .models import Label, TodoList
from .forms import SearchForm


class HomeView(View):

    def get(self, request):
        labels = Label.objects.all()
        todo_lists = TodoList.objects.all().order_by('due_date')

        selected_label = request.GET.get('label')
        if selected_label:
            todo_lists = todo_lists.filter(label__name=selected_label)

        q = request.GET.get('q')
        if q:
            form = SearchForm(request.GET)
            if form.is_valid():
                q = form.cleaned_data.get('q')
                todo_lists = todo_lists.filter(Q(title__icontains=q) |
                                               Q(details__icontains=q) |
                                               Q(label__name__icontains=q)
                                               )
            else:
                form = SearchForm()

        pending_todos = todo_lists.filter(status=TodoList.PENDING)
        missed_todos = todo_lists.filter(status=TodoList.MISSED)
        completed_todos = todo_lists.filter(status=TodoList.COMPLETED)

        todos_by_status = [
            {'status': TodoList.PENDING, 'todos': pending_todos},
            {'status': TodoList.COMPLETED, 'todos': completed_todos},
            {'status': TodoList.MISSED, 'todos': missed_todos}
        ]

        context = {
            'labels': labels,
            'todos_by_status': todos_by_status
        }
        return render(request, 'todoapp/home.html', context)


class CreateView(View):

    def get(self, request):
        return render(request, 'todoapp/create_edit.html', {})
