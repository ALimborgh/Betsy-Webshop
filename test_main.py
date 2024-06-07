import unittest
from peewee import SqliteDatabase
from main import search_products, add_product_to_catalog, remove_product_from_user
from models import Product, User

class TestMain(unittest.TestCase):
    def setUp(self):
        # Use an in-memory SQLite database for testing
        self.db = SqliteDatabase(':memory:')
        self.db.bind([User, Product], bind_refs=False, bind_backrefs=False)
        self.db.connect()
        self.db.create_tables([User, Product])

        # Create a test user and product
        self.user = User.create(name='Test User', address='123 Test Street', billing_info='Some Billing Info')
        self.product = Product.create(name='Test Product', description='This is a test product', user=self.user, price_per_unit=10.0, quantity_in_stock=5, tags=[])

    def tearDown(self):
        # Close the database connection after each test
        self.db.close()

    def test_search_products(self):
        # Test that search_products returns products that match the search term
        products = search_products('Test')
        self.assertIn(self.product, products)

        # Test that search_products does not return products that do not match the search term
        products = search_products('Nonexistent')
        self.assertNotIn(self.product, products)

class TestRemoveProductFromUser(unittest.TestCase):
    def setUp(self):
        self.product = Product.create(name='Test Product', description='This is a test product', price_per_unit=10.0)

    def test_remove_product_from_user(self):
        remove_product_from_user(self.product.id)
        with self.assertRaises(Product.DoesNotExist):
            Product.get(Product.id == self.product.id)

    def tearDown(self):
        if self.product.id is not None:
            self.product.delete_instance()

if __name__ == '__main__':
    unittest.main()
    
    