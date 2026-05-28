from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Secure role redirection
        if current_user.role == 'customer':
            return redirect(url_for('customer.home'))
        elif current_user.role == 'vendor':
            return redirect(url_for('vendor.dashboard'))
        elif current_user.role == 'delivery':
            return redirect(url_for('delivery.dashboard'))
        elif current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        # Accept JSON submissions for premium frontend dynamic compatibility
        if request.is_json:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            role = data.get('role', 'customer')
        else:
            email = request.form.get('email')
            password = request.form.get('password')
            role = request.form.get('role', 'customer')

        user = User.query.filter_by(email=email).first()
        
        # Verify credentials and appropriate role access
        if user and user.check_password(password):
            
            if user.status != 'active':
                if request.is_json:
                    return jsonify({'success': False, 'message': 'Account is suspended or pending approval.'}), 403
                flash('Account is suspended or pending.', 'warning')
                return redirect(url_for('auth.login'))

            login_user(user, remember=True)
            
            # Formulate dynamic response redirects mapping template paths
            redirect_url = url_for('customer.home')
            if user.role == 'vendor':
                redirect_url = url_for('vendor.dashboard')
            elif user.role == 'delivery':
                redirect_url = url_for('delivery.dashboard')
            elif user.role == 'admin':
                redirect_url = url_for('admin.dashboard')

            if request.is_json:
                return jsonify({
                    'success': True, 
                    'message': 'Authorized successfully.', 
                    'redirect': redirect_url,
                    'user': user.to_dict()
                })
            return redirect(redirect_url)
        else:
            if request.is_json:
                return jsonify({'success': False, 'message': 'Invalid email or password.'}), 401
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('auth.login'))

    # GET request: render dynamic login screen
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('customer.home'))
        
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
        else:
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')

        if not username or not email or not password:
            if request.is_json:
                return jsonify({'success': False, 'message': 'Please fill all fields.'}), 400
            flash('Please fill all fields.', 'danger')
            return redirect(url_for('auth.register'))

        # Check existing email
        if User.query.filter_by(email=email).first():
            if request.is_json:
                return jsonify({'success': False, 'message': 'Email address already registered.'}), 400
            flash('Email already registered.', 'danger')
            return redirect(url_for('auth.register'))

        # Check existing username
        if User.query.filter_by(username=username).first():
            if request.is_json:
                return jsonify({'success': False, 'message': 'Username already taken.'}), 400
            flash('Username already taken.', 'danger')
            return redirect(url_for('auth.register'))

        try:
            # Force role to 'customer' - only customers can register themselves!
            new_user = User(username=username, email=email, role='customer', status='active')
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            
            # Auto login customer
            login_user(new_user, remember=True)
            
            redirect_url = url_for('customer.home')
            if request.is_json:
                return jsonify({
                    'success': True,
                    'message': 'Account created successfully! Welcome to ShopSmart.',
                    'redirect': redirect_url,
                    'user': new_user.to_dict()
                })
            return redirect(redirect_url)
        except Exception as e:
            db.session.rollback()
            if request.is_json:
                return jsonify({'success': False, 'message': f'Failed to create account: {str(e)}'}), 500
            flash(f'Failed to create account: {str(e)}', 'danger')
            return redirect(url_for('auth.register'))

    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/session', methods=['GET'])
def get_session():
    # Session state check endpoint
    if current_user.is_authenticated:
        return jsonify({'authenticated': True, 'user': current_user.to_dict()})
    return jsonify({'authenticated': False}), 200
