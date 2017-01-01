from django.conf.urls import url
from .views import (HomeView, CreateUpdateTodoView, DeleteTodoView,
                    CompleteTodoView, CreateLabelView,)


app_name = 'todoapp'
urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^new$', CreateUpdateTodoView.as_view(), name='new_todo'),
    url(r'^(?P<pk>[0-9]+)/edit$',
        CreateUpdateTodoView.as_view(),
        name='edit_todo'),
    url(r'^(?P<pk>[0-9]+)/delete$',
        DeleteTodoView.as_view(),
        name='delete_todo'),
    url(r'^(?P<pk>[0-9]+)/complete$',
        CompleteTodoView.as_view(),
        name='complete_todo'),
    url(r'^new_label$', CreateLabelView.as_view(), name='new_label'),
]
