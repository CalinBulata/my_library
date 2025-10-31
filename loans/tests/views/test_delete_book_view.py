from django.test import TestCase
from django.urls import reverse
from django.db import transaction

from loans.forms import BookForm
from loans.models import Book

import datetime

class DeleteBookTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            authors = "Doe, J.",
            title = "A Title",
            publication_date = datetime.datetime(2024, 9, 1),
            isbn = "1234567890123"
        )
        self.url = reverse('delete_book', kwargs={"book_id": self.book.pk})
        self.expected_url_path = f'/delete_book/{self.book.pk}/'

    def test_delete_book_url(self):
        self.assertEqual(self.url, self.expected_url_path)

    def test_get_request_with_invalid_book_id(self):
        non_existent_id = 999
        bad_url = reverse('delete_book', kwargs={'book_id': non_existent_id})
        response = self.client.get(bad_url)
        self.assertEqual(response.status_code, 404)

    def test_post_deletes_books_with_valid_data(self):
        book_to_delete_pk = self.book.pk
        before_count = Book.objects.count()
        response = self.client.post(self.url, follow=True)
        after_count = Book.objects.count()
        self.assertEqual(after_count, before_count-1)
        book_exists = Book.objects.filter(pk=book_to_delete_pk).exists()
        self.assertFalse(book_exists)
        expected_redirect_url = reverse('list_books')
        self.assertRedirects(response, expected_redirect_url, status_code = 302, target_status_code = 200)

    def test_post_request_with_invalid_book_id(self):
        non_existent_id = 999
        bad_url = reverse('delete_book', kwargs={'book_id': non_existent_id})
        before_count = Book.objects.count()
        self.assertEqual(before_count, 1)
        response = self.client.post(bad_url)
        after_count = Book.objects.count()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(after_count, before_count)