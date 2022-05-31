from itertools import count
from urllib import response
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from todos.models import Todo


class TodosAPITestCase(APITestCase):
    def create_todo(self):
        sample_data = {'title': "1st Task", 'description': "DOing the project"}
        response = self.client.post(reverse('todos'), sample_data)
        return response

    def authenticate(self):
        self.client.post(reverse('todos'), {
                         'username': "userone", 'email': "userone@gmail.com", 'password': "TestUser123"})
        response = self.client.post(
            reverse('login'), {'email': "userone@gmail.com", 'password': "TestUser123"})

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {response.data['token']}")

class TodoListCreateTest(TodosAPITestCase):

    def test_for_not_to_create_todo_without_user(self):
        response = self.create_todo()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_create_todo_with_authenticate_user(self):
        previous_todo_count = Todo.objects.all().count()
        self.authenticate() #authenticating the user
        response = self.create_todo()

        self.assertEqual(Todo.objects.all().count(), previous_todo_count + 1) #counting the todos

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], '1st Task')
        self.assertEqual(response.data['description'], 'DOing the project')

    def test_retrieves_all_todos(self):
        self.authenticate()
        response = self.client.get(reverse('todos'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'], list)

        self.create_todo()

        res = self.client.get(reverse('todos'))
        self.assertIsInstance(res.data['count'], int)
        self.assertEqual(res.data['count'], 1)


class TestTodoDetailView(TodosAPITestCase):

    def test_retrieves_One_item(self):
        self.authenticate()
        response = self.create_todo()

        res = self.client.get(reverse('todos',kwargs={'id':response.data['id']}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        todo = Todo.objects.get(id=response.data['id'])

        self.assertEqual(todo.title, res.data['title'])


    def test_retrieves_One_item(self):
        self.authenticate()
        response= self.create_todo()

        res= self.client.patch(reverse('todos', kwargs={'id': response.data['id']}), {'title': "New One", 'is_complete': True})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        updated_todo = Todo.objects.get('id')

        self.assertEqual(updated_todo.is_complete, True)
        self.assertEqual(updated_todo.title, 'New One')
    
    def test_retrieves_One_item(self):
        self.authenticate()
        response = self.create_todo()

        prev_db_count = Todo.objects.all().count()

        self.assertGreater(prev_db_count, 0)
        self.assertEqual(prev_db_count, 1)

        res = self.client.delete(reverse('todos', kwargs={'id': response.data['id']}))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Todo.objects.all().count(), 0)