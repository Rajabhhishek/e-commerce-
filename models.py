from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize SQLite SQLAlchemy database binder
db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='customer') # customer, vendor, delivery, admin
    status = db.Column(db.String(20), nullable=False, default='active') # active, pending, suspended
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    shops = db.relationship('Shop', backref='vendor', lazy=True)
    orders = db.relationship('Order', backref='customer', lazy=True, foreign_keys='Order.customer_id')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }

class Shop(db.Model):
    __tablename__ = 'shops'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='approved') # approved, pending, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='shop', lazy=True)
    orders = db.relationship('Order', backref='shop', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'vendor_id': self.vendor_id,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    description = db.Column(db.String(256))
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False, default=0.0)
    stock = db.Column(db.Integer, nullable=False, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'), nullable=False)
    image_url = db.Column(db.String(512))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'category_id': self.category_id,
            'shop_id': self.shop_id,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat()
        }

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    gst_amount = db.Column(db.Float, nullable=False, default=0.0)
    status = db.Column(db.String(30), nullable=False, default='PENDING') 
    # PENDING, ACCEPTED, READY_FOR_PICKUP, OUT_FOR_DELIVERY, DELIVERED, CANCELLED, FAILED
    
    delivery_boy_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")
    logs = db.relationship('OrderLog', backref='order', lazy=True, cascade="all, delete-orphan")
    
    # Explicitly map double-user key relation for delivery rider
    delivery_boy = db.relationship('User', foreign_keys=[delivery_boy_id], backref='delivery_jobs', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'shop_id': self.shop_id,
            'total_amount': self.total_amount,
            'gst_amount': self.gst_amount,
            'status': self.status,
            'delivery_boy_id': self.delivery_boy_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'items': [item.to_dict() for item in self.items],
            'logs': [log.to_dict() for log in self.logs]
        }

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Float, nullable=False) # Purchase price lock
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price': self.price
        }

class OrderLog(db.Model):
    __tablename__ = 'order_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    status = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'status': self.status,
            'description': self.description,
            'created_at': self.created_at.isoformat()
        }
