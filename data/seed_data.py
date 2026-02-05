import json
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.mongo import labs_col, systems_col

def load_json(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), 'r') as f:
        return json.load(f)

def seed_data():
    # 1. Seed Labs
    labs_data = load_json('seed_labs.json')
    print(f"Found {len(labs_data)} labs in seed file.")
    
    # Clear existing labs (optional, but good for reset)
    labs_col.delete_many({})
    
    if labs_data:
        labs_col.insert_many(labs_data)
        print("Labs seeded successfully.")

    # 2. Seed Systems
    systems_data = load_json('seed_systems.json')
    print(f"Found {len(systems_data)} systems in seed file.")
    
    # Clear existing systems
    systems_col.delete_many({})
    
    if systems_data:
        systems_col.insert_many(systems_data)
        print("Systems seeded successfully.")

if __name__ == "__main__":
    seed_data()
