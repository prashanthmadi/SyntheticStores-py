#!/usr/bin/env python3
"""
Synthetic Store Data Generator
Generates realistic synthetic store records and inserts them into MongoDB or saves to JSON files

Usage:
    python main.py                              # Generate 1 record to MongoDB
    python main.py count=100                    # Generate 100 records to MongoDB
    python main.py count=100 output=json        # Generate 100 records to JSON file
    python main.py loop=true count=50           # Generate 50 records continuously to MongoDB
    python main.py loop=true count=50 output=json  # Generate 50 records continuously to JSON files
"""
import sys
import json
import random
import uuid
import time
from datetime import datetime, timedelta
from faker import Faker
from pymongo import MongoClient


def load_config(config_path="config.json"):
    """Load MongoDB configuration"""
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_data_files():
    """Load all metadata files"""
    with open("data/ProductCategories.json", "r", encoding="utf-8") as f:
        categories = json.load(f)["shop_categories"]
    
    with open("data/metadata.json", "r", encoding="utf-8") as f:
        metadata = json.load(f)
        shop_names = metadata["company_names"]
        shop_types = metadata["store_types"]
        promotions = metadata["promotions"]
    
    return categories, shop_names, shop_types, promotions


def generate_store(faker, category, shop_names, shop_types, promotions):
    """Generate a single store record"""
    
    # Basic store info
    store = {
        "id": str(uuid.uuid4()),
        "name": f"{random.choice(shop_names)} | {category['category']} {random.choice(shop_types)} - {faker.city()}",
        "location": {
            "lat": float(faker.latitude()),
            "lon": float(faker.longitude())
        },
        "staff": {
            "totalStaff": {
                "fullTime": random.randint(1, 20),
                "partTime": random.randint(0, 20)
            }
        },
        "sales": {
            "totalSales": 0,
            "salesByCategory": []
        },
        "promotionEvents": []
    }
    
    # Generate sales by category
    products = category['products']
    sales_count = random.randint(1, max(1, len(products) // 5))
    selected_products = random.sample(products, min(sales_count, len(products)))
    
    total_sales = 0
    for product in selected_products:
        category_sales = random.randint(100, 50000)
        store["sales"]["salesByCategory"].append({
            "categoryName": product,
            "totalSales": category_sales
        })
        total_sales += category_sales
    
    store["sales"]["totalSales"] = total_sales
    
    # Generate promotion events
    promo_count = random.randint(1, 6)
    selected_promos = random.sample(promotions, min(promo_count, len(promotions)))
    
    for i, promo_name in enumerate(selected_promos):
        start_date = datetime.now() - timedelta(days=90 * (promo_count - i))
        end_date = start_date + timedelta(days=random.randint(7, 10))
        
        # Generate discounts for this promotion
        discount_count = max(1, len(products) // 5)
        discount_products = random.sample(products, min(discount_count, len(products)))
        
        promo_event = {
            "eventName": promo_name,
            "promotionalDates": {
                "startDate": start_date.strftime('%Y-%m-%d'),
                "endDate": end_date.strftime('%Y-%m-%d')
            },
            "discounts": [
                {
                    "categoryName": prod,
                    "discountPercentage": random.randint(5, 25)
                }
                for prod in discount_products
            ]
        }
        store["promotionEvents"].append(promo_event)
    
    return store


def generate_stores(count, categories, shop_names, shop_types, promotions):
    """Generate multiple store records"""
    faker = Faker("en_US")
    stores = []
    
    for i in range(count):
        category = random.choice(categories)
        store = generate_store(faker, category, shop_names, shop_types, promotions)
        stores.append(store)
    
    return stores


def insert_to_mongodb(stores, config):
    """Insert stores into MongoDB"""
    try:
        client = MongoClient(config["MongoConnectionString"])
        db = client[config["mongoDBName"]]
        collection = db[config["mongoCollectionName"]]
        
        result = collection.insert_many(stores)
        print(f"✓ Inserted {len(result.inserted_ids)} records into MongoDB")
        
        client.close()
    except Exception as ex:
        print(f"✗ MongoDB Error: {ex}")


def save_to_json(stores, filename=None):
    """Save stores to JSON file"""
    try:
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"output/stores_{timestamp}.json"
        
        # Create output directory if it doesn't exist
        import os
        os.makedirs("output", exist_ok=True)
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(stores, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Saved {len(stores)} records to {filename}")
        return filename
    except Exception as ex:
        print(f"✗ File Error: {ex}")


def parse_args():
    """Parse command line arguments"""
    args = {'loop': False, 'count': 1, 'output': 'mongodb'}
    
    for arg in sys.argv[1:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            if key == 'loop':
                args['loop'] = value.lower() in ('true', '1', 'yes')
            elif key == 'count':
                args['count'] = int(value)
            elif key == 'output':
                args['output'] = value.lower()
    
    return args


def main():
    """Main entry point"""
    args = parse_args()
    
    # Load configuration and data
    categories, shop_names, shop_types, promotions = load_data_files()
    config = None
    
    # Only load MongoDB config if needed
    if args['output'] == 'mongodb':
        config = load_config()
    
    # Display mode
    output_target = "MongoDB" if args['output'] == 'mongodb' else "JSON files"
    if args['loop']:
        print(f"🔄 Loop mode: {args['count']} records per run to {output_target} (Ctrl+C to stop)")
    else:
        print(f"📝 Generating {args['count']} record(s) to {output_target}...")
    
    try:
        if args['loop']:
            # Continuous generation
            while True:
                stores = generate_stores(args['count'], categories, shop_names, shop_types, promotions)
                
                if args['output'] == 'json':
                    save_to_json(stores)
                else:
                    insert_to_mongodb(stores, config)
                
                time.sleep(2)
        else:
            # Single run
            stores = generate_stores(args['count'], categories, shop_names, shop_types, promotions)
            
            if args['output'] == 'json':
                save_to_json(stores)
            else:
                insert_to_mongodb(stores, config)
            
            print(f"✓ Done at {datetime.now().strftime('%H:%M:%S')}")
    
    except KeyboardInterrupt:
        print("\n⏹ Stopped")
    except Exception as ex:
        print(f"✗ Error: {ex}")


if __name__ == "__main__":
    main()
