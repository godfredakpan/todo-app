from django.shortcuts import render
from django.views import View

from .models import Label, ToDoList


class HomeView(View):

    def get(self, request):
        labels = Label.objects.all()
        pending_todos = ToDoList.objects.filter(status='P')
        missed_todos = ToDoList.objects.filter(status='M')
        completed_todos = ToDoList.objects.filter(status='C')

        context = {
            'labels': labels,
            'pending_todos': pending_todos,
            'missed_todos': missed_todos,
            'completed_todos': completed_todos
        }
        return render(request, 'todoapp/home.html', context)
