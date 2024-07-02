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