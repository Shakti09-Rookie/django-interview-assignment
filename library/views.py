from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics, status
# from rest_framework.permissions import IsAuthenticated
from .serializers import BookSerializer
from .models import Book

# Create your views here.
class BooksView(APIView):

    def get(self, request):
        qs = Book.objects.all()
        serializer = BookSerializer(qs, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# using mixins
# class BookCreateView(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
#     serializer_class = BookSerializer
#     queryset = Book.objects.all()

#     def get(self, request):
#         return self.list(self, request)

#     def post(self, request):
#         return self.create(request)

class BookView(APIView):

    def get(self,request, id):
        book = Book.objects.get(id=id)
        bookSerial = BookSerializer(book)
        return Response(bookSerial.data)

    def put(self, request, id):
        data = request.data
        book = Book.objects.get(id=id)
        serializer = BookSerializer(book, data=data)
        if serializer.is_valid():
            serializer.save()
        updatedBook = Book.objects.get(id=id)
        updatedBookSerial = BookSerializer(updatedBook)
        return Response(updatedBookSerial.data)

    def delete(self, request, id):
        book = Book.objects.get(id=id)
        book.delete()
        return Response({
            'message' : "Book Removed"
        })
