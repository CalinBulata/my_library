from django.db import models
from django.core.validators import MinLengthValidator
from django.core.validators import RegexValidator

class Book (models.Model):
    authors = models.CharField(
        max_length = 255,
        validators = [MinLengthValidator(4)]
        )
    title = models.CharField(max_length = 255)
    publication_date = models.DateField()
    isbn = models.CharField(
        validators = [RegexValidator(r'^\d{10}(\d{3})?$')],
        unique = True
        )

    def __str__(self):
        return (f"{self.authors}    ({self.publication_date.year})  \"{self.title}\"    ISBN {self.isbn}.")
    
    def __repr__(self):
        return (f"<Book: {self.__str__()}>")
    
class Member(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.EmailField()

    def __str__(self):
        return (f"Member {self.id}: {self.last_name}, {self.first_name} <{self.email}>")
    
class Loan(models.Model):
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    start_at = models.DateField()
    end_at = models.DateField()