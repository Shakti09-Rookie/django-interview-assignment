from django.db import models
from users.models import User

# Create your models here.

class Book(models.Model):
    choices = [
        ("AVAILABLE", "AVAILABLE"),
        ("BORROWED", "BORROWED"),
    ]
    Name = models.CharField(max_length=120)
    Author = models.CharField(max_length=100)
    Status = models.CharField(max_length=10, default = "AVAILABLE" ,choices=choices)

    class Meta:
        db_table = "BOOKS"

    def _str__(self):
        return self.Name

class BookRecords(models.Model):
    choices = [
        ("BORROW", "BORROW"),
        ("RETURN", "RETURN")
    ]
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    Status = models.CharField(max_length=50, choices=choices, null=True)
    created = models.DateField(auto_now=False, auto_now_add=True)

    class Meta:
        db_table = "BookRecords"