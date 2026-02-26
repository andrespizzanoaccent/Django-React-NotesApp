from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Category, Note


class CategoryTests(APITestCase):

    def setUp(self):
        self.category_data = {'name': 'Work', 'metadata': {}}
        self.category = Category.objects.create(**self.category_data)

    def test_create_category(self):
        url = reverse('categories')
        data = {'name': 'Personal', 'metadata': {}}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    def test_get_categories(self):
        url = reverse('categories')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_category(self):
        url = reverse('category', args=[self.category.id])
        data = {'name': 'Updated Work', 'metadata': {}}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Updated Work')

    def test_delete_category(self):
        url = reverse('category', args=[self.category.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)


class NoteTests(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Work', metadata={})
        self.note_data = {'body': 'Test Note', 'category': self.category.id}
        self.note = Note.objects.create(**self.note_data)

    def test_create_note_with_category(self):
        url = reverse('notes')
        data = {'body': 'Another Test Note', 'category': self.category.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 2)

    def test_update_note_category(self):
        new_category = Category.objects.create(name='Personal', metadata={})
        url = reverse('note', args=[self.note.id])
        data = {'body': 'Updated Note', 'category': new_category.id}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.note.refresh_from_db()
        self.assertEqual(self.note.category.id, new_category.id)

    def test_delete_note(self):
        url = reverse('note', args=[self.note.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Note.objects.count(), 0)
