from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    mongodb_uri: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    db_name: str = os.getenv("DB_NAME", "episense")


settings = Settings()

client: AsyncIOMotorClient = None  # type: ignore


async def connect_db():
    global client
    client = AsyncIOMotorClient(settings.mongodb_uri, serverSelectionTimeoutMS=3000)
    try:
        await client.admin.command("ping")
        print(f"✅ Connected to MongoDB — DB: {settings.db_name}")
    except Exception as e:
        print(f"⚠️  MongoDB not reachable ({e}). Engine endpoints will still work (dummy data).")
        print(f"   Only /projects CRUD needs MongoDB. Start mongod or set MONGODB_URI to fix.")


async def close_db():
    global client
    if client:
        client.close()
        print("🔌 MongoDB connection closed.")


def get_database():
    return client[settings.db_name]
