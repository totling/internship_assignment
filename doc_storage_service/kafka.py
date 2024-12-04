from aiokafka import AIOKafkaConsumer
from file_service import handle_file
from config import settings

import json


consumer = None


async def start_kafka_consumer():
    global consumer
    consumer = AIOKafkaConsumer(
        settings.TOPIC_NAME,
        bootstrap_servers=settings.KAFKA_SERVER,
        group_id=settings.KAFKA_GROUP_ID
    )
    await consumer.start()

    async for msg in consumer:
        message_str = msg.value.decode('utf-8')
        message = json.loads(message_str)
        await handle_file(message)


async def stop_kafka_consumer():
    if consumer:
        await consumer.stop()
