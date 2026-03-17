"""Product model"""
from datetime import datetime
from app import db


class Product(db.Model):
    """Product model for database"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    sku = db.Column(db.String(50), unique=True, nullable=False, index=True)
    category = db.Column(db.String(50), nullable=False, default='general')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'sku': self.sku,
            'category': self.category,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get_by_id(cls, product_id):
        """Get product by ID"""
        return cls.query.get(product_id)
    
    @classmethod
    def get_by_sku(cls, sku):
        """Get product by SKU"""
        return cls.query.filter_by(sku=sku).first()
    
    @classmethod
    def get_all_active(cls, page=1, per_page=10):
        """Get all active products with pagination"""
        return cls.query.filter_by(is_active=True).paginate(
            page=page, per_page=per_page, error_out=False
        )
    
    @classmethod
    def search_by_name(cls, name, page=1, per_page=10):
        """Search products by name"""
        return cls.query.filter(
            cls.name.ilike(f'%{name}%'),
            cls.is_active == True
        ).paginate(page=page, per_page=per_page, error_out=False)
    
    @classmethod
    def filter_by_category(cls, category, page=1, per_page=10):
        """Filter products by category"""
        return cls.query.filter_by(
            category=category,
            is_active=True
        ).paginate(page=page, per_page=per_page, error_out=False)