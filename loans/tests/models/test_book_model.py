from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
import datetime
from loans.models import Book

class BookTestCase(TestCase):
    def setUp(self):
        authors = "Doe, J."
        title = "A title"
        publication_date = datetime.datetime(2024, 9, 1)
        isbn = "1234567890123"
        self.book = Book(authors = authors, title=title, publication_date=publication_date, isbn=isbn)

    def test_valid_book_is_valid(self):
        try:
            self.book.full_clean()
        except ValidationError:
            self.fail("Default test should be deemed valid")

    def test_book_with_blank_author_is_invalid(self):
        self.book.authors = ""
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_book_with_overlong_author_is_invalid(self):
        self.book.authors = "x" * 256
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_book_with_blank_title_is_invalid(self):
        self.book.title = ""
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_book_with_overlong_title_is_invalid(self):
        self.book.title = "x" * 256
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_book_with_blank_publicaation_date_is_invalid(self):
        self.book.publication_date = None
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_book_with_non_publication_date_is_invalid(self):
        self.book.publication_date = 'this is not a date'
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_book_with_blank_isbn_is_invalid(self):
        self.book.isbn = ""
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_book_with_overlong_isbn_is_invalid(self):
        self.book.isbn = "12345678901234"
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_book_with_13_isbn_is_valid(self):
        self.book.isbn = "1234567890123"
        try:
            self.book.full_clean()
        except ValidationError:
            self.fail("isbn consisting of numbers and of size 13 should be deemed valid")

    def test_book_with_12_isbn_is_invalid(self):
        self.book.isbn = "123456789012"
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_book_with_11_isbn_is_invalid(self):
        self.book.isbn = "12345678901"
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_book_with_10_isbn_is_valid(self):
        self.book.isbn = "1234567890"
        try:
            self.book.full_clean()
        except ValidationError:
            self.fail("isbn consisting of numbers and of size 10 should be deemed valid")

    def test_book_with_short_isbn_is_invalid(self):
        self.book.isbn = "123456789"
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_book_with_string_13_isbn_is_invalid(self):
        self.book.isbn = "1234567b90123"
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_book_with_string_10_isbn_is_invalid(self):
        self.book.isbn = "1234567b90"
        with self.assertRaises(ValidationError):
            self.book.full_clean()

    def test_book_isbn_must_be_unique(self):
        self.book.save()
        authors = "Pickles, P."
        title = "Another title"
        publication_date = datetime.datetime(2023, 9, 2)
        isbn = "1234567890123"
        with self.assertRaises(IntegrityError):
            Book.objects.create(authors = authors, title=title, publication_date=publication_date, isbn=isbn)

    def test_str_method(self):
        actual_string = str(self.book)
        expected_string ="Doe, J.    (2024)  \"A title\"    ISBN 1234567890123."
        self.assertEqual(actual_string, expected_string)

    def test_book_with_short_author_is_invalid(self):
        self.book.authors = "abc"
        with self.assertRaises(ValidationError):
            self.book.full_clean()