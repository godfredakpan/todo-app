from django.conf.urls import url
from .views import HomeView, CreateView


app_name = 'todoapp'
urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^create$', CreateView.as_view(), name='create'),
]
