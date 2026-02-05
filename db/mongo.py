from pymongo import MongoClient

# Local MongoDB connection
client = MongoClient("mongodb://localhost:27017")

db = client["lab_monitoring_db"]

labs_col = db["labs"]
systems_col = db["systems"]
staff_col = db["staff"]
