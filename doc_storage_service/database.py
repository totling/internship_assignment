from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket

from config import settings


client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.MONGO_DATABASE]

fs_bucket = AsyncIOMotorGridFSBucket(db)

metadata_collection = db['file_metadata']


async def save_file_to_gridfs(file_data: bytes, file_name: str):
    file_id = await fs_bucket.upload_from_stream(file_name, file_data)
    return file_id


async def save_file_metadata(user_id: int, file_id, file_name: str):
    metadata = {
        "user_id": user_id,
        "file_id": file_id,
        "file_name": file_name,
        "upload_date": datetime.utcnow()
    }
    await metadata_collection.insert_one(metadata)


async def get_file_from_gridfs(file_id):
    grid_out = await fs_bucket.open_download_stream(file_id)
    file_data = await grid_out.read()
    return file_data
