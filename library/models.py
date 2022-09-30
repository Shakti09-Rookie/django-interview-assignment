from django.db import models

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