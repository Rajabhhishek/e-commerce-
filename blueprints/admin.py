from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models import db, Shop, User, Order, Product, Category, OrderLog

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        return "Access Denied: Admin privileges required.", 403
    return render_template('admin/dashboard.html')

@admin_bp.route('/api/shops/approve', methods=['POST'])
@login_required
def approve_shop():
    if current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Access denied.'}), 403

    data = request.get_json() or {}
    shop_id = data.get('shop_id')
    action = data.get('action') # 'APPROVED' or 'REJECTED'

    if not shop_id or action not in ['APPROVED', 'REJECTED']:
        return jsonify({'success': False, 'message': 'Invalid parameters.'}), 400

    shop = Shop.query.get_or_404(shop_id)
    
    try:
        shop.status = action.lower()
        db.session.commit()
        return jsonify({'success': True, 'message': f'Shop successfully {shop.status}.', 'shop': shop.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_bp.route('/api/analytics', methods=['GET'])
@login_required
def get_analytics():
    if current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Access denied.'}), 403

    # Calculate basic KPIs
    total_sales = db.session.query(db.func.sum(Order.total_amount)).filter_by(status='DELIVERED').scalar() or 0.0
    total_gst = db.session.query(db.func.sum(Order.gst_amount)).filter_by(status='DELIVERED').scalar() or 0.0
    total_orders = Order.query.count()
    delivered_orders = Order.query.filter_by(status='DELIVERED').count()
    pending_shops = Shop.query.filter_by(status='pending').count()

    # Formulate mock report payload for Chart.js frontend widgets
    report = {
        'total_revenue': round(total_sales, 2),
        'total_gst': round(total_gst, 2),
        'net_platform_commission': round((total_sales - total_gst) * 0.1, 2), # 10% platform share
        'orders_count': total_orders,
        'delivered_count': delivered_orders,
        'pending_shops_count': pending_shops
    }

    return jsonify({'success': True, 'analytics': report})

@admin_bp.route('/api/products', methods=['GET'])
@login_required
def get_all_products():
    if current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Access denied.'}), 403
    products = Product.query.order_by(Product.id.desc()).all()
    return jsonify([p.to_dict() for p in products])

@admin_bp.route('/api/categories', methods=['GET'])
@login_required
def get_categories():
    categories = Category.query.all()
    return jsonify([c.to_dict() for c in categories])

@admin_bp.route('/api/product/add', methods=['POST'])
@login_required
def add_product():
    if current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Access denied.'}), 403
        
    data = request.get_json() or {}
    name = data.get('name')
    price = data.get('price', 0.0)
    stock = data.get('stock', 0)
    description = data.get('description', '')
    category_id = data.get('category_id')
    
    if not name or not category_id:
        return jsonify({'success': False, 'message': 'Product Name and Category are required.'}), 400
        
    try:
        # Default to first available shop since Admin acts globally
        default_shop = Shop.query.first()
        if not default_shop:
            return jsonify({'success': False, 'message': 'No registered shops found in the system to host this product.'}), 400

        new_prod = Product(
            name=name,
            price=float(price),
            stock=int(stock),
            description=description,
            category_id=int(category_id),
            shop_id=default_shop.id,
            image_url='https://lh3.googleusercontent.com/aida-public/AB6AXuAQG0rmKccsHKgPGjsNKBz-FT9CC6XvPxfAkMDHs3KEMomwpEnXheWaz0kolZl9G5yifjKFPWHfBB4qa7LeOH9aP8F-0hkEgV5OjAZLS5mRjvqT887PCSBfYOgdNq9Npqz8tEpl5x9hN7-1ZHVOjGdsLOIDzqdZh3bfcaapO5KfJZ-Jqg1kXW7tyAMCMydmtbLOZ8o45lbAZ28F7C9AP0QeBfqLzMHuiz3GovQOe-XGEhQbQ1xw3j5vT5MQ4LPiqVlv5KiBsJ3CLcDX'
        )
        db.session.add(new_prod)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Global product added successfully!', 'product': new_prod.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_bp.route('/api/product/<int:product_id>/update', methods=['POST'])
@login_required
def update_product(product_id):
    if current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Access denied.'}), 403
        
    product = Product.query.get_or_404(product_id)
    data = request.get_json() or {}
    price = data.get('price')
    stock = data.get('stock')
    
    try:
        if price is not None:
            product.price = float(price)
        if stock is not None:
            product.stock = int(stock)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Global product updated successfully!', 'product': product.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_bp.route('/api/orders', methods=['GET'])
@login_required
def get_all_orders():
    if current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Access denied.'}), 403
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return jsonify([o.to_dict() for o in orders])

@admin_bp.route('/api/order/<int:order_id>/action', methods=['POST'])
@login_required
def order_action(order_id):
    if current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Access denied.'}), 403

    data = request.get_json() or {}
    action = data.get('action')

    order = Order.query.get_or_404(order_id)
    if order.status != 'PENDING':
        return jsonify({'success': False, 'message': f'Order is in {order.status} state.'}), 400

    try:
        if action == 'ACCEPT':
            order.status = 'ACCEPTED'
            log_desc = 'Order manually accepted by System Admin.'
        elif action == 'DECLINE':
            order.status = 'CANCELLED'
            log_desc = 'Order declined by System Admin. Stock restored.'
            for item in order.items:
                product = Product.query.get(item.product_id)
                if product:
                    product.stock += item.quantity
        else:
            return jsonify({'success': False, 'message': 'Invalid action.'}), 400

        log = OrderLog(order_id=order.id, status=order.status, description=log_desc)
        db.session.add(log)
        db.session.commit()
        return jsonify({'success': True, 'message': f'Order {order.status.lower()} by Admin.', 'order': order.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_bp.route('/api/order/<int:order_id>/ready', methods=['POST'])
@login_required
def order_ready(order_id):
    if current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Access denied.'}), 403

    order = Order.query.get_or_404(order_id)
    if order.status != 'ACCEPTED':
        return jsonify({'success': False, 'message': f'Order must be ACCEPTED first.'}), 400

    try:
        order.status = 'READY_FOR_PICKUP'
        log = OrderLog(
            order_id=order.id, 
            status='READY_FOR_PICKUP', 
            description='Admin marked order ready for Rider pickup.'
        )
        db.session.add(log)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Order marked ready.', 'order': order.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

