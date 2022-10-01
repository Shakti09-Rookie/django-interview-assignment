from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializer import UserSerializer, LoginSerializer, MemberSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from .models import User
# Create your views here.

class RegisterAPI(APIView):
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                user=User.objects.get(username=serializer.data['username'])
                refresh = RefreshToken.for_user(user)
                return Response({
                    'status' : 200,
                    'data' : serializer.data,
                    'refresh' : str(refresh),
                    'access' : str(refresh.access_token),
                    'message' : "Registration Successfull",
                })

            return Response({
                'status' : 400,
                'message' : 'Something went wrong',
                'data' : serializer.errors
            })
        except Exception as e:
            print(e)
            return Response({'error' : e})

class LoginAPI(APIView):
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                username = serializer.data['username']
                password = serializer.data['password']

                user = authenticate(username=username, password=password)
                if user is None:
                    return Response({
                        'status' : 400,
                        'message' : 'Credentials Invalid',
                        'data' : {}
                    })


                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh' : str(refresh),
                    'access' : str(refresh.access_token),
                })

            return Response({
                'status' : 400,
                'message' : 'Something went wrong',
                'data' : serializer.errors
            })                

        except Exception as e:
            print(e)

class MemberViewAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == "LIBRARIAN":
            members = User.objects.filter(role='MEMBER')
            serializer = MemberSerializer(members, many=True)
            return Response(serializer.data)
        return Response({'message': 'Action Restricted'})

    def post(self, request):
        if request.user.role == "LIBRARIAN":
            data = request.data
            try:
                user = User.objects.create(
                    username = data['username'],
                    password = make_password(data['password']),
                    role = "MEMBER"
                )
                user.save()
                return Response({
                        'status' : 200,
                        'message' : 'Member Added'
                        })
            except:
                return Response({
                    'message' : 'username already exists'
                })
        return Response({'message': 'Action Restricted'})

class MemberOpsAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request,id):
        if request.user.role == "LIBRARIAN" or request.user.id == id:
            members = User.objects.get(id=id)
            serializer = MemberSerializer(members)
            return Response(serializer.data)
        return Response({'message': 'Action Restricted'})

    def put(self, request,id):
        if request.user.role == "LIBRARIAN":
            data = request.data
            user = User.objects.get(id=id)
            if not user:
                return Response({
                    'message' : 'No record found'
                })
            user.password = make_password(data['password'])
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.save()
            return Response({'message' : "Member Updated"})
        return Response({'message': 'Action Restricted'})

    def delete(self, request, id):
        if request.user.role == "LIBRARIAN" or request.user.id == id:
            user = User.objects.get(id=id)
            user.delete()
            return Response({
                    'message' : "User Removed"
                })
        return Response({'message': 'Action Restricted'})