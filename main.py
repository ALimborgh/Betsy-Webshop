from datetime import datetime
from models import Product, User, Tag, ProductTag, Transaction

# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

# Add your code after this line


def search_products(search_term):
    return Product.select().where(
        (Product.name.contains(search_term)) | (Product.description.contains(search_term))
    )

def list_user_products(user_id):
    return [product.name for product in Product.select().where(Product.user_id == user_id)]


def list_products_per_tag(tag_id):
    return [product.name for product in Product.select().join(ProductTag).where(ProductTag.tag_id == tag_id)]


def add_product_to_catalog(user_id, product):
    product.user_id = user_id
    product.save()

def remove_product_from_user(product_id):
    product = Product.get(Product.id == product_id)
    product.delete_instance()

def update_stock(product_id, new_quantity):
    product = Product.get(Product.id == product_id)
    product.stock_quantity = new_quantity
    product.save()

def purchase_product(product_id, buyer_id, quantity):
    product = Product.get(Product.id == product_id)
    if product.stock_quantity < quantity:
        raise ValueError('Not enough stock')
    product.stock_quantity -= quantity
    product.save()
    transaction = Transaction(user_id=buyer_id, product_id=product_id, quantity=quantity, total_price=product.price_per_unit * quantity)
    transaction.save()
    return transaction.id

def populate_test_database():
    # Create users
    user1 = User.create(username='user1', password='password1', address='address1')
    user2 = User.create(username='user2', password='password2', address='address2')

    # Create products
    product1 = Product.create(name='product1', description='description1', price=10.0, quantity=5, user=user1)
    product2 = Product.create(name='product2', description='description2', price=20.0, quantity=10, user=user2)

    # Create tags
    tag1 = Tag.create(name='tag1')
    tag2 = Tag.create(name='tag2')

    # Create product tags
    ProductTag.create(product=product1, tag=tag1)
    ProductTag.create(product=product2, tag=tag2)

    # Create transactions
    Transaction.create(buyer=user1, product=product2, quantity=2, total_price=40.0, timestamp=datetime.now())
    Transaction.create(buyer=user2, product=product1, quantity=1, total_price=10.0, timestamp=datetime.now())