import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise EnvironmentError(
        "MONGO_URI is not set. Please add it to your .env file.\n"
        "Example:  MONGO_URI=mongodb+srv://<user>:<pass>@cluster.mongodb.net/"
    )

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")          
except ConnectionFailure as e:
    raise ConnectionFailure(
        f"Could not connect to MongoDB. Check your MONGO_URI.\nDetails: {e}"
    )

db                 = client["student_app"]
users_collection   = db["users"]
history_collection = db["history"]
