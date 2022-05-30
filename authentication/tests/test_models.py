import email
from rest_framework.test import APITestCase
from authentication.models import User

class TestModel(APITestCase):
    
    def test_creates_user(self):
        user = User.objects.create_user('Aman', 'aman@gmail.com', 'TestUser123')
        self.assertIsInstance(user, User)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.email,'aman@gmail.com')
    
    def test_creates_super_user(self):
        user = User.objects.create_superuser('admin', 'admin@gmail.com', 'TestUser123')
        self.assertIsInstance(user, User)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.email,'admin@gmail.com')

    def test_raises_errors_when_no_username_is_supplied(self):
        self.assertRaises(ValueError, User.objects.create_user, username="", email='aman@gmail.com', password='TestUser123')
    
    def test_raises_errors_with_message_when_no_username_is_supplied(self):
        with self.assertRaisesMessage(ValueError, 'The given username must be set'):
            User.objects.create_user(username='', email='aman@gmail.com', password='TestUser123')
    
    def test_raises_errors_when_no_email_is_supplied(self):
        self.assertRaises(ValueError, User.objects.create_user, username="test", email='', password='TestUser123')
    
    def test_raises_errors_with_message_when_no_email_is_supplied(self):
        with self.assertRaisesMessage(ValueError, 'The given email must be set'):
            User.objects.create_user(username='test', email='', password='TestUser123')

    def test_cant_create_super_user_with_is_staff_status(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_staff=True.'):
            User.objects.create_superuser(username='username', email='aman@gmail.com', password='TestUser123', is_staff=False)

    def test_cant_create_super_user_with_is_superuser_status(self):
        with self.assertRaisesMessage(ValueError, 'Superuser must have is_superuser=True.'):
            User.objects.create_superuser(username='username', email='aman@gmail.com', password='TestUser123', is_superuser=False)
           
    