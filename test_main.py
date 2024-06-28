import unittest
from peewee import SqliteDatabase
from main import search_products, add_product_to_catalog, remove_product_from_user
from models import Product, User


class TestDatabaseOperations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use an in-memory SQLite database for testing, shared across tests
        cls.db = SqliteDatabase(':memory:')
        cls.db.bind([User, Product], bind_refs=False, bind_backrefs=False)
        cls.db.connect()
        cls.db.create_tables([User, Product])

        # Create a test user and product for use in all tests
        cls.user = User.create(name='Test User', address='123 Test Street', billing_info='Some Billing Info')
        cls.product = Product.create(name='Test Product', description='This is a test product', user=cls.user, price_per_unit=10.0, quantity_in_stock=5, tags=[])

    @classmethod
    def tearDownClass(cls):
        # Close the database connection after all tests have run
        cls.db.close()

    def test_search_products(self):
        # Test that search_products returns products that match the search term
        products = search_products('Test')
        self.assertTrue(any(product.name == 'Test Product' for product in products))

        # Test that search_products does not return products that do not match the search term
        products = search_products('Nonexistent')
        self.assertTrue(all(product.name != 'Test Product' for product in products))

    def test_add_product_to_catalog(self):
        # Test adding a new product to the catalog
        new_product = add_product_to_catalog('New Product', 'New Description', self.user, 20.0, 10, [])
        self.assertIsNotNone(new_product)
        # Verify the product was added
        self.assertTrue(Product.select().where(Product.name == 'New Product').exists())

    def test_remove_product_from_user(self):
        # Test removing a product from a user
        remove_product_from_user(self.product.id, self.user.id)
        self.assertFalse(Product.select().where(Product.id == self.product.id).exists())

if __name__ == '__main__':
    unittest.main()
    
    