import asyncio
import uvicorn
from fastapi import FastAPI
from kafka import start_kafka_consumer, stop_kafka_consumer

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_running_loop()
    app.state.kafka_consumer_task = loop.create_task(start_kafka_consumer())


@app.on_event("shutdown")
async def shutdown_event():
    if app.state.kafka_consumer_task:
        await stop_kafka_consumer()
        app.state.kafka_consumer_task.cancel()


@app.get("/")
async def root():
    return {"message": "File storage microservice is running"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.2", port=8001, reload=True)
