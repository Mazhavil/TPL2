from django.test import TestCase, Client

class PurchaseCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_webpage_accessibility(self):
        response = self.client.get('/buy/')
        self.assertEqual(response.status_code, 200)

    def test_webpage_inaccessible(self):
        response = self.client.get('/buy/1')
        self.assertEqual(response.status_code, 404)
