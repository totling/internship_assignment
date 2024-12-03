import uvicorn
from fastapi import FastAPI
from aiokafka import AIOKafkaProducer
from bson import ObjectId
import json

from user_service.config import settings
from user_service.users.router import router_auth, router_admin_manage

app = FastAPI()

app.include_router(router_auth, prefix="/public")
app.include_router(router_admin_manage, prefix="/protected")


producer = None


@app.on_event("startup")
async def startup():
    global producer
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_SERVER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    await producer.start()


@app.on_event("shutdown")
async def shutdown_event():
    global producer
    await producer.stop()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
