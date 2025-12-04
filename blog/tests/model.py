from django.test import TestCase
from ..models import Comment,Post,User,Category,Vote
from model_bakery import baker
# import mptt
# mptt.models._use_is_testing = False

class ModelTest(TestCase):
    def setUp(self):
        self.user = baker.make(User)
        self.category = baker.make(Category)
        self.post = baker.make(Post, author=self.user, category=self.category)
        
        # self.vote = baker.make(Vote, post=self.post, user=self.user, value=1)
    def test_get_absolute_url(self):
        url = self.post.get_absolute_url()
        self.assertIn(self.post.slug, url)
    def test_str_method_post(self):
        self.assertEqual(str(self.post), self.post.title)