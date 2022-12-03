from django.test import TestCase, Client
from shop.models import Product
from shop.views import calculate_general_price_and_discount

class PurchaseCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_webpage_accessibility(self):
        response = self.client.get('/buy/')
        self.assertEqual(response.status_code, 200)

    def test_webpage_inaccessible(self):
        response = self.client.get('/buy/1')
        self.assertEqual(response.status_code, 404)

class DiscountCreateTestCase(TestCase):
    def setUp(self):
       self.product_cap = Product.objects.create(name="cap", price=2500)
       self.product_tshirt = Product.objects.create(name="tshirt", price=4000)

    def test_calculating(self):
        expectedData1 = 5850, 10.0
        expectedData2 = 2500, 0.0

        receivedData1 = calculate_general_price_and_discount([self.product_cap, self.product_tshirt], None, None)
        receivedData2 = calculate_general_price_and_discount([self.product_cap], None, None)
        receivedData1 = receivedData1[1:]
        receivedData2 = receivedData2[1:]

        self.assertEqual(expectedData1, receivedData1)
        self.assertEqual(expectedData2, receivedData2)