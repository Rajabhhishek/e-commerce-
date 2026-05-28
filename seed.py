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
            {'name': 'Tech', 'description': 'Advanced computing, laptops, and technical gear.'},
            {'name': 'Fashion', 'description': 'Sleek luxury apparel, designs, and sunglasses.'},
            {'name': 'Home', 'description': 'Ergonomic furniture and ambient lightning fixtures.'},
            {'name': 'Sports', 'description': 'High-performance athletic gear and trainers.'},
            {'name': 'Beauty', 'description': 'Aesthetic skincare, cosmetics, and self-care.'},
            {'name': 'Audio', 'description': 'Premium studio over-ear headphones and listening gears.'},
            {'name': 'Pharmacy', 'description': 'Essential health supplies, medicine, and first-aid.'}
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
        shop = Shop(name='Kinetic Electronics Lab', vendor_id=vendor.id, status='approved')
        db.session.add(shop)
        
        db.session.flush() # Secure Shop ID
        
        # 4. Create Initial Products mapping to homepage showcase
        print("Seeding premium product showcase items...")
        products_data = [
            {
                'name': 'Kinetic Runners X1',
                'description': 'A pair of sleek, modern athletic sneakers featuring futuristic design elements and reflective materials.',
                'price': 129.00,
                'stock': 15,
                'category': 'Sports',
                'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuA-RM_AA_-yCKMjrkjPWujto6m0nTXtu5ROoAJ5GnibIw_m3KweU1daoZILogmKop5awrlCM_-ORVkQWz4RdbWBf1ziQPmLagaFzDFMoyNW6TtDnQj2Y0V8xGP0L96BHGJN9vY1EgeRkTono6Q_opgyx01TWb_d1-dmqNXd14xP83S8GcFp3gAcb34XaO-bgz9aUcOeFOKGcRslOlCWCTUnsvIjBeIWliuxvZITcGVO888MhB5X2NVWTQQAeGKry3S0-cVo5hxoCNAN'
            },
            {
                'name': 'WH-1000XM5 Dark',
                'description': 'Professional over-ear studio headphones with a matte black finish and subtle indigo metallic details.',
                'price': 349.00,
                'stock': 20,
                'category': 'Audio',
                'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuAQG0rmKccsHKgPGjsNKBz-FT9CC6XvPxfAkMDHs3KEMomwpEnXheWaz0kolZl9G5yifjKFPWHfBB4qa7LeOH9aP8F-0hkEgV5OjAZLS5mRjvqT887PCSBfYOgdNq9Npqz8tEpl5x9hN7-1ZHVOjGdsLOIDzqdZh3bfcaapO5KfJZ-Jqg1kXW7tyAMCMydmtbLOZ8o45lbAZ28F7C9AP0QeBfqLzMHuiz3GovQOe-XGEhQbQ1xw3j5vT5MQ4LPiqVlv5KiBsJ3CLcDX'
            },
            {
                'name': 'Vanguard Pro Smart',
                'description': 'A luxurious smartwatch with a dark titanium frame and a minimalist black OLED interface.',
                'price': 499.00,
                'stock': 8,
                'category': 'Tech',
                'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuBrxrg2BEsx7EWAYVcihXJqENm_sKDsbFMXK5-uDP9rV1YIn3QWFQnl-jpfjyDh7rItwIXzRtJgBg3PPiPWDN19LxbEBUyVOjl8dZTTvehJsIekYAlMDnu7hyLOqcFBLYXNm6HoCa8NUY0GdEOQrPkAANIjKaIlRV0BSdky5qbQ0tSD_rWqq7Jhsj75-gkbYK3P76r_uEWTjGDEADqC5hyI3h8UtEf_CyaCXqhjFICd3V236eoo9u_HU3rM3WEbQGuyTn1NcICX01et'
            },
            {
                'name': 'Eclipse Shade 400',
                'description': 'Designer matte black sunglasses with dark polarized lenses, showcased in a minimalist architectural setting.',
                'price': 185.00,
                'stock': 12,
                'category': 'Fashion',
                'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuAvHjCZwlv-wh-yG4b48iAkJcto4zT6yaYd9NBwFfeFykKcG9uDRRN7JjTF3CLYttey4dsyHSVOeoN1Zw-6nhCKN9xNqdCwM-rZEMEwk5DCDoUbObBa8VYOXGHztSZKCvTMWwd5t_ZIOxfAzdolwff_GTw4BU8bkRdpDB_mmKAsxHbXPGfWaQ-dvnzBq3N0g9EILCVWtg9lEmFvpvqwtZZDKQVWTuWht3xGXsilpgQ7IkAvcbxpbRgvqS0mhAxbdMNwFWdMVMTr7vAT'
            },
            {
                'name': 'Bio-Shield First Aid Kit',
                'description': 'A premium clinical emergency kit packed with essential medical supplies, sterile bandages, and antiseptics in a robust utility case.',
                'price': 45.00,
                'stock': 30,
                'category': 'Pharmacy',
                'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuAQG0rmKccsHKgPGjsNKBz-FT9CC6XvPxfAkMDHs3KEMomwpEnXheWaz0kolZl9G5yifjKFPWHfBB4qa7LeOH9aP8F-0hkEgV5OjAZLS5mRjvqT887PCSBfYOgdNq9Npqz8tEpl5x9hN7-1ZHVOjGdsLOIDzqdZh3bfcaapO5KfJZ-Jqg1kXW7tyAMCMydmtbLOZ8o45lbAZ28F7C9AP0QeBfqLzMHuiz3GovQOe-XGEhQbQ1xw3j5vT5MQ4LPiqVlv5KiBsJ3CLcDX'
            },
            {
                'name': 'Pulse-Check Oximeter',
                'description': 'High-precision dark titanium digital fingertip oxygen monitor with an active dark OLED screen displaying realtime telemetry.',
                'price': 55.00,
                'stock': 25,
                'category': 'Pharmacy',
                'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuBrxrg2BEsx7EWAYVcihXJqENm_sKDsbFMXK5-uDP9rV1YIn3QWFQnl-jpfjyDh7rItwIXzRtJgBg3PPiPWDN19LxbEBUyVOjl8dZTTvehJsIekYAlMDnu7hyLOqcFBLYXNm6HoCa8NUY0GdEOQrPkAANIjKaIlRV0BSdky5qbQ0tSD_rWqq7Jhsj75-gkbYK3P76r_uEWTjGDEADqC5hyI3h8UtEf_CyaCXqhjFICd3V236eoo9u_HU3rM3WEbQGuyTn1NcICX01et'
            },
            {
                'name': 'Aura Multi-Vitamins',
                'description': 'A bottle of daily organic health supplements and active minerals for optimal physical vitality and immune system fortification.',
                'price': 29.00,
                'stock': 50,
                'category': 'Pharmacy',
                'image_url': 'https://lh3.googleusercontent.com/aida-public/AB6AXuA-RM_AA_-yCKMjrkjPWujto6m0nTXtu5ROoAJ5GnibIw_m3KweU1daoZILogmKop5awrlCM_-ORVkQWz4RdbWBf1ziQPmLagaFzDFMoyNW6TtDnQj2Y0V8xGP0L96BHGJN9vY1EgeRkTono6Q_opgyx01TWb_d1-dmqNXd14xP83S8GcFp3gAcb34XaO-bgz9aUcOeFOKGcRslOlCWCTUnsvIjBeIWliuxvZITcGVO888MhB5X2NVWTQQAeGKry3S0-cVo5hxoCNAN'
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
