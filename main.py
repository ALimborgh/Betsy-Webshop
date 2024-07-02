from peewee import *
from models import Product, ProductTag, Transaction
import logging

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
        # Assuming Product.select() and Product.create() are part of an ORM like Peewee
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

