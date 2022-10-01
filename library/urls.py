from django.urls import path
from .views import BooksView, BookView, BookIssueView

urlpatterns = [
    path('books/', BooksView.as_view(), name = 'books'),
    path('books/<str:id>/', BookView.as_view(), name = 'book'),
    path('books/<str:id>/issue/', BookIssueView.as_view(), name = 'issue'),
    
]