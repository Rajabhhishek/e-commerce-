from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models import db, Order, OrderLog

delivery_bp = Blueprint('delivery', __name__, url_prefix='/delivery')

@delivery_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'delivery':
        return "Access Denied: Rider privileges required.", 403
    return render_template('delivery/dashboard.html')

@delivery_bp.route('/api/jobs', methods=['GET'])
@login_required
def get_jobs():
    if current_user.role != 'delivery':
        return jsonify({'success': False, 'message': 'Access denied.'}), 403

    # Query orders packed and waiting for rider assignment
    jobs = Order.query.filter_by(status='READY_FOR_PICKUP', delivery_boy_id=None).all()
    return jsonify([j.to_dict() for j in jobs])

@delivery_bp.route('/api/job/<int:order_id>/accept', methods=['POST'])
@login_required
def accept_job(order_id):
    if current_user.role != 'delivery':
        return jsonify({'success': False, 'message': 'Access denied.'}), 403

    order = Order.query.get_or_404(order_id)
    if order.status != 'READY_FOR_PICKUP' or order.delivery_boy_id is not None:
        return jsonify({'success': False, 'message': 'Job is no longer available.'}), 400

    try:
        order.delivery_boy_id = current_user.id
        order.status = 'OUT_FOR_DELIVERY'
        
        log = OrderLog(
            order_id=order.id, 
            status='OUT_FOR_DELIVERY', 
            description=f'Rider {current_user.username} picked up the items and is out for delivery.'
        )
        db.session.add(log)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Delivery job accepted!', 'order': order.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@delivery_bp.route('/api/job/<int:order_id>/deliver', methods=['POST'])
@login_required
def deliver_job(order_id):
    if current_user.role != 'delivery':
        return jsonify({'success': False, 'message': 'Access denied.'}), 403

    order = Order.query.get_or_404(order_id)
    if order.delivery_boy_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized action.'}), 403

    if order.status != 'OUT_FOR_DELIVERY':
        return jsonify({'success': False, 'message': f'Order is in {order.status} state, cannot deliver.'}), 400

    try:
        order.status = 'DELIVERED'
        
        log = OrderLog(
            order_id=order.id, 
            status='DELIVERED', 
            description='Order successfully delivered at destination.'
        )
        db.session.add(log)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Delivery completed successfully!', 'order': order.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
