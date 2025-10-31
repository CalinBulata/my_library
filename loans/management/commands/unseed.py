from loans.models import Book
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Remove all Book entries from the database"
    
    def handle(self, *args, **options):
        Book.objects.all().delete()

