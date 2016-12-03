from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.db.models import Q
from django.urls import reverse

from .models import Label, TodoList
from .forms import SearchForm, TodoForm


def sort_todolists(todolists):
    lists_with_due_date = []
    lists_without_due_date = []

    for todolist in todolists:
        if todolist.due_date:
            lists_with_due_date.append(todolist)
        else:
            lists_without_due_date.append(todolist)

    lists_with_due_date.sort(key=lambda todolist: todolist.due_date)
    lists_without_due_date.sort(key=lambda todolist: todolist.date_created)

    return lists_with_due_date + lists_without_due_date


class HomeView(View):

    def get(self, request):
        labels = Label.objects.all()
        todo_lists = TodoList.objects.all()

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

        pending_todos = todo_lists.filter(status=TodoList.PENDING)
        skipped_todos = pending_todos.filter(due_date__isnull=False,
                                             due_date__lt=datetime.now())
        # Update skipped todos to missed
        skipped_todos.update(status=TodoList.MISSED)
        missed_todos = todo_lists.filter(status=TodoList.MISSED)
        completed_todos = todo_lists.filter(status=TodoList.COMPLETED)

        todos_by_status = [
            {'status': TodoList.PENDING, 'todos': sort_todolists(pending_todos)},
            {'status': TodoList.COMPLETED, 'todos': sort_todolists(completed_todos)},
            {'status': TodoList.MISSED, 'todos': sort_todolists(missed_todos)}
        ]

        context = {
            'labels': labels,
            'todos_by_status': todos_by_status
        }
        return render(request, 'todoapp/home.html', context)


class CreateUpdateTodoView(View):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        form = TodoForm()

        if pk is not None:
            todo = get_object_or_404(TodoList, pk=pk)
            form = TodoForm(instance=todo)

        context = {
            'form': form
        }
        return render(request, 'todoapp/create_edit.html', context)

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        if pk is not None:
            todo = get_object_or_404(TodoList, pk=pk)
            form = TodoForm(request.POST, instance=todo)
        else:
            form = TodoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse('todoapp:home'))

        context = {
            'form': form
        }

        return render(request, 'todoapp/create_edit.html', context)


class DeleteTodoView(View):

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        todo = get_object_or_404(TodoList, pk=pk)
        todo.delete()
        return redirect(reverse('todoapp:home'))


class CompleteTodoView(View):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        todo = get_object_or_404(TodoList, pk=pk)

        todo.status = TodoList.COMPLETED
        todo.save()
        return redirect(reverse('todoapp:home'))
