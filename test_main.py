import email
import unittest
from peewee import SqliteDatabase
from main import search_products, add_product_to_catalog, remove_product_from_user, update_stock, purchase_product, list_user_products, list_products_per_tag
from models import Product, User, Tag, ProductTag, Transaction


class TestDatabaseOperations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = SqliteDatabase(':memory:')
        cls.db.bind([User, Product], bind_refs=False, bind_backrefs=False)
        cls.db.connect()
        cls.db.create_tables([User, Product, Tag, ProductTag, Transaction])

        # Create a test user and product for use in all tests
        cls.user = User.create(name='Test User', email='test@email.com', address='123 Test Street', billing_info='Some Billing Info')
        cls.product = Product.create(name='Test Product', description='This is a test product', user=cls.user, price_per_unit=10.0, quantity_in_stock=5, tags=[])
        cls.tag = Tag.create(name='Test Tag')
        cls.product_tag = ProductTag.create(product=cls.product, tag=cls.tag)
        cls.transaction = Transaction.create(user=cls.user, product=cls.product, quantity=1, total_price=10.0)
        
    def setUp(self):
        # Start a new transaction before each test method
        self.db.begin()
        
    def tearDown(self):
        # Rollback the transaction after each test method
        self.db.rollback()
         
    def tearDownClass(cls):
        # Close the database connection after all tests have run
        cls.db.close()

    @classmethod
    def test_search_products(self):
        # Add additional products to test the search functionality
        Product.create(name='Unique Product', description='Unique description', user=self.user, price_per_unit=20.0, quantity_in_stock=10)
        Product.create(name='Another Product', description='Another description', user=self.user, price_per_unit=15.0, quantity_in_stock=8)
        
        # Use a search term that matches the 'Unique Product'
        search_term = 'Unique'
        matching_products = search_products(search_term)
        
        # Assert that the search returns exactly one product and it's the 'Unique Product'
        self.assertEqual(len(matching_products), 1)
        self.assertEqual(matching_products[0].name, 'Unique Product')
        self.assertEqual(matching_products[0].description, 'Unique description')

    def test_add_product_to_catalog(self):
        # Test adding a new product to the catalog
        new_product = add_product_to_catalog('New Product', 'New Description', self.user, 20.0, 10, [])
        self.assertIsNotNone(new_product)
        # Verify the product was added with correct details
        added_product = Product.get(Product.name == 'New Product')
        self.assertEqual(added_product.description, 'New Description')
        self.assertEqual(added_product.user, self.user)
        self.assertEqual(added_product.price_per_unit, 20.0)
        self.assertEqual(added_product.quantity_in_stock, 10)

    def test_remove_product_from_user(self):
        # Add a product to remove
        product_to_remove = Product.create(name='Removable Product', description='Removable description', user=self.user, price_per_unit=5.0, quantity_in_stock=5)
        # Test removing the product from a user
        remove_product_from_user(product_to_remove.id, self.user.id)
        self.assertFalse(Product.select().where(Product.id == product_to_remove.id).exists())

    def test_update_stock(self):
        # Test updating the stock of a product
        initial_stock = self.product.quantity_in_stock
        update_stock(self.product.id, initial_stock + 10)
        updated_product = Product.get(Product.id == self.product.id)
        self.assertEqual(updated_product.quantity_in_stock, initial_stock + 10)
        
    def test_purchase_product(self):
        # Test purchasing a product
        initial_stock = 5
        purchase_quantity = 1
        purchase_product(self.product.id, self.user.id, purchase_quantity)
        product_after_purchase = Product.get(Product.id == self.product.id)
        # Check if stock decreased by 1
        self.assertEqual(product_after_purchase.quantity_in_stock, initial_stock - purchase_quantity)
        # Verify a transaction record exists
        self.assertTrue(Transaction.select().where(Transaction.product == self.product).exists())

    def test_list_user_products(self):
        # Test listing products owned by a specific user
        products = list_user_products(self.user.id)
        # Check if 'Test Product' is in the list of user's products
        self.assertIn('Test Product', [product.name for product in products])

    def test_list_products_per_tag(self):
        # Test listing products associated with a specific tag
        products = list_products_per_tag(self.tag.id)
        # Check if 'Test Product' is in the list of products tagged with 'self.tag'
        self.assertIn('Test Product', [product.name for product in products])

if __name__ == '__main__':
    unittest.main()
    
    