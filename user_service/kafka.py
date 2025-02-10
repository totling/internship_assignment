from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import json
import asyncio
from user_service.config import settings

producer = None
consumer = None
producer_ready = asyncio.Event()
consumer_ready = asyncio.Event()


async def start_producer():
    global producer
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_SERVER,
        value_serializer=lambda v: json.dumps(v).encode('latin-1'),
        compression_type="gzip",
        max_request_size=104857600
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


async def start_consumer():
    global consumer
    consumer = AIOKafkaConsumer(
        settings.RESPONSE_TOPIC_NAME,
        bootstrap_servers=settings.KAFKA_SERVER,
        group_id=settings.KAFKA_GROUP_ID,
        value_deserializer=lambda v: json.loads(v.decode('latin-1')),
    )
    await consumer.start()
    consumer_ready.set()


async def stop_consumer():
    global consumer
    if consumer:
        await consumer.stop()
    else:
        raise RuntimeError("Consumer is not initialized yet")


async def get_consumer():
    await consumer_ready.wait()
    return consumer
