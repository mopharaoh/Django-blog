from django.test import TestCase

# Create your tests here.
class Urltest(TestCase):
    def test_checkurl(self):
        response=self.client.get('/account/profile/')
        self.assertEqual(response.status_code,302)