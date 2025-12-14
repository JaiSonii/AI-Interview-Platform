import asyncio
import aio_pika
import json
import uuid

AMQP_URL = "amqp://user:password@localhost:5672/"

async def main():
    connection = await aio_pika.connect_robust(AMQP_URL)
    channel = await connection.channel()

    exchange = await channel.declare_exchange(
        "interview.exchange",
        aio_pika.ExchangeType.DIRECT,
        durable=True
    )

    payload = {
        "session_id": str(uuid.uuid4()),
        "candidate_id": "candidate-123",
        "resume_url": "s3://fake-bucket/resume.pdf"
    }

    message = aio_pika.Message(
        body=json.dumps(payload).encode(),
        delivery_mode=aio_pika.DeliveryMode.PERSISTENT
    )

    await exchange.publish(message, routing_key="flow.create")

    print("🚀 Published job:", payload)

    await connection.close()

async def connect_test():
    from prisma import Prisma
    db = Prisma()
    await db.connect()
    print("DB Connected")
    await db.disconnect()

asyncio.run(connect_test())
