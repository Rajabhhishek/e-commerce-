from flask import Flask
from flask_login import LoginManager
from flask_socketio import SocketIO, emit
from config import Config
from models import db, User

# Initialize core system hooks
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'

# Initialize SocketIO for high-telemetry realtime streams with standard threading async fallback
socketio = SocketIO(async_mode='threading')

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize SQL extensions
    db.init_app(app)
    
    # Initialize Session Authentications
    login_manager.init_app(app)
    
    # Initialize Realtime Sockets
    socketio.init_app(app, cors_allowed_origins="*", async_mode='threading')

    # User loader hook for flask-login session state persistence
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints (Modular role controllers)
    from blueprints.auth import auth_bp
    from blueprints.customer import customer_bp
    from blueprints.vendor import vendor_bp
    from blueprints.delivery import delivery_bp
    from blueprints.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(vendor_bp)
    app.register_blueprint(delivery_bp)
    app.register_blueprint(admin_bp)

    # Automatically create SQLite tables if database file is missing
    with app.app_context():
        db.create_all()

    return app

app = create_app()

# --- REAL-TIME TELEMETRY CHANNELS (Flask-SocketIO events) ---

@socketio.on('connect')
def handle_connect():
    print("Real-time telemetry stream client connected.")

@socketio.on('join_order_room')
def on_join(data):
    # Enable private rooms so customers only receive updates for their specific orders
    room = f"order_{data.get('order_id')}"
    print(f"Client joining real-time updates room: {room}")

@socketio.on('update_location')
def handle_location(data):
    # Rider pushes coordinates, stream directly to customer dashboard
    order_id = data.get('order_id')
    lat = data.get('lat')
    lng = data.get('lng')
    
    emit('location_changed', {
        'order_id': order_id, 
        'lat': lat, 
        'lng': lng
    }, to=f"order_{order_id}")
    print(f"Rider pushed telemetry: Order {order_id} at ({lat}, {lng})")

if __name__ == '__main__':
    # Starts standard development server with unsafe werkzeug flag enabled for local debugger testing
    socketio.run(app, debug=True, host='127.0.0.1', port=5000, allow_unsafe_werkzeug=True)
