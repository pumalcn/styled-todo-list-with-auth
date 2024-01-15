from django.test import TestCase
from django.contrib.auth.models import User
from .models import Task
from django.urls import reverse, resolve
from .views import TaskList, TaskCreate, TaskDetail, TaskUpdate, TaskDeleteView

class ModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('test_user', 'test@example.com', 'Test_password123')
        self.task = Task.objects.create(user=self.user, title='Test Task', description='Test Description')

    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'Test Description')
        self.assertFalse(self.task.complete)
        self.assertEqual(str(self.task), 'Test Task')


class ViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='Test_password123')
        self.client.login(username='test_user', password='Test_password123')
        Task.objects.create(user=self.user, title='Test Task')

    def test_task_list_view(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    def test_task_create_view(self):
        response = self.client.post(reverse('task-create'), {'title': 'New Task', 'description': 'New Description'})
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        new_task = Task.objects.filter(title='New Task').first()
        self.assertIsNotNone(new_task, 'New Task was not created')
        self.assertEqual(new_task.title, 'New Task')


class UrlsTest(TestCase):

    def test_task_list_url(self):
        url = reverse('tasks')
        self.assertEqual(resolve(url).func.view_class, TaskList)

    def test_task_create_url(self):
        url = reverse('task-create')
        self.assertEqual(resolve(url).func.view_class, TaskCreate)

    def test_task_detail_url(self):
        url = reverse('task', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, TaskDetail)

    def test_task_update_url(self):
        url = reverse('task-update', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, TaskUpdate)

    def test_task_delete_url(self):
        url = reverse('task-delete', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, TaskDeleteView)