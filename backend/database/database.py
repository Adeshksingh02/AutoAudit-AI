import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGODB_URL")

class Database:
    client: AsyncIOMotorClient = None
    db = None

    @classmethod
    def connect_db(cls):
        """FastAPI startup par database connect karne ke liye"""
        if MONGO_URL and MONGO_URL != "your_mongodb_uri_here":
            cls.client = AsyncIOMotorClient(MONGO_URL)
            cls.db = cls.client.autoaudit_db
            print("🟢 Connected to MongoDB Database!")
        else:
            # Fallback for local testing if MongoDB URI is not set
            print("🟡 No MongoDB URI found. Running in local fallback mode (No persistence).")

    @classmethod
    def close_db(cls):
        """FastAPI shutdown par database connection close karne ke liye"""
        if cls.client:
            cls.client.close()
            print("🔴 MongoDB Connection Closed.")

    @classmethod
    def get_db(cls):
        """Dusri files me database instance use karne ke liye"""
        return cls.db

# Instance export kar rahe hain taaki agents isko import kar sakein
db_manager = Database()