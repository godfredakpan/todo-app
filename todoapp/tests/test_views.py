from datetime import datetime

from django.test import Client, TestCase
from django.urls import reverse

from freezegun import freeze_time

from todoapp.models import Label, TodoList


class HomeViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.label_1 = Label.objects.create(name='label_one')
        self.label_2 = Label.objects.create(name='label_two')

        Label.objects.create(name='all')

        # Freezing time here to get specific date for date created
        # We need this to be able to sort todo_lists internally by date created for those without due date
        with freeze_time("2012-01-14 12:00:01"):
            due_date = datetime(2012, 8, 14, 3, 21, 34)
            TodoList.objects.create(title='todo_one', label=self.label_1, status=TodoList.PENDING)
            TodoList.objects.create(title='todo_five', label=self.label_1, status=TodoList.COMPLETED)
            TodoList.objects.create(title='todo_nine', label=self.label_1, status=TodoList.MISSED)
            TodoList.objects.create(title='todo_three', label=self.label_2, status=TodoList.PENDING, due_date=due_date)
            TodoList.objects.create(title='todo_seven', label=self.label_2, status=TodoList.COMPLETED, due_date=due_date)
            TodoList.objects.create(title='todo_eleven', label=self.label_2, status=TodoList.MISSED, due_date=due_date)

        with freeze_time("2012-01-15 12:00:01"):
            due_date = datetime(2012, 8, 15, 3, 21, 34)
            TodoList.objects.create(title='todo_two', label=self.label_1, status=TodoList.PENDING)
            TodoList.objects.create(title='todo_six', label=self.label_1, status=TodoList.COMPLETED)
            TodoList.objects.create(title='todo_ten', label=self.label_1, status=TodoList.MISSED)
            TodoList.objects.create(title='todo_four', label=self.label_2, status=TodoList.PENDING, due_date=due_date)
            TodoList.objects.create(title='todo_eight', label=self.label_2, status=TodoList.COMPLETED, due_date=due_date)
            TodoList.objects.create(title='todo_twelve', label=self.label_2, status=TodoList.MISSED, details='one',
                                    due_date=due_date)

    def test_home_page_route(self):
        """ Tests that home page route can be successfully loaded."""

        response = self.client.get(reverse('todoapp:home'))
        self.assertEqual(response.status_code, 200)

    def test_labels_are_available_on_homepage(self):
        """ Tests that the context contains labels. """

        response = self.client.get(reverse('todoapp:home'))
        self.assertQuerysetEqual(response.context['labels'],
                                 ['<Label: all>', '<Label: label_one>', '<Label: label_two>'],
                                 ordered=False)

    @freeze_time("2012-02-15 12:00:01")
    def test_todos_are_available_on_homepage(self):
        """Tests that the right amount of todos are available on the homepage."""

        response = self.client.get(reverse('todoapp:home'))
        todos_by_status = response.context['todos_by_status']
        self.assertEqual(len(todos_by_status[0]['todos']), 4)
        self.assertEqual(len(todos_by_status[1]['todos']), 4)
        self.assertEqual(len(todos_by_status[2]['todos']), 4)

    @freeze_time("2012-02-15 12:00:01")
    def test_todos_are_sorted_properly_on_homepage(self):
        """Tests that todos are sorted by due date or by date created if due date is not available."""
        response = self.client.get(reverse('todoapp:home'))
        pending_todos = response.context['todos_by_status'][0]['todos']
        self.assertEqual(pending_todos[0].title, 'todo_three')
        self.assertEqual(pending_todos[1].title, 'todo_four')
        self.assertEqual(pending_todos[2].title, 'todo_one')
        self.assertEqual(pending_todos[3].title, 'todo_two')

    @freeze_time("2012-02-15 12:00:01")
    def test_filter_by_selected_label(self):
        """ Tests that you can filter by selected label."""

        data = {'label': 'label_one'}
        response = self.client.get(reverse('todoapp:home'), data)
        todos_by_status = response.context['todos_by_status']

        self.assertEqual(len(todos_by_status[0]['todos']), 2)
        self.assertEqual(len(todos_by_status[1]['todos']), 2)
        self.assertEqual(len(todos_by_status[2]['todos']), 2)

        for status_column in todos_by_status:
            for todo in status_column['todos']:
                self.assertEqual(todo.label.name, 'label_one')

    @freeze_time("2012-02-15 12:00:01")
    def test_search_todo(self):
        """ Tests that you can search todolists. """
        data = {'q': 'one'}
        response = self.client.get(reverse('todoapp:home'), data)
        todos_by_status = response.context['todos_by_status']

        self.assertEqual(len(todos_by_status[0]['todos']), 2)
        self.assertEqual(len(todos_by_status[1]['todos']), 2)
        self.assertEqual(len(todos_by_status[2]['todos']), 3)

        for status_column in todos_by_status:
            for todo in status_column['todos']:
                self.assertIn('one', '{0},{1},{2}'.format(todo.title, todo.details, todo.label.name))


class CreateUpdateTodoViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        Label.objects.create(name='all')
        self.label_1 = Label.objects.create(name='label_one')

        self.todo_list = TodoList.objects.create(title='todo_one', label=self.label_1, status=TodoList.PENDING)
        self.todo_list2 = TodoList.objects.create(title='todo_two', label=self.label_1, status=TodoList.PENDING)

    def test_create_todo_route(self):
        """ Tests that create todo route can be loaded successfully."""
        response = self.client.get(reverse('todoapp:new_todo'))

        self.assertEqual(response.status_code, 200)

    def test_edit_todo_route(self):
        """ Tests that edit todo route can be loaded successfully."""
        data = {'pk': self.todo_list.id}
        response = self.client.get(reverse('todoapp:edit_todo', kwargs=data))

        self.assertEqual(response.status_code, 200)

    def test_create_todo(self):
        """ Tests that todolist can be created successfully."""
        data = {'title': 'todo_two', 'label': self.label_1.id, 'status': TodoList.PENDING}
        response = self.client.post(reverse('todoapp:new_todo'), data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(TodoList.objects.filter(title='todo_two').exists())
        self.assertContains(response, 'todo_two')

    def test_edit_todo(self):
        """ Tests that todolist can be edited successfully."""
        data = {'title': 'todo_one_edited', 'label': self.label_1.id, 'status': TodoList.PENDING}
        response = self.client.post(reverse('todoapp:edit_todo', kwargs={'pk': self.todo_list.id}),
                                     data, follow=True)

        self.todo_list.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.todo_list.title, 'todo_one_edited')
        self.assertContains(response, 'todo_one_edited')

    def test_delete_todo(self):
        """Tests that todolist can be deleted successfully."""
        response = self.client.post(reverse('todoapp:delete_todo', kwargs={'pk': self.todo_list2.id}),
                                    follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'todo_two')

    def test_complete_todo(self):
        """Tests that todolist can be marked as completed."""
        response = self.client.get(reverse('todoapp:complete_todo', kwargs={'pk': self.todo_list.id}),
                                   follow=True)

        self.todo_list.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.todo_list.status, TodoList.COMPLETED)

    def test_create_label(self):
        """Tests that you can create label successfully. """
        data = {'name': 'label_two'}
        response = self.client.post(reverse('todoapp:new_label'), data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'label_two')
