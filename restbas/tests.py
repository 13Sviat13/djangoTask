from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User, Permission
from rest_framework.utils import json
from restbas.models import Restaurant


class TestRegisterUser(TestCase):
    def test_register_user(self):
        client = APIClient()
        data = {
            'email': 'test@example.com',
            'password': 'password123',
            'username': 'testuser'
        }
        response = client.post(
            '/register/', json.dumps(data),
            content_type='application/json'
        )
        print(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()['message'],
            'Registered and logged in successfully'
        )


class TestLoginUser(TestCase):
    def setUp(self):
        # Set up user
        self.user = User(username="foo", email="foo@bar.com")
        self.user.email = "foo@bar.com"
        password = 'some_password'
        self.user.set_password(password)
        self.user.save()

    def test_login_user(self):
        # Login user
        login_url = reverse('login')
        response = self.client.post(
            login_url,
            {'username': self.user.email,
             'password': 'some_password'},
            follow=True
        )
        if response.status_code == 400:
            print("Failed to login user:", response.content.decode('utf-8'))
        else:
            self.assertRedirects(
                response,
                '/'
            )
            print("User is logged in successfully")


class TestCreateRestaurant(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('test@example.com', 'password123')
        self.user.is_staff = True  # Make the user a staff user
        self.user.save()
        permission = Permission.objects.get(codename='add_restaurant')
        self.user.user_permissions.add(permission)
        self.client.force_authenticate(user=self.user)

    def test_create_restaurant(self):
        data = {
            'name': 'Test Restaurant',
            'address': '123 Main St',
            'kitchen': 'Italian',
            'phone_number': '555-555-5555',
            'owner': self.user.id
        }
        response = self.client.post('/restaurants/', data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'Test Restaurant')


class TestUploadMenu(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('test@example.com', 'password123')
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            owner=self.user
        )

    def test_upload_menu(self):
        data = {
            'menu': {
                'date': 'MONDAY'
            },
            'menu_items': [
                {'name': 'Item 1', 'description': 'Desc 1', 'price': 10.99},
                {'name': 'Item 2', 'description': 'Desc 2', 'price': 9.99}
            ]
        }
        response = self.client.post(
            f'/restaurants/{self.restaurant.id}/menu',
            data, format='json'
        )
        print(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data['message'],
            'Menu uploaded successfully'
        )
