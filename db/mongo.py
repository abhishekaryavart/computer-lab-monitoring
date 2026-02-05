# from pymongo import MongoClient

# import os

# # MongoDB Connection
# # Use MONGO_URI from env if available (Atlas), else default to localhost
# MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
# client = MongoClient(MONGO_URI)

# db = client["lab_monitoring_db"]

# labs_col = db["labs"]
# systems_col = db["systems"]
# staff_col = db["staff"]






from pymongo import MongoClient
import os

MONGO_URI = os.environ.get("MONGO_URI")

if not MONGO_URI:
    raise Exception("MONGO_URI environment variable not set")

client = MongoClient(MONGO_URI)
db = client["lab_monitoring_db"]

labs_col = db["labs"]
systems_col = db["systems"]
