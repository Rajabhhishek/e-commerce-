import os

class Config:
    # Flask application encryption key for secure cookies
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'shopsmart-ultra-secure-key-9988'
    
    # Path to SQLite relational database
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{os.path.join(BASE_DIR, "database.db")}'
    
    # Disable SQLAlchemy event modifications system to save memory resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Enable template auto-reload for local hot refresh
    TEMPLATES_AUTO_RELOAD = True
