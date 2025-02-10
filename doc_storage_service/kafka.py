import asyncio
import json

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from doc_storage_service.file_service import upload_file, download_file
from doc_storage_service.config import settings


producer = None
consumer = None


async def init_kafka():
    global producer, consumer
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_SERVER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        compression_type="gzip",
    )
    consumer = AIOKafkaConsumer(
        settings.REQUEST_TOPIC_NAME,
        bootstrap_servers=settings.KAFKA_SERVER,
        group_id=settings.KAFKA_GROUP_ID,
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )

    await producer.start()
    await consumer.start()

    asyncio.create_task(consume_file_requests())


async def close_kafka():
    global producer, consumer
    await producer.stop()
    await consumer.stop()


async def consume_file_requests():
    global consumer, producer
    async for message in consumer:
        user_id = message.value["user_id"]
        file_name = message.value["filename"]
        file_data = message.value.get("file_content")

        if file_data:
            await upload_file(user_id, file_name, file_data)
        else:
            result = await download_file(user_id, file_name)

            result = result.decode('latin-1')

            message = {
                "filedata": result,
            }

            await producer.send_and_wait(settings.RESPONSE_TOPIC_NAME, message)


# async def start_kafka_consumer():
#     global consumer
#     consumer = AIOKafkaConsumer(
#         settings.TOPIC_NAME,
#         bootstrap_servers=settings.KAFKA_SERVER,
#         group_id=settings.KAFKA_GROUP_ID
#     )
#     await consumer.start()
#
#     async for msg in consumer:
#         message_str = msg.value.decode('utf-8')
#         message = json.loads(message_str)
#         await handle_file(message)
#
#
# async def stop_kafka_consumer():
#     if consumer:
#         await consumer.stop()
