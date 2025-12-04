from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Post,Category,Comment
from model_bakery import baker
from django.urls import reverse

class HomeViewTest(TestCase):
    def setUp(self):
        self.user = baker.make(User)
        self.category = baker.make(Category)
        self.post = baker.make(Post, author=self.user, category=self.category, status='published',_quantity=5)


    def test_home(self):
        url = reverse('blog:homepage')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
