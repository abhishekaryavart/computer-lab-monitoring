from pymongo import MongoClient
import random

client = MongoClient("mongodb://localhost:27017/")
db = client["lab_monitor_db_2"]
systems_col = db["systems"]
labs_col = db["labs"]

# Helper to generate systems
def generate_systems(lab_id, tables, config_options):
    systems = []
    
    for table_def in tables:
        table_name = table_def["name"]
        start_num = table_def["start"]
        count = table_def["count"]
        
        for i in range(1, count + 1):
            pc_num = f"{start_num}{i:02d}" # e.g. L101, B101
            
            # Random status
            r = random.random()
            if r < 0.6:
                status = "ON"
                user = random.choice(["Student", "Faculty", "Exam User", "Project Team"])
                purpose = random.choice(["Coding", "Research", "Exam", "Browsing"])
            elif r < 0.9:
                status = "OFF"
                user = "Available"
                purpose = None
            else:
                status = "DEAD"
                user = "Maintenance"
                purpose = "Hardware Issue"
                
            system = {
                "_id": f"{lab_id}_{pc_num}",
                "lab_id": lab_id,
                "table": table_name,
                "pc_name": pc_num,
                "position": i,
                "config": random.choice(config_options),
                "user": user,
                "status": status,
                "purpose": purpose
            }
            systems.append(system)
    return systems

def seed_full_data():
    print("Clearing existing systems...")
    systems_col.delete_many({})
    
    # --- MCA LAB (Classic Layout) ---
    print("Seeding MCA Lab...")
    mca_tables = [
        {"name": "L1", "start": "L1", "count": 5},
        {"name": "L2", "start": "L2", "count": 5},
        {"name": "L3", "start": "L3", "count": 10},
        {"name": "L4", "start": "L4", "count": 10},
        {"name": "L5", "start": "L5", "count": 10}
    ]
    mca_systems = generate_systems("MCA_LAB", mca_tables, ["Ryzen 7, 32GB", "i7 12th Gen, 16GB"])
    systems_col.insert_many(mca_systems)
    
    # --- BCA LAB (4 Large Rows) ---
    print("Seeding BCA Lab...")
    bca_tables = [
        {"name": "B1", "start": "B1", "count": 10},
        {"name": "B2", "start": "B2", "count": 10},
        {"name": "B3", "start": "B3", "count": 10},
        {"name": "B4", "start": "B4", "count": 10}
    ]
    bca_systems = generate_systems("BCA_LAB", bca_tables, ["i5 11th Gen, 16GB", "i5 10th Gen, 8GB"])
    systems_col.insert_many(bca_systems)
    
    # --- BIT LAB (High Density) ---
    print("Seeding BIT Lab...")
    bit_tables = [
        {"name": "T1", "start": "T1", "count": 10},
        {"name": "T2", "start": "T2", "count": 10},
        {"name": "T3", "start": "T3", "count": 10},
        {"name": "T4", "start": "T4", "count": 10},
        {"name": "T5", "start": "T5", "count": 10},
        {"name": "T6", "start": "T6", "count": 10}
    ]
    bit_systems = generate_systems("BIT_LAB", bit_tables, ["i3 12th Gen, 8GB", "Ryzen 3, 8GB"])
    systems_col.insert_many(bit_systems)
    
    # Update Stats
    print("Updating Lab Stats...")
    for lab_id in ["MCA_LAB", "BCA_LAB", "BIT_LAB"]:
        total = systems_col.count_documents({"lab_id": lab_id})
        running = systems_col.count_documents({"lab_id": lab_id, "status": "ON"})
        dead = systems_col.count_documents({"lab_id": lab_id, "status": "DEAD"})
        available = systems_col.count_documents({"lab_id": lab_id, "status": "OFF"})
        
        labs_col.update_one(
            {"_id": lab_id},
            {"$set": {"total": total, "running": running, "dead": dead, "available": available}}
        )
        
    print("Seeding Complete!")

if __name__ == "__main__":
    seed_full_data()
