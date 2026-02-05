import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.mongo import staff_col

def seed_staff():
    staff_users = [
        {
            "_id": "admin",
            "password": "admin123", # In production, use hashed passwords!
            "name": "System Administrator",
            "role": "admin"
        },
        {
            "_id": "staff01",
            "password": "password",
            "name": "Lab Assistant",
            "role": "staff"
        }
    ]

    print("Seeding staff users...")
    for user in staff_users:
        if staff_col.find_one({"_id": user["_id"]}):
            print(f"User {user['_id']} already exists. Skipping.")
        else:
            staff_col.insert_one(user)
            print(f"Created user: {user['_id']}")

    print("Staff seeding complete!")

if __name__ == "__main__":
    seed_staff()
