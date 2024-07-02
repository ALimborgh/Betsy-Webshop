from peewee import *
from models import Product, ProductTag, Transaction, User, Tag
import logging
from peewee import SqliteDatabase

# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

# Add your code after this line
def search_products(search_term):
    # Search for products by name or description
    return Product.select().where(
        (Product.name.contains(search_term)) | (Product.description.contains(search_term))
    )

def list_user_products(user_id):
    # List products owned by a specific user
    return [product.name for product in Product.select().where(Product.user == user_id)]

def list_products_per_tag(tag_id):
    # List products associated with a specific tag
    return [product.name for product in Product.select().join(ProductTag).where(ProductTag.tag == tag_id)]

def add_product_to_catalog(user_id, name, description, price_per_unit, quantity_in_stock):
    try:
        # Check if the product already exists for the user
        existing_product = Product.select().where(
            (Product.user == user_id) & (Product.name == name)
        ).first()

        if existing_product:
            logging.info(f"Product already exists for user_id {user_id}: {name}")
            return "Product already exists for this user."

        new_product = Product.create(
            user=user_id, 
            name=name, 
            description=description, 
            price_per_unit=price_per_unit, 
            quantity_in_stock=quantity_in_stock,
            is_active=True 
        )
        logging.info(f"Product added successfully: {new_product.id}")
        return new_product.id
    except Exception as e:
        logging.error(f"Error adding product: {e}")
        return "Error adding product"

def remove_product_from_user(product_id, user_id):
    # Remove a product from a user's catalog
    product = Product.get(Product.id == product_id)
    if product.user.id != user_id: 
        raise ValueError('User does not own this product')
    product.delete_instance()

def update_stock(product_id, new_quantity):
    # Update the stock quantity of a product
    product = Product.get(Product.id == product_id)
    product.quantity_in_stock = new_quantity 
    product.save()

def purchase_product(product_id, buyer_id, quantity):
    # Retrieve the product by ID
    product = Product.get_or_none(Product.id == product_id)
    # Check if product exists and is active
    if not product or not product.is_active:
        raise ValueError('Product not available for purchase')
    
    # Check if there's enough stock
    if product.quantity_in_stock < quantity:
        raise ValueError('Not enough stock')
    
    # Deduct the quantity from stock
    product.quantity_in_stock -= quantity
    product.save()
    
    # Calculate the total price
    total_price = product.price_per_unit * quantity
    
    # Create a transaction record
    transaction = Transaction.create(
        user_id=buyer_id,
        product_id=product_id,
        quantity=quantity,
        total_price=total_price
    )
    
    return transaction.id

def populate_database():
    db=SqliteDatabase('my_database.db')
    # Connect to the database
    db.connect()
    
    # Delete the tables
    db.drop_tables([User, Product, Tag, ProductTag, Transaction])

    # Create the tables
    db.create_tables([User, Product, Tag, ProductTag, Transaction])

    # Create some users with address and billing_info
    user1 = User.create(name='John Doe', email='john@example.com', address='123 Main St', billing_info='Visa 1234')
    user2 = User.create(name='Jane Doe', email='jane@example.com', address='456 Elm St', billing_info='MasterCard 5678')

    # Add products for user1
    Product.create(name='Product 1', description='Description 1', price_per_unit=10.0, quantity_in_stock=100, user=user1)
    Product.create(name='Product 2', description='Description 2', price_per_unit=20.0, quantity_in_stock=200, user=user1)

    # Add products for user2
    Product.create(name='Product 3', description='Description 3', price_per_unit=30.0, quantity_in_stock=300, user=user2)

    with db.atomic():
        # Create user and products within a transaction
        user3 = User.create(name='Alice Wonderland', email='alice@example.com', address='789 Pine St', billing_info='Amex 9012')
        Product.create(name='Product 4', description='Description 4', price_per_unit=40.0, quantity_in_stock=400, user=user3)

    # Add tags
    tag1 = Tag.create(name='Tag 1', description='Tag 1 description')
    tag2 = Tag.create(name='Tag 2', description='Tag 2 description')

    # Add tags to products
    ProductTag.create(product=Product.get(Product.name == 'Product 1'), tag=tag1)
    ProductTag.create(product=Product.get(Product.name == 'Product 1'), tag=tag2)
    ProductTag.create(product=Product.get(Product.name == 'Product 2'), tag=tag2)

    # Add transactions
    Transaction.create(user=user1, product=Product.get(Product.name == 'Product 1'), quantity=5, total_price=50.0)
    Transaction.create(user=user1, product=Product.get(Product.name == 'Product 2'), quantity=10, total_price=200.0)
    Transaction.create(user=user2, product=Product.get(Product.name == 'Product 3'), quantity=15, total_price=450.0)

    # Close the database connection
    db.close()
        
# Populate the database with sample data
populate_database()