"""Product CRUD endpoints with validation and error handling"""
from flask import Blueprint, request, jsonify, abort
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Product
from app.schemas import ProductSchema, ProductCreateSchema, ProductUpdateSchema, ProductQuerySchema

bp = Blueprint('products', __name__)

# Initialize schemas
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
product_create_schema = ProductCreateSchema()
product_update_schema = ProductUpdateSchema()
product_query_schema = ProductQuerySchema()


def make_response(data, success=True, status_code=200):
    """Standardize API response format"""
    response = {
        'success': success,
        'data': data if success else None,
        'meta': {
            'version': '2.0.0',
            'endpoint': request.endpoint
        }
    }
    if not success:
        response['error'] = data
    return jsonify(response), status_code


@bp.route('', methods=['GET'])
def get_products():
    """
    Get all products with optional filtering, sorting and pagination
    
    Query Parameters:
        - page: Page number (default: 1)
        - per_page: Items per page (default: 10, max: 100)
        - category: Filter by category
        - search: Search by name
        - sort_by: Sort field (name, price, created_at, stock)
        - sort_order: asc or desc (default: desc)
    """
    try:
        # Validate query parameters
        query_params = product_query_schema.load(request.args.to_dict() or {})
        
        page = query_params.get('page', 1)
        per_page = query_params.get('per_page', 10)
        category = query_params.get('category')
        search = query_params.get('search')
        sort_by = query_params.get('sort_by', 'created_at')
        sort_order = query_params.get('sort_order', 'desc')
        
        # Build query
        query = Product.query.filter_by(is_active=True)
        
        if category:
            query = query.filter_by(category=category)
        
        if search:
            query = query.filter(Product.name.ilike(f'%{search}%'))
        
        # Apply sorting
        sort_column = getattr(Product, sort_by, Product.created_at)
        if sort_order == 'desc':
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)
        
        # Execute pagination
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return make_response({
            'items': products_schema.dump(pagination.items),
            'pagination': {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total_pages': pagination.pages,
                'total_items': pagination.total,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        })
        
    except ValidationError as err:
        return make_response({
            'code': 400,
            'message': 'Validation error',
            'details': err.messages
        }, success=False, status_code=400)


@bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a single product by ID"""
    product = Product.get_by_id(product_id)
    
    if not product:
        return make_response({
            'code': 404,
            'message': 'Product not found',
            'details': f'Product with ID {product_id} does not exist'
        }, success=False, status_code=404)
    
    return make_response(product_schema.dump(product))


@bp.route('', methods=['POST'])
def create_product():
    """
    Create a new product
    
    Request Body:
        - name (required): Product name
        - description: Product description
        - price (required): Product price (must be >= 0)
        - stock (required): Product stock (must be >= 0)
        - sku (required): Unique SKU (3-50 chars)
        - category (required): Product category
    """
    try:
        json_data = request.get_json()
        
        if not json_data:
            return make_response({
                'code': 400,
                'message': 'Bad Request',
                'details': 'Request body is required'
            }, success=False, status_code=400)
        
        # Validate input data
        validated_data = product_create_schema.load(json_data)
        
        # Check if SKU already exists
        existing = Product.get_by_sku(validated_data['sku'])
        if existing:
            return make_response({
                'code': 409,
                'message': 'Conflict',
                'details': f"Product with SKU '{validated_data['sku']}' already exists"
            }, success=False, status_code=409)
        
        # Create product
        product = Product(**validated_data)
        db.session.add(product)
        db.session.commit()
        
        return make_response({
            'message': 'Product created successfully',
            'product': product_schema.dump(product)
        }, status_code=201)
        
    except ValidationError as err:
        return make_response({
            'code': 422,
            'message': 'Validation error',
            'details': err.messages
        }, success=False, status_code=422)
    
    except IntegrityError as e:
        db.session.rollback()
        return make_response({
            'code': 409,
            'message': 'Database error',
            'details': 'SKU already exists'
        }, success=False, status_code=409)


@bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """
    Update an existing product
    
    Request Body (all optional):
        - name: Product name
        - description: Product description
        - price: Product price (must be >= 0)
        - stock: Product stock (must be >= 0)
        - category: Product category
        - is_active: Boolean flag
    """
    product = Product.get_by_id(product_id)
    
    if not product:
        return make_response({
            'code': 404,
            'message': 'Product not found',
            'details': f'Product with ID {product_id} does not exist'
        }, success=False, status_code=404)
    
    try:
        json_data = request.get_json()
        
        if not json_data:
            return make_response({
                'code': 400,
                'message': 'Bad Request',
                'details': 'Request body is required'
            }, success=False, status_code=400)
        
        # Validate input data
        validated_data = product_update_schema.load(json_data)
        
        # Update product fields
        for key, value in validated_data.items():
            setattr(product, key, value)
        
        db.session.commit()
        
        return make_response({
            'message': 'Product updated successfully',
            'product': product_schema.dump(product)
        })
        
    except ValidationError as err:
        return make_response({
            'code': 422,
            'message': 'Validation error',
            'details': err.messages
        }, success=False, status_code=422)


@bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Soft delete a product (mark as inactive)"""
    product = Product.get_by_id(product_id)
    
    if not product:
        return make_response({
            'code': 404,
            'message': 'Product not found',
            'details': f'Product with ID {product_id} does not exist'
        }, success=False, status_code=404)
    
    # Soft delete
    product.is_active = False
    db.session.commit()
    
    return make_response({
        'message': 'Product deleted successfully',
        'product_id': product_id
    })


@bp.route('/<int:product_id>/restore', methods=['POST'])
def restore_product(product_id):
    """Restore a soft-deleted product"""
    product = Product.query.get(product_id)
    
    if not product:
        return make_response({
            'code': 404,
            'message': 'Product not found',
            'details': f'Product with ID {product_id} does not exist'
        }, success=False, status_code=404)
    
    if product.is_active:
        return make_response({
            'code': 400,
            'message': 'Bad Request',
            'details': 'Product is already active'
        }, success=False, status_code=400)
    
    product.is_active = True
    db.session.commit()
    
    return make_response({
        'message': 'Product restored successfully',
        'product': product_schema.dump(product)
    })


@bp.route('/stats', methods=['GET'])
def get_stats():
    """Get product statistics"""
    total_products = Product.query.filter_by(is_active=True).count()
    total_value = db.session.query(db.func.sum(Product.price * Product.stock)).scalar() or 0
    total_stock = db.session.query(db.func.sum(Product.stock)).scalar() or 0
    
    categories = db.session.query(
        Product.category,
        db.func.count(Product.id).label('count')
    ).filter_by(is_active=True).group_by(Product.category).all()
    
    return make_response({
        'total_products': total_products,
        'total_inventory_value': round(float(total_value), 2),
        'total_stock': int(total_stock),
        'categories': [{'name': cat, 'count': count} for cat, count in categories]
    })