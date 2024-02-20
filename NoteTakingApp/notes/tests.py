from notes.models import Note
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.authtoken.models import Token

# Create your tests here.
class NoteTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.note = Note.objects.create(title='Test Note', content='This is a test note.', owner=self.user)

    def test_signup(self):
        response = self.client.post(reverse('signup'), {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'newpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.json())

    def test_create_note(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('create_note'), {'title': 'New Note', 'content': 'This is a new note.'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Note.objects.filter(title='New Note').exists())

    def test_get_note(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('get_note', args=[self.note.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'Test Note')

    def test_share_note(self):
        self.client.force_login(self.user)
        new_user = User.objects.create_user(username='newuser', password='newpassword') 
        response = self.client.post(reverse('share_note'), {'note_id': self.note.id, 'usernames': [new_user.username]})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(new_user in self.note.shared_with.all())

    def test_update_note(self):
        self.client.force_login(self.user)
        response = self.client.put(reverse('update_note', args=[self.note.id]), {'content': 'This is an updated note.'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.note.refresh_from_db()
        self.assertIn('This is an updated note.', self.note.content)

    def test_get_note_history(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('get_note_history', args=[self.note.id]))
        self.assertEqual(response.status_code, 200)
