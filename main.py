from datetime import datetime
import re
from models import Product, User, Tag, ProductTag, Transaction
import bcrypt

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


def add_product_to_catalog(user_id, product, price_per_unit, quantity_in_stock, description, name):
    product = Product(user_id=user_id, price_per_unit=price_per_unit, quantity_in_stock=quantity_in_stock, description=description, name=name)
    product.save()
    return product.id
    
def remove_product_from_user(product_id, user_id):
    product = Product.get(Product.id == product_id)
    if product.user_id != user_id:
        raise ValueError('User does not own this product')
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
    timestamp = datetime.now()  # Use the same timestamp for all transactions in this batch
    
    # Hash passwords before storing them
    hashed_password1 = bcrypt.hashpw('password1'.encode('utf-8'), bcrypt.gensalt())
    hashed_password2 = bcrypt.hashpw('password2'.encode('utf-8'), bcrypt.gensalt())
    
    # Create users with hashed passwords and email
    user1 = User.create(username='user1', password=hashed_password1, email='email1@example.com')
    user2 = User.create(username='user2', password=hashed_password2, email='email2@example.com')

    # Create products with seller_id instead of user
    product1 = Product.create(name='product1', description='description1', price=10.0, quantity=5, seller_id=user1.id)
    product2 = Product.create(name='product2', description='description2', price=20.0, quantity=10, seller_id=user2.id)

    # Create tags with tag_name instead of name
    tag1 = Tag.create(tag_name='tag1')
    tag2 = Tag.create(tag_name='tag2')

    # Create product tags with product_id and tag_id
    ProductTag.create(product_id=product1.id, tag_id=tag1.id)
    ProductTag.create(product_id=product2.id, tag_id=tag2.id)

    # Create transactions with buyer_id, product_id, and transaction_time
    Transaction.create(buyer_id=user1.id, product_id=product2.id, quantity=2, total_price=40.0, transaction_time=timestamp)
    Transaction.create(buyer_id=user2.id, product_id=product1.id, quantity=1, total_price=10.0, transaction_time=timestamp)