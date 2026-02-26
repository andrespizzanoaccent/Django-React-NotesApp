from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Category, Note


class CategoryAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category_data = {'name': 'Work', 'metadata': {'color': 'blue'}}
        self.category = Category.objects.create(**self.category_data)

    def test_create_category(self):
        response = self.client.post('/api/categories/', {'name': 'Personal', 'metadata': {'color': 'red'}})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.count(), 2)

    def test_get_categories(self):
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_category(self):
        response = self.client.put(f'/api/categories/{self.category.id}/', {'name': 'Work Updated', 'metadata': {'color': 'green'}})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Work Updated')

    def test_delete_category(self):
        response = self.client.delete(f'/api/categories/{self.category.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Category.objects.count(), 0)


class NoteCategoryAssignmentTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='Work', metadata={'color': 'blue'})
        self.note_data = {'body': 'Test note', 'category': self.category.id}

    def test_create_note_with_category(self):
        response = self.client.post('/api/notes/', self.note_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        note = Note.objects.get(id=response.data['id'])
        self.assertEqual(note.category, self.category)

    def test_filter_notes_by_category(self):
        note = Note.objects.create(body='Test note', category=self.category)
        response = self.client.get(f'/api/notes/?category={self.category.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], note.id)
