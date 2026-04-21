# Synthetic Stores Data Generator

Professional Python tool that generates synthetic retail store data with realistic randomized attributes. Output to JSON files or MongoDB.

## Quick Start

```bash
# 1. Setup virtual environment
python -m venv venv
venv\Scripts\activate                    # Windows
# source venv/bin/activate               # Linux/Mac

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate test data (no MongoDB needed)
python main.py count=5 output=json

# 4. View output
# Files saved to: output/stores_YYYYMMDD_HHMMSS.json
```

## Usage

### Generate JSON Files (No MongoDB Required)

```bash
# Test with 5 records
python main.py count=5 output=json

# Medium dataset (100 records)
python main.py count=100 output=json

# Large dataset (10,000 records)
python main.py count=10000 output=json

# Continuous generation (50 records per file every 2 seconds)
python main.py loop=true count=50 output=json
```

### Insert to MongoDB

```bash
# 1. Edit config.json with your connection string:
{
  "MongoConnectionString": "mongodb+srv://username:password@cluster.mongodb.net/",
  "mongoDBName": "sampledb",
  "mongoCollectionName": "stores"
}

# 2. Generate and insert
python main.py count=100                 # Insert 100 records
python main.py loop=true count=50        # Insert 50 records every 2 seconds
```

### Command Line Arguments

- `count=N` - Number of records to generate (default: 1)
- `output=json|mongodb` - Output destination (default: mongodb)
- `loop=true|false` - Continuous generation mode (default: false)

## Project Structure

```
SyntheticStoresPy/
├── main.py                    # Single-file implementation
├── config.json                # MongoDB connection settings
├── requirements.txt           # Python dependencies
├── data/                      # Metadata files (legally approved content)
│   ├── metadata.json          # Company names, store types, promotions
│   └── ProductCategories.json # Product categories and items
├── output/                    # Generated JSON files
└── venv/                      # Virtual environment
```

## Data Structure

Each store record contains:

```json
{
  "id": "uuid",
  "name": "Company | Category Type - City",
  "location": {"lat": 0.0, "lon": 0.0},
  "staff": {
    "totalStaff": {"fullTime": 10, "partTime": 5}
  },
  "sales": {
    "totalSales": 50000,
    "salesByCategory": [
      {"categoryName": "Product", "totalSales": 25000}
    ]
  },
  "promotionEvents": [
    {
      "eventName": "Sale Event",
      "promotionalDates": {"startDate": "2026-01-01", "endDate": "2026-01-10"},
      "discounts": [
        {"categoryName": "Product", "discountPercentage": 15}
      ]
    }
  ]
}
```

## File Sizes (Approximate)

- 5 records: ~15 KB
- 50 records: ~110 KB
- 100 records: ~220 KB
- 1,000 records: ~2.2 MB
- 10,000 records: ~22 MB

## Examples

```bash
# Quick test
python main.py count=10 output=json

# Generate large dataset for testing
python main.py count=10000 output=json

# Insert to MongoDB
python main.py count=1000 output=mongodb

# Continuous data generation for load testing
python main.py loop=true count=100 output=json
```

## Troubleshooting

**Import errors:**
```bash
pip install --upgrade -r requirements.txt
```

**MongoDB connection issues:**
- Verify connection string in config.json
- Check network access (whitelist IP for cloud databases)
- Test with MongoDB Compass

**File not found errors:**
- Run from the SyntheticStoresPy directory
- Ensure data/ folder contains metadata.json and ProductCategories.json

Generate and insert a single store record:

```bash
python main.py
```

### Multiple Records (One-Time)

Generate and insert multiple records at once:

```bash
python main.py count=100
```

### Loop Mode

Generate records continuously (every 2 seconds):

```bash
python main.py loop=true count=30
```

Press `Ctrl+C` to stop the loop.

### Combined Arguments

```bash
python main.py loop=true count=50
```

## Command Line Arguments

- `count=N` - Number of records to generate per run (default: 30)
- `loop=true|false` - Run continuously or once (default: false)

## Data Model

Each store record contains:

```json
{
  "id": "unique-guid",
  "name": "Company Name | Category Type - City",
  "location": {
    "lat": 40.7128,
    "lon": -74.0060
  },
  "staff": {
    "totalStaff": {
      "fullTime": 15,
      "partTime": 8
    }
  },
  "sales": {
    "totalSales": 125000,
    "salesByCategory": [
      {
        "categoryName": "Smartphones",
        "totalSales": 45000
      }
    ]
  },
  "promotionEvents": [
    {
      "eventName": "Mega Savings Extravaganza",
      "promotionalDates": {
        "startDate": "2024-01-15",
        "endDate": "2024-01-25"
      },
      "discounts": [
        {
          "categoryName": "Laptops",
          "discountPercentage": 15
        }
      ]
    }
  ]
}
```

## Requirements

- Python 3.8+
- faker 24.0.0
- pymongo 4.6.2
- python-dotenv 1.0.1
- MongoDB instance (optional - only for MongoDB output)
