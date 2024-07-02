from peewee import *
from peewee import DateTimeField, DecimalField, IntegerField, TextField, ForeignKeyField, CharField, Model, SqliteDatabase, Check
from datetime import datetime

db = SqliteDatabase('my_database.db')

class User(Model):
    name = CharField()
    email = CharField(unique=True)
    address = CharField()
    billing_info = CharField()

    class Meta:
        database = db
        
class Product(Model):
    user = ForeignKeyField(User, backref='products')
    name = CharField()
    description = TextField()
    price_per_unit = DecimalField()
    quantity_in_stock = IntegerField()
    is_active = BooleanField(default=True)

    class Meta:
        database = db
        indexes = (
            (('name', 'description'), False),
        )

class Tag(Model):
    name = CharField(unique=True)
    description = TextField(null=True)

    class Meta:
        database = db

class ProductTag(Model):
    product = ForeignKeyField(Product, backref='product_tags')
    tag = ForeignKeyField(Tag, backref='product_tags')
    created_at = DateTimeField(default=datetime.now)
    
    class Meta:
        database = db

class Transaction(Model):
    user = ForeignKeyField(User, backref='transactions')
    product = ForeignKeyField(Product, backref='transactions')
    quantity = IntegerField(constraints=[Check('quantity > 0')])
    timestamp = DateTimeField(default=datetime.now)
    total_price = DecimalField(constraints=[Check('total_price >= 0.00')])

    class Meta:
        database = db
        indexes = (
            (('user', 'timestamp'), False),
            (('product', 'timestamp'), False),
        )

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