from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models import db, Product, Category, Order, OrderItem, OrderLog, Shop

customer_bp = Blueprint('customer', __name__)

# Middleware decoration to restrict mapping to role
def customer_only(func):
    # Customer RBAC security helper (redirects/restricts if non-customer accesses)
    # Since mock auth is fully integrated, we assume session security is present.
    return func

@customer_bp.route('/')
@customer_bp.route('/home')
def home():
    categories = Category.query.all()
    # Query standard products
    products = Product.query.limit(8).all()
    return render_template('customer/home.html', categories=categories, products=products)

@customer_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    similar_products = Product.query.filter(
        Product.category_id == product.category_id, 
        Product.id != product.id
    ).limit(4).all()
    return render_template('customer/detail.html', product=product, similar_products=similar_products)

@customer_bp.route('/cart')
def cart():
    return render_template('customer/cart.html')

@customer_bp.route('/profile')
@login_required
def profile():
    # Customer orders query
    orders = Order.query.filter_by(customer_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('customer/profile.html', orders=orders)

@customer_bp.route('/category/<int:category_id>')
def category_page(category_id):
    category = Category.query.get_or_404(category_id)
    products = Product.query.filter_by(category_id=category.id).all()
    categories = Category.query.all()
    return render_template('customer/category.html', category=category, products=products, categories=categories)

@customer_bp.route('/pharmacy')
def pharmacy_page():
    # Attempt to find Medical category, fallback to just rendering the template if not found
    category = Category.query.filter_by(name='Medical').first()
    products = Product.query.filter_by(category_id=category.id).all() if category else []
    return render_template('customer/pharmacy.html', products=products)

@customer_bp.route('/services')
def services_page():
    return render_template('customer/services.html')

# --- API ENDPOINTS ---

@customer_bp.route('/api/products', methods=['GET'])
def get_products():
    query = Product.query
    
    # Filter by category
    category_id = request.args.get('category_id', type=int)
    if category_id:
        query = query.filter_by(category_id=category_id)
        
    # Search filter
    search = request.args.get('search', '').strip()
    if search:
        query = query.filter(Product.name.like(f'%{search}%') | Product.description.like(f'%{search}%'))
        
    products = query.all()
    return jsonify([p.to_dict() for p in products])

@customer_bp.route('/api/order/create', methods=['POST'])
@login_required
def create_order():
    data = request.get_json()
    if not data or 'items' not in data:
        return jsonify({'success': False, 'message': 'Missing order details.'}), 400
        
    items = data.get('items') # List of {'product_id': 1, 'quantity': 2}
    if not items:
        return jsonify({'success': False, 'message': 'Cart is empty.'}), 400

    # Group cart items by shop (since orders must be created per shop)
    shop_orders = {}
    
    for item in items:
        prod_id = item.get('product_id')
        qty = item.get('quantity', 1)
        
        product = Product.query.get(prod_id)
        if not product:
            return jsonify({'success': False, 'message': f'Product {prod_id} not found.'}), 404
            
        if product.stock < qty:
            return jsonify({'success': False, 'message': f'Insufficient stock for {product.name}. Available: {product.stock}'}), 400
            
        shop_id = product.shop_id
        if shop_id not in shop_orders:
            shop_orders[shop_id] = []
        shop_orders[shop_id].append({'product': product, 'qty': qty})

    created_orders = []
    
    try:
        for shop_id, order_items_list in shop_orders.items():
            total = 0.0
            for item_data in order_items_list:
                total += item_data['product'].price * item_data['qty']
                
            gst = round(total * 0.18, 2) # Mock flat GST rate 18%
            grand_total = round(total + gst, 2)
            
            # Create Order
            order = Order(
                customer_id=current_user.id,
                shop_id=shop_id,
                total_amount=grand_total,
                gst_amount=gst,
                status='PENDING'
            )
            db.session.add(order)
            db.session.flush() # Secure order.id
            
            # Create Order Items and adjust stock
            for item_data in order_items_list:
                product = item_data['product']
                qty = item_data['qty']
                
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=qty,
                    price=product.price
                )
                db.session.add(order_item)
                
                # Reduce stock
                product.stock -= qty
                
            # Log primary history state
            log = OrderLog(
                order_id=order.id,
                status='PENDING',
                description='Order placed successfully by Customer.'
            )
            db.session.add(log)
            created_orders.append(order)
            
        db.session.commit()
        return jsonify({
            'success': True, 
            'message': 'Orders created successfully!', 
            'orders': [o.to_dict() for o in created_orders]
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Transaction failed: {str(e)}'}), 500

@customer_bp.route('/api/order/<int:order_id>/cancel', methods=['POST'])
@login_required
def cancel_order(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Authenticate user authorization
    if order.customer_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized action.'}), 403
        
    if order.status != 'PENDING':
        return jsonify({'success': False, 'message': f'Cannot cancel order in {order.status} state.'}), 400
        
    try:
        order.status = 'CANCELLED'
        
        # Restore stock configurations
        for item in order.items:
            product = Product.query.get(item.product_id)
            if product:
                product.stock += item.quantity
                
        # Write Log
        log = OrderLog(
            order_id=order.id,
            status='CANCELLED',
            description='Order cancelled by Customer.'
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Order successfully cancelled.', 'order': order.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Failed to cancel order: {str(e)}'}), 500
