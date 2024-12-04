from aiokafka import AIOKafkaProducer
import json
import asyncio
from config import settings

producer = None
producer_ready = asyncio.Event()


async def start_producer():
    global producer
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_SERVER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        compression_type="gzip",
    )
    await producer.start()
    producer_ready.set()


async def stop_producer():
    global producer
    if producer:
        await producer.stop()
    else:
        raise RuntimeError("Producer is not initialized yet")


async def get_producer():
    await producer_ready.wait()
    return producer
