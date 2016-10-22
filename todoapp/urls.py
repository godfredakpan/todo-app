from django.conf.urls import url
from .views import HomeView, CreateUpdateTodoView


app_name = 'todoapp'
urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^new$', CreateUpdateTodoView.as_view(), name='new_todo'),
    url(r'^(?P<pk>[0-9]+)/edit$',
        CreateUpdateTodoView.as_view(),
        name='edit_todo'),
]
