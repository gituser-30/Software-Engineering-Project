from pymongo import MongoClient

client = MongoClient("Your Mongodb url")
db = client["user_db"]
users = db["users"]
