from django.test import TestCase
from shop.models import Product, Purchase
from datetime import datetime

class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="hat", price="450", buying="True")
        Product.objects.create(name="shirt", price="1500", buying="False")

    def test_correctness_types(self):                   
        self.assertIsInstance(Product.objects.get(name="hat").name, str)
        self.assertIsInstance(Product.objects.get(name="hat").price, int)
        self.assertIsInstance(Product.objects.get(name="hat").buying, bool)
        self.assertIsInstance(Product.objects.get(name="shirt").name, str)
        self.assertIsInstance(Product.objects.get(name="shirt").price, int)
        self.assertIsInstance(Product.objects.get(name="shirt").buying, bool)

    def test_correctness_data(self):
        self.assertTrue(Product.objects.get(name="hat").price == 450)
        self.assertTrue(Product.objects.get(name="hat").buying == True)
        self.assertTrue(Product.objects.get(name="shirt").price == 1500)
        self.assertTrue(Product.objects.get(name="shirt").buying == False)


class PurchaseTestCase(TestCase):
    def setUp(self):
        self.product_jeans = Product.objects.create(name="jeans", price="2500")
        self.datetime = datetime.now()
        Purchase.objects.create(product=self.product_jeans,
                                person="Mikhail",
                                address="Yes St.",
                                discount=0.1)

        self.product_skirt = Product.objects.create(name="skirt", price="3999")
        self.datetime = datetime.now()
        Purchase.objects.create(product=self.product_skirt,
                                person="Anna",
                                address="Gaming St.",
                                discount=0)

    def test_correctness_types(self):
        self.assertIsInstance(Purchase.objects.get(product=self.product_jeans).person, str)
        self.assertIsInstance(Purchase.objects.get(product=self.product_jeans).address, str)
        self.assertIsInstance(Purchase.objects.get(product=self.product_jeans).date, datetime)
        self.assertIsInstance(Purchase.objects.get(product=self.product_jeans).discount, float)

        self.assertIsInstance(Purchase.objects.get(product=self.product_skirt).person, str)
        self.assertIsInstance(Purchase.objects.get(product=self.product_skirt).address, str)
        self.assertIsInstance(Purchase.objects.get(product=self.product_skirt).date, datetime)
        self.assertIsInstance(Purchase.objects.get(product=self.product_skirt).discount, float)

    def test_correctness_data(self):
        self.assertTrue(Purchase.objects.get(product=self.product_jeans).person == "Mikhail")
        self.assertTrue(Purchase.objects.get(product=self.product_jeans).address == "Yes St.")
        self.assertTrue(Purchase.objects.get(product=self.product_jeans).date.replace(microsecond=0) == \
            self.datetime.replace(microsecond=0))
        self.assertTrue(Purchase.objects.get(product=self.product_jeans).discount == 0.1)

        self.assertTrue(Purchase.objects.get(product=self.product_skirt).person == "Anna")
        self.assertTrue(Purchase.objects.get(product=self.product_skirt).address == "Gaming St.")
        self.assertTrue(Purchase.objects.get(product=self.product_skirt).date.replace(microsecond=0) == \
                        self.datetime.replace(microsecond=0))
        self.assertTrue(Purchase.objects.get(product=self.product_skirt).discount == 0)