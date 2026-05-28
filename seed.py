from app import app
from models import db, User, Category, Shop, Product

def seed_database():
    print("Initializing database seeder...")
    
    with app.app_context():
        # Wipe all records to ensure a clean run
        print("Clearing existing data...")
        db.drop_all()
        db.create_all()
        
        # 1. Create Core Categories
        print("Creating product categories...")
        categories_data = [
            {'name': 'Grocery', 'description': 'Fresh produce, grains, and kitchen essentials.'},
            {'name': 'Medical', 'description': 'Pharmacy supplies, first-aid, and health devices.'},
            {'name': 'Cake', 'description': 'Freshly baked cakes, pastries, and sweet treats.'},
            {'name': 'Daily Need', 'description': 'Everyday household essentials and personal care.'}
        ]
        
        categories = {}
        for cat_info in categories_data:
            cat = Category(name=cat_info['name'], description=cat_info['description'])
            db.session.add(cat)
            categories[cat_info['name']] = cat
            
        db.session.flush() # Secure category IDs
        
        # 2. Create Core Users matching login autofill parameters
        print("Creating mock user accounts...")
        
        # Customer
        customer = User(username='AlexCustomer', email='customer@shopsmart.com', role='customer')
        customer.set_password('customerPass123')
        db.session.add(customer)
        
        # Vendor
        vendor = User(username='TechMerchant', email='vendor_electronics@shopsmart.com', role='vendor')
        vendor.set_password('vendorSecret99')
        db.session.add(vendor)
        
        # Delivery Rider
        rider = User(username='SwiftRider', email='rider_fast@shopsmart.com', role='delivery')
        rider.set_password('riderDrive77')
        db.session.add(rider)
        
        # System Admin
        admin = User(username='SuperAdmin', email='admin_portal@shopsmart.com', role='admin')
        admin.set_password('adminControl00')
        db.session.add(admin)
        
        db.session.flush() # Secure User IDs
        
        # 3. Create Shop registered under Vendor User
        print("Creating shop profiles...")
        shop = Shop(name='SuperMart HQ', vendor_id=vendor.id, status='approved')
        db.session.add(shop)
        
        db.session.flush() # Secure Shop ID
        
        # 4. Create Initial Products mapping to homepage showcase
        print("Seeding premium product showcase items...")
        products_data = [
            # GROCERY
            {
                'name': 'Organic Basmati Chawal (5kg)',
                'description': 'Premium quality long-grain aromatic basmati rice.',
                'price': 450.00,
                'stock': 150,
                'category': 'Grocery',
                'image_url': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=400&q=80'
            },
            {
                'name': 'Yellow Toor Dal (1kg)',
                'description': 'Unpolished, high-protein yellow pigeon peas.',
                'price': 160.00,
                'stock': 200,
                'category': 'Grocery',
                'image_url': 'https://images.unsplash.com/photo-1585996884639-5bb8e461a293?auto=format&fit=crop&w=400&q=80'
            },
            {
                'name': 'Whole Wheat Atta (10kg)',
                'description': '100% whole wheat chakki fresh atta for soft rotis.',
                'price': 380.00,
                'stock': 100,
                'category': 'Grocery',
                'image_url': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=400&q=80'
            },
            {
                'name': 'Refined Sunflower Oil (1L)',
                'description': 'Healthy and light refined sunflower oil enriched with vitamins.',
                'price': 140.00,
                'stock': 300,
                'category': 'Grocery',
                'image_url': 'https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?auto=format&fit=crop&w=400&q=80'
            },
            
            # MEDICAL
            {
                'name': 'Paracetamol 500mg (10 Tablets)',
                'description': 'Fast-acting fever and pain relief medication.',
                'price': 30.00,
                'stock': 500,
                'category': 'Medical',
                'image_url': 'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?auto=format&fit=crop&w=400&q=80'
            },
            {
                'name': 'Antiseptic Liquid (250ml)',
                'description': 'Multipurpose germ protection liquid for first-aid.',
                'price': 85.00,
                'stock': 120,
                'category': 'Medical',
                'image_url': 'https://images.unsplash.com/photo-1584017911766-d451b3d0e843?auto=format&fit=crop&w=400&q=80'
            },
            {
                'name': 'Cough Syrup (100ml)',
                'description': 'Soothing syrup for dry and wet cough relief.',
                'price': 110.00,
                'stock': 80,
                'category': 'Medical',
                'image_url': 'https://images.unsplash.com/photo-1587854692152-cbe660dbde88?auto=format&fit=crop&w=400&q=80'
            },
            {
                'name': 'Waterproof Band-Aids (Pack of 20)',
                'description': 'Sterile adhesive bandages for minor cuts and wounds.',
                'price': 45.00,
                'stock': 250,
                'category': 'Medical',
                'image_url': 'https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=400&q=80'
            },

            # DAILY NEED
            {
                'name': 'Heavy Duty Plastic Bucket (20L)',
                'description': 'Durable and unbreakable plastic bucket for bathroom.',
                'price': 250.00,
                'stock': 60,
                'category': 'Daily Need',
                'image_url': 'https://images.unsplash.com/photo-1585659722983-36cb2b46906a?auto=format&fit=crop&w=400&q=80'
            },
            {
                'name': 'Liquid Dish Wash (500ml)',
                'description': 'Tough on grease, gentle on hands with lemon extracts.',
                'price': 99.00,
                'stock': 150,
                'category': 'Daily Need',
                'image_url': 'https://images.unsplash.com/photo-1584813539806-2538b8d918c6?auto=format&fit=crop&w=400&q=80'
            },
            {
                'name': 'Floor Cleaning Broom (Phool Jhadu)',
                'description': 'Premium quality grass broom for everyday sweeping.',
                'price': 120.00,
                'stock': 90,
                'category': 'Daily Need',
                'image_url': 'https://images.unsplash.com/photo-1527515862127-a4fc05baf7a5?auto=format&fit=crop&w=400&q=80'
            },
            {
                'name': 'Antibacterial Bath Soap (Pack of 4)',
                'description': 'Deep cleansing and moisturizing body soap bars.',
                'price': 145.00,
                'stock': 200,
                'category': 'Daily Need',
                'image_url': 'https://images.unsplash.com/photo-1600857544200-b2f666a9a2ec?auto=format&fit=crop&w=400&q=80'
            },

            # CAKE
            {
                'name': 'Rich Chocolate Truffle Cake (1kg)',
                'description': 'Decadent, moist dark chocolate cake loaded with ganache.',
                'price': 650.00,
                'stock': 15,
                'category': 'Cake',
                'image_url': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=400&q=80'
            },
            {
                'name': 'Classic Black Forest Cake (500g)',
                'description': 'Layered chocolate sponge with whipped cream and cherries.',
                'price': 350.00,
                'stock': 20,
                'category': 'Cake',
                'image_url': 'https://images.unsplash.com/photo-1606890737304-57a1ca8a5b62?auto=format&fit=crop&w=400&q=80'
            },
            {
                'name': 'Fresh Pineapple Cake (1kg)',
                'description': 'Soft vanilla sponge loaded with fresh pineapple chunks.',
                'price': 550.00,
                'stock': 12,
                'category': 'Cake',
                'image_url': 'https://images.unsplash.com/photo-1557925923-33b251fc3262?auto=format&fit=crop&w=400&q=80'
            },
            {
                'name': 'Red Velvet Cupcakes (Box of 6)',
                'description': 'Moist red velvet cupcakes topped with cream cheese frosting.',
                'price': 300.00,
                'stock': 25,
                'category': 'Cake',
                'image_url': 'https://images.unsplash.com/photo-1616541823729-00fe0aacd32c?auto=format&fit=crop&w=400&q=80'
            }
        ]
        
        for prod_info in products_data:
            product = Product(
                name=prod_info['name'],
                description=prod_info['description'],
                price=prod_info['price'],
                stock=prod_info['stock'],
                category_id=categories[prod_info['category']].id,
                shop_id=shop.id,
                image_url=prod_info['image_url']
            )
            db.session.add(product)
            
        db.session.commit()
        print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed_database()
