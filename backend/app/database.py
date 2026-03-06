from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    mongodb_uri: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    db_name: str = os.getenv("DB_NAME", "episense")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()

client: AsyncIOMotorClient = None  # type: ignore
is_connected = False


async def connect_db():
    global client, is_connected
    if "<user>:<pass>" in settings.mongodb_uri:
        is_connected = False
        print("⚠️  Dummy MongoDB URI detected. Save to Dashboard disabled. Update .env to fix.")
        return

    client = AsyncIOMotorClient(settings.mongodb_uri, serverSelectionTimeoutMS=3000)
    try:
        await client.admin.command("ping")
        is_connected = True
        print(f"✅ Connected to MongoDB — DB: {settings.db_name}")
    except Exception as e:
        is_connected = False
        print(f"⚠️  MongoDB not reachable ({e}). Engine endpoints will still work (dummy data).")
        print(f"   Only /projects CRUD needs MongoDB. Start mongod or set MONGODB_URI to fix.")


async def close_db():
    global client, is_connected
    if client:
        client.close()
        is_connected = False
        print("🔌 MongoDB connection closed.")


def get_database():
    if not is_connected or client is None:
        raise HTTPException(
            status_code=503,
            detail="Database service unavailable. Please check MongoDB connection."
        )
    return client[settings.db_name]
