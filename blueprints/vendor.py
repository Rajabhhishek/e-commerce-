from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models import db, Order, OrderLog, Product, Shop, OrderItem, Category

vendor_bp = Blueprint('vendor', __name__, url_prefix='/vendor')

@vendor_bp.route('/dashboard')
@login_required
def dashboard():
    # Enforce role safety
    if current_user.role != 'vendor':
        return "Access Denied: Vendor privileges required.", 403
    
    # Render placeholder vendor panel dashboard template
    shop = Shop.query.filter_by(vendor_id=current_user.id).first()
    return render_template('vendor/dashboard.html', shop=shop)

@vendor_bp.route('/api/orders', methods=['GET'])
@login_required
def get_orders():
    if current_user.role != 'vendor':
        return jsonify({'success': False, 'message': 'Access denied.'}), 403

    shop = Shop.query.filter_by(vendor_id=current_user.id).first()
    if not shop:
        return jsonify({'success': False, 'message': 'Shop not registered.'}), 404

    orders = Order.query.filter_by(shop_id=shop.id).order_by(Order.created_at.desc()).all()
    return jsonify([o.to_dict() for o in orders])

@vendor_bp.route('/api/order/<int:order_id>/action', methods=['POST'])
@login_required
def order_action(order_id):
    if current_user.role != 'vendor':
        return jsonify({'success': False, 'message': 'Access denied.'}), 403

    data = request.get_json() or {}
    action = data.get('action') # 'ACCEPT' or 'DECLINE'

    shop = Shop.query.filter_by(vendor_id=current_user.id).first()
    order = Order.query.get_or_404(order_id)

    if order.shop_id != shop.id:
        return jsonify({'success': False, 'message': 'Unauthorized action.'}), 403

    if order.status != 'PENDING':
        return jsonify({'success': False, 'message': f'Order is in {order.status} state.'}), 400

    try:
        if action == 'ACCEPT':
            order.status = 'ACCEPTED'
            log_desc = 'Order accepted by Vendor. Preparation in progress.'
        elif action == 'DECLINE':
            order.status = 'CANCELLED'
            log_desc = 'Order declined by Vendor. Stock restored.'
            # Restore stock
            for item in order.items:
                product = Product.query.get(item.product_id)
                if product:
                    product.stock += item.quantity
        else:
            return jsonify({'success': False, 'message': 'Invalid action.'}), 400

        # Create Timeline Log
        log = OrderLog(order_id=order.id, status=order.status, description=log_desc)
        db.session.add(log)
        db.session.commit()

        return jsonify({'success': True, 'message': f'Order successfully {order.status.lower()}.', 'order': order.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@vendor_bp.route('/api/order/<int:order_id>/ready', methods=['POST'])
@login_required
def order_ready(order_id):
    if current_user.role != 'vendor':
        return jsonify({'success': False, 'message': 'Access denied.'}), 403

    shop = Shop.query.filter_by(vendor_id=current_user.id).first()
    order = Order.query.get_or_404(order_id)

    if order.shop_id != shop.id:
        return jsonify({'success': False, 'message': 'Unauthorized action.'}), 403

    if order.status != 'ACCEPTED':
        return jsonify({'success': False, 'message': f'Order must be ACCEPTED first. Current status: {order.status}'}), 400

    try:
        order.status = 'READY_FOR_PICKUP'
        
        log = OrderLog(
            order_id=order.id, 
            status='READY_FOR_PICKUP', 
            description='Order packed and ready for Rider pickup.'
        )
        db.session.add(log)
        db.session.commit()

        # Real-time socket event trigger should occur here in production (e.g. notify nearby riders)
        return jsonify({'success': True, 'message': 'Order marked ready for pickup.', 'order': order.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@vendor_bp.route('/api/products', methods=['GET'])
@login_required
def get_shop_products():
    if current_user.role != 'vendor':
        return jsonify({'success': False, 'message': 'Access denied.'}), 403
    shop = Shop.query.filter_by(vendor_id=current_user.id).first()
    if not shop:
        return jsonify({'success': False, 'message': 'Shop not registered.'}), 404
    products = Product.query.filter_by(shop_id=shop.id).all()
    return jsonify([p.to_dict() for p in products])

@vendor_bp.route('/api/categories', methods=['GET'])
@login_required
def get_categories():
    categories = Category.query.all()
    return jsonify([c.to_dict() for c in categories])

@vendor_bp.route('/api/product/add', methods=['POST'])
@login_required
def add_product():
    if current_user.role != 'vendor':
        return jsonify({'success': False, 'message': 'Access denied.'}), 403
    shop = Shop.query.filter_by(vendor_id=current_user.id).first()
    if not shop:
        return jsonify({'success': False, 'message': 'Shop not registered.'}), 404
        
    data = request.get_json() or {}
    name = data.get('name')
    price = data.get('price', 0.0)
    stock = data.get('stock', 0)
    description = data.get('description', '')
    category_id = data.get('category_id')
    
    if not name or not category_id:
        return jsonify({'success': False, 'message': 'Product Name and Category are required.'}), 400
        
    try:
        new_prod = Product(
            name=name,
            price=float(price),
            stock=int(stock),
            description=description,
            category_id=int(category_id),
            shop_id=shop.id,
            image_url='https://lh3.googleusercontent.com/aida-public/AB6AXuAQG0rmKccsHKgPGjsNKBz-FT9CC6XvPxfAkMDHs3KEMomwpEnXheWaz0kolZl9G5yifjKFPWHfBB4qa7LeOH9aP8F-0hkEgV5OjAZLS5mRjvqT887PCSBfYOgdNq9Npqz8tEpl5x9hN7-1ZHVOjGdsLOIDzqdZh3bfcaapO5KfJZ-Jqg1kXW7tyAMCMydmtbLOZ8o45lbAZ28F7C9AP0QeBfqLzMHuiz3GovQOe-XGEhQbQ1xw3j5vT5MQ4LPiqVlv5KiBsJ3CLcDX' # default mock headphones placeholder
        )
        db.session.add(new_prod)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Product added successfully!', 'product': new_prod.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@vendor_bp.route('/api/product/<int:product_id>/update', methods=['POST'])
@login_required
def update_product(product_id):
    if current_user.role != 'vendor':
        return jsonify({'success': False, 'message': 'Access denied.'}), 403
    shop = Shop.query.filter_by(vendor_id=current_user.id).first()
    product = Product.query.get_or_404(product_id)
    
    if product.shop_id != shop.id:
        return jsonify({'success': False, 'message': 'Unauthorized action.'}), 403
        
    data = request.get_json() or {}
    price = data.get('price')
    stock = data.get('stock')
    
    try:
        if price is not None:
            product.price = float(price)
        if stock is not None:
            product.stock = int(stock)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Product updated successfully!', 'product': product.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@vendor_bp.route('/api/pos/sale', methods=['POST'])
@login_required
def pos_sale():
    if current_user.role != 'vendor':
        return jsonify({'success': False, 'message': 'Access denied.'}), 403
    shop = Shop.query.filter_by(vendor_id=current_user.id).first()
    if not shop:
        return jsonify({'success': False, 'message': 'Shop not registered.'}), 404
        
    data = request.get_json() or {}
    items = data.get('items') # List of {'product_id': 1, 'quantity': 2}
    
    if not items:
        return jsonify({'success': False, 'message': 'No products in POS register.'}), 400
        
    try:
        total = 0.0
        products_to_update = []
        
        for item in items:
            p_id = item.get('product_id')
            qty = item.get('quantity', 1)
            
            product = Product.query.get(p_id)
            if not product or product.shop_id != shop.id:
                return jsonify({'success': False, 'message': f'Product {p_id} not found in your inventory.'}), 404
                
            if product.stock < qty:
                return jsonify({'success': False, 'message': f'Insufficient stock for {product.name}. Available: {product.stock}'}), 400
                
            total += product.price * qty
            products_to_update.append((product, qty))
            
        gst = round(total * 0.18, 2)
        grand_total = round(total + gst, 2)
        
        # Create Offline Delivered Order
        order = Order(
            customer_id=current_user.id, # Logged under vendor's session representing POS agent
            shop_id=shop.id,
            total_amount=grand_total,
            gst_amount=gst,
            status='DELIVERED' # Directly marked as DELIVERED because it was sold in-person
        )
        db.session.add(order)
        db.session.flush()
        
        for product, qty in products_to_update:
            product.stock -= qty
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=qty,
                price=product.price
            )
            db.session.add(order_item)
            
        # Create Log
        log = OrderLog(
            order_id=order.id,
            status='DELIVERED',
            description='In-store physical counter sale completed (POS Cash transaction).'
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'POS sale registered successfully!', 'order': order.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
