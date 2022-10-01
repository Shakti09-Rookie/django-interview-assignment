from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import BookSerializer
from .models import Book, BookRecords
from users.models import User

# Create your views here.
class BooksView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Book.objects.all()
        serializer = BookSerializer(qs, many = True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role == "LIBRARIAN":
            serializer = BookSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Action Restricted'})

# using mixins
# class BookCreateView(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
#     serializer_class = BookSerializer
#     queryset = Book.objects.all()

#     def get(self, request):
#         return self.list(self, request)

#     def post(self, request):
#         return self.create(request)

class BookView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request, id):
        book = Book.objects.get(id=id)
        bookSerial = BookSerializer(book)
        return Response(bookSerial.data)

    def put(self, request, id):
        if request.user.role == "LIBRARIAN":
            data = request.data
            book = Book.objects.get(id=id)
            serializer = BookSerializer(book, data=data)
            if serializer.is_valid():
                serializer.save()
            updatedBook = Book.objects.get(id=id)
            updatedBookSerial = BookSerializer(updatedBook)
            return Response(updatedBookSerial.data)
        return Response({'message': 'Action Restricted'})

    def delete(self, request, id):
        if request.user.role == "LIBRARIAN":
            book = Book.objects.get(id=id)
            book.delete()
            return Response({
                'message' : "Book Removed"
            })
        return Response({'message': 'Action Restricted'})

class BookIssueView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if request.user.role == "MEMBER":
            book = Book.objects.get(id=id)
            return Response({"Book Status" : book.Status})
        return Response({'message': 'Action Restricted'})

    def post(self, request, id):
        if request.user.role == "MEMBER":
            book = Book.objects.get(id=id)
            if request.data['Status'] == "BORROW":
                if book.Status == "AVAILABLE":
                    book.Status = "BORROWED"
                    book.save()
                    BookRecords.objects.create(book=book, Status= request.data['Status'])
                    return Response({"messagee" : "Book Borrowed"})
                else:
                    return Response({"message" : "Not Available to Borrow"})
            elif request.data['Status'] == "RETURN":
                if book.Status == "BORROWED":
                    book.Status = "AVAILABLE"
                    book.save()
                    BookRecords.objects.create(book=book, Status= request.data['Status'])
                    return Response({"message" : "Book Returned"})
                else:
                    return Response({"message" : "Bad Request, Book, is already in the system"})
            else:
                return Response({"message" : "Bad Request"})
        return Response({'message': 'Action Restricted'})