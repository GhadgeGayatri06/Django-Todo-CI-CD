
from django.test import TestCase
from django.urls import reverse
from .models import Task


class TodoAppTests(TestCase):

    # Test 1: Home page loads successfully
    def test_home_page(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)

    # Test 2: Create a new task
    def test_create_task(self):
        response = self.client.post(
            reverse('home'),
            {'title': 'Complete Django Project'}
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Task.objects.filter(
                title='Complete Django Project'
            ).exists()
        )

    # Test 3: Complete a task
    def test_complete_task(self):
        task = Task.objects.create(
            title='Learn Jenkins'
        )

        response = self.client.post(
            reverse('complete_task', args=[task.id])
        )

        task.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertTrue(task.completed)
        self.assertIsNotNone(task.completed_at)

    # Test 4: Delete a task
    def test_delete_task(self):
        task = Task.objects.create(
            title='Delete This Task'
        )

        response = self.client.post(
            reverse('delete_task', args=[task.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Task.objects.filter(id=task.id).exists()
        )

    # Test 5: Analytics calculation
    def test_task_analytics(self):
        Task.objects.create(
            title='Completed Task',
            completed=True
        )

        Task.objects.create(
            title='Pending Task',
            completed=False
        )

        response = self.client.get(reverse('home'))

        self.assertEqual(response.context['total_tasks'], 2)
        self.assertEqual(response.context['completed_tasks'], 1)
        self.assertEqual(response.context['pending_tasks'], 1)
        self.assertEqual(response.context['completion_percentage'], 50.0)
