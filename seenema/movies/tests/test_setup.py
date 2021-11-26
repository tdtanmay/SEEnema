from rest_framework.test import APITestCase
from django.urls import reverse

class TestSetup(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')

        self.register_data = {
            'email': 'example@gmail.com',
            'username': 'example123',
            'password': 'Example@123#pass'
        }

        self.login_data = {
            'username': 'example123',
            'password': 'Example@1456'
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()