from django.test import TestCase
from .models import UserAccount
from django.db.utils import IntegrityError
from django.urls import reverse
from rest_framework.test import APITestCase
from users import views
from rest_framework import status

# UserAccountTestCase inherits from TestCase. The test_create_user method creates a user and checks that the user is created successfully. 
# The test_create_superuser method creates a superuser and checks that the superuser is created successfully. 
# The test_create_user_same_email method creates a user and then tries to create another user with the same email. This should raise an IntegrityError.

class UserAccountTestCase(TestCase):
    # Test that a user can be created
    def test_create_user(self):
        user = UserAccount.objects.create_user(first_name='Grace', last_name='Test', email='test@gmail.com', password="Test!12345")
        self.assertEqual(user.first_name, "Grace")
        self.assertEqual(user.last_name, "Test")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    # Test that a superuser can be created
    def  test_create_superuser(self):
        admin_user = UserAccount.objects.create_superuser(first_name='Grace', last_name='Test', email='admin@gmail.com', password="Admin!12345")
        self.assertEqual(admin_user.first_name, "Grace")
        self.assertEqual(admin_user.last_name, "Test")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    # Test that a user cannot be created with same email
    def test_create_user_same_email(self):
        user = UserAccount.objects.create_user(first_name='Grace', last_name='Test', email='test2@gmail.com', password='Test!54321')
        with self.assertRaises(IntegrityError):
            user = UserAccount.objects.create_user(first_name='Grace', last_name='Test', email='test2@gmail.com', password='Test!54321')

# UserAccountAPITestCase inherits from APITestCase. The test_current_user method checks that the current user can be retrieved successfully.

class AuthViewsTests(APITestCase):
    # setup a user to be used in the tests
    def setUp(self):
        self.first_name = 'Auth'
        self.last_name = 'test'
        self.email = 'auth@gmail.com'
        self.password = 'Test!12345'
        self.data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password
        }
        self.login_data = {
            'email': self.email,
            'password': self.password
        }
    
    def test_current_user(self):

        # URL using path name
        url = reverse('register')

        # First post to register a user
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)

        # Second post to get token
        token = self.client.post(reverse('token_obtain_pair'), self.login_data, format='json').data['access']

        # Next post/get's will require the token to connect
        self.client.credentials(HTTP_AUTHORIZATION='Bearer  {0}'.format(token))
        response = self.client.get(reverse('me'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
