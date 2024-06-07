from peewee import *
from peewee import DateTimeField
from datetime import datetime

db = SqliteDatabase('my_database.db')

class User(Model):
    name = CharField()
    address = CharField()
    billing_info = CharField()

    class Meta:
        database = db

class Product(Model):
    user = ForeignKeyField(User, backref='products')
    name = CharField()
    description = TextField()

    class Meta:
        indexes = (
            (('name', 'description'), False),
        )
        
class Product(Model):
    user = ForeignKeyField(User, backref='products')
    name = CharField()
    description = TextField()
    price_per_unit = DecimalField()
    quantity_in_stock = IntegerField()

    class Meta:
        database = db

class Tag(Model):
    name = CharField(unique=True)

    class Meta:
        database = db

class ProductTag(Model):
    product = ForeignKeyField(Product, backref='product_tags')
    tag = ForeignKeyField(Tag, backref='product_tags')

    class Meta:
        database = db
        indexes = (
            # Create a unique index on product/tag
            (('product', 'tag'), True),
        )

class Transaction(Model):
    user = ForeignKeyField(User, backref='transactions')
    product = ForeignKeyField(Product, backref='transactions')
    quantity = IntegerField(constraints=[Check('quantity > 0')])
    timestamp = DateTimeField(default=datetime.now)
    total_price = DecimalField(constraints=[Check('total_price >= 0.00')])

    class Meta:
        database = db

# Connect to the database
db.connect()

# Delete the tables
db.drop_tables([User, Product, Tag, ProductTag, Transaction])

# Create the tables
db.create_tables([User, Product, Tag, ProductTag, Transaction])



