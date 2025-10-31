from faker import Faker
from loans.models import Book
fake =Faker()

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Seed the database with sample Book data"
    
    def handle(self, *args, **options):
        for _ in range(100):
            book_authors = f"{fake.last_name()}, {fake.first_name()}"
            book_title = fake.sentence()
            book_publication_date = fake.date()
            book_isbn = fake.unique.isbn13().replace('-', '')
            Book.objects.create(
                authors=book_authors,
                title=book_title,
                publication_date=book_publication_date,
                isbn=book_isbn
            )

