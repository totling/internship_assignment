import asyncio
import uvicorn
from fastapi import FastAPI
from doc_storage_service.kafka import init_kafka, close_kafka

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await init_kafka()


@app.on_event("shutdown")
async def shutdown_event():
    await close_kafka()


@app.get("/")
async def root():
    return {"message": "File storage microservice is running"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.2", port=8001, reload=True)
