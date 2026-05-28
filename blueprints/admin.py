from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models import db, Shop, User, Order

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
