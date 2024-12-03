from motor.motor_asyncio import AsyncIOMotorClient
from aiokafka import AIOKafkaConsumer
import json
import base64
from bson import ObjectId
from gridfs import GridFSBucket
from doc_storage_service.config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.MONGO_DATABASE]
grid_fs_bucket = GridFSBucket(db)