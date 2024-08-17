import datetime
import jwt
from django.contrib.auth import login, logout
from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from restbas.models import User
from restbas.Auth.serializers import UserSerializer


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response(
                {'error': 'Email and password are required'},
                status=400
            )
        user = User.objects.filter(email=email).first()

        if user:
            print("User found:", user)
        else:
            print("User not found")
            return Response({'error': 'Invalid credentials'}, status=401)

        if not user.check_password(password):
            print("Invalid password")
            return Response({'error': 'Invalid credentials'}, status=401)

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(
            payload, 'secret',
            algorithm='HS256'
        ).decode('utf-8')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token,
            'message': 'Logged in successfully',

        }

        return response

    def get(self, request):
        return render(request, 'login.html')


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            payload = {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60), # noqa
                'iat': datetime.datetime.utcnow()
            }
            token = jwt.encode(
                payload, 'secret',
                algorithm='HS256'
            ).decode('utf-8')
            response = Response({
                'jwt': token,
                'message': 'Registered and logged in successfully',
                'authenticated': True
            }, status=201)  # Set the status code to 201
            response.set_cookie(key='jwt', value=token, httponly=True)

            return response
        else:
            return Response(serializer.errors, status=400)

    def get(self, request):
        return render(request, 'register.html')


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("no token")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("token is expired")

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'logged out'
        }
        return response


def homepage(request):
    return render(request, 'homepage.html')


class UserView(APIView): # noqa
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("no token")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("token is expired")

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView): # noqa
    def post(self, request):
        logout(request)
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'logged out'
        }
        return response


def homepage(request): # noqa
    return render(request, 'homepage.html')
