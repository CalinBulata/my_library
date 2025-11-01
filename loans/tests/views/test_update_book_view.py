from django.test import TestCase
from django.urls import reverse
from django.db import transaction
from django.contrib import messages

from loans.forms import BookForm
from loans.models import Book

import datetime

class UpdateBookTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            authors = "Doe, J.",
            title = "A Title",
            publication_date = datetime.date(2024, 9, 1),
            isbn = "1234567890123"
        )
        self.url = reverse('update_book', kwargs={"book_id": self.book.pk})
        self.form_input = {
            'authors': "Calin, B.",
            'title': "A New Title",
            'publication_date': '2025-01-01',
            'isbn': "1111111111"
        }

    def test_update_book_url(self):
        self.assertEqual(self.url, f'/update_book/{self.book.pk}/')

    def test_get_update_book(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_book.html')
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(isinstance(form, BookForm))
        self.assertFalse(form.is_bound)
        self.assertEqual(form.instance, self.book)
        self.assertEqual(form.initial['title'], 'A Title')
        self.assertEqual(form.initial['authors'], 'Doe, J.')

    def test_post_with_valid_data(self):
        before_count = Book.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Book.objects.count()
        self.assertEqual(after_count, before_count)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "A New Title")
        self.assertEqual(self.book.authors, "Calin, B.")
        self.assertEqual(self.book.isbn, "1111111111")
        self.assertEqual(self.book.publication_date, datetime.date(2025, 1, 1))
        expected_redirect_url = reverse('list_books')
        self.assertRedirects(response, expected_redirect_url, status_code = 302, target_status_code = 200)
        message_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(message_list), 1)
        self.assertEqual(message_list[0].level, messages.INFO)

    def test_post_with_invalid_data(self):
        self.form_input['authors'] = ''
        original_title = self.book.title
        before_count = Book.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Book.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_book.html')
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(isinstance(form, BookForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, original_title)
        self.assertNotEqual(self.book.authors, '')

    def test_post_with_non_unique_isbn(self):
        Book.objects.create(
            authors = "Pickles, P.",
            title = "My book",
            publication_date = datetime.datetime(2023, 8, 2),
            isbn = "9999999999"
        )
        self.form_input['isbn'] = "9999999999"
        original_isbn = self.book.isbn
        with transaction.atomic():
            response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_book.html')
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(isinstance(form, BookForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        self.assertIn('isbn', form.errors)
        self.book.refresh_from_db()
        self.assertEqual(self.book.isbn, original_isbn)
        self.assertNotEqual(self.book.isbn, "9999999999")

    def test_get_request_with_invalid_book_id(self):
        non_existent_id = 999
        bad_url = reverse('update_book', kwargs={'book_id': non_existent_id})
        response = self.client.get(bad_url)
        self.assertEqual(response.status_code, 404)

    def test_post_request_with_invalid_book_id(self):
        non_existent_id = 999
        bad_url = reverse('update_book', kwargs={'book_id': non_existent_id})
        before_count = Book.objects.count()
        response = self.client.post(bad_url, self.form_input)
        after_count = Book.objects.count()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(after_count, before_count)