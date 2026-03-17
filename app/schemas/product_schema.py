"""Product schemas for validation and serialization"""
from marshmallow import Schema, fields, validate, validates, ValidationError
from app import ma


class ProductSchema(ma.SQLAlchemyAutoSchema):
    """Product schema for serialization"""
    class Meta:
        from app.models import Product
        model = Product
        include_fk = True
    
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=2, max=100))
    description = fields.String(allow_none=True, validate=validate.Length(max=500))
    price = fields.Float(required=True, validate=validate.Range(min=0))
    stock = fields.Integer(required=True, validate=validate.Range(min=0))
    sku = fields.String(required=True, validate=validate.Length(min=3, max=50))
    category = fields.String(required=True, validate=validate.Length(min=1, max=50))
    is_active = fields.Boolean(dump_default=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class ProductCreateSchema(Schema):
    """Schema for creating a new product"""
    name = fields.String(required=True, validate=validate.Length(min=2, max=100), 
                         error_messages={"required": "Name is required"})
    description = fields.String(allow_none=True, validate=validate.Length(max=500))
    price = fields.Float(required=True, validate=validate.Range(min=0, error="Price must be >= 0"),
                          error_messages={"required": "Price is required"})
    stock = fields.Integer(required=True, validate=validate.Range(min=0, error="Stock must be >= 0"),
                           error_messages={"required": "Stock is required"})
    sku = fields.String(required=True, validate=validate.Length(min=3, max=50),
                        error_messages={"required": "SKU is required"})
    category = fields.String(required=True, validate=validate.Length(min=1, max=50),
                             error_messages={"required": "Category is required"})
    
    @validates('sku')
    def validate_sku_unique(self, value):
        """Validate SKU uniqueness"""
        from app.models import Product
        existing = Product.get_by_sku(value)
        if existing:
            raise ValidationError(f"SKU '{value}' already exists")


class ProductUpdateSchema(Schema):
    """Schema for updating a product"""
    name = fields.String(validate=validate.Length(min=2, max=100))
    description = fields.String(allow_none=True, validate=validate.Length(max=500))
    price = fields.Float(validate=validate.Range(min=0, error="Price must be >= 0"))
    stock = fields.Integer(validate=validate.Range(min=0, error="Stock must be >= 0"))
    category = fields.String(validate=validate.Length(min=1, max=50))
    is_active = fields.Boolean()
    
    @validates('sku')
    def validate_sku_not_changed(self, value):
        """Prevent SKU changes on update"""
        raise ValidationError("SKU cannot be changed after creation")


class ProductQuerySchema(Schema):
    """Schema for query parameters"""
    page = fields.Integer(validate=validate.Range(min=1), load_default=1)
    per_page = fields.Integer(validate=validate.Range(min=1, max=100), load_default=10)
    category = fields.String(validate=validate.Length(max=50))
    search = fields.String(validate=validate.Length(max=100))
    sort_by = fields.String(validate=validate.OneOf(['name', 'price', 'created_at', 'stock']))
    sort_order = fields.String(validate=validate.OneOf(['asc', 'desc']), load_default='desc')