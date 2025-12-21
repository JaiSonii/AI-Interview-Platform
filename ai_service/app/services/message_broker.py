import aio_pika
from typing import Optional
import json

from app.config import settings
from app.logger import logger
from app.managers.socket_manager import socket_manager

class MessageBroker:
    def __init__(self):
        self._user = settings.RABBITMQ_USER
        self._password = settings.RABBITMQ_PASSWORD
        self._host = settings.RABBITMQ_HOST
        self._port = settings.RABBITMQ_PORT

        self._broker_url = (
            f"amqp://{self._user}:{self._password}"
            f"@{self._host}:{self._port}/"
        )

        self._channels: dict[str, Optional[aio_pika.abc.AbstractChannel]] = {
            "publish": None,
            "consume": None
        }

        self._connection = None
        self._queue_list: list[aio_pika.abc.AbstractQueue] = []
        self._consumer_tags: list[str] = []

    async def _connect(self):
        self._connection = await aio_pika.connect_robust(self._broker_url)

        self._channels["publish"] = await self._connection.channel()
        self._channels["consume"] = await self._connection.channel()

        await self._channels["consume"].set_qos(prefetch_count=5)

    async def close(self):
        """Gracefull Shutdown"""
        logger.info("Shutting Down Message Broker")

        if self._queue_list and self._consumer_tags:
            for queue, consumer_tag in zip(self._queue_list, self._consumer_tags):
                await queue.cancel(consumer_tag)
        
        if self._connection:
            await self._connection.close()
            
    async def _process_message(self, message: aio_pika.abc.AbstractIncomingMessage):
        async with message.process():
            try:
                payload = json.loads(message.body)
                routing_key = message.routing_key
                if routing_key == "flow.ready":
                    session_id = payload.get('session_id')
                    logger.info(f"Inteview Flow Ready for id {session_id}")
                    assert socket_manager is not None
                    await socket_manager.emit('flow.ready', payload, room=session_id)
                    
            except Exception as e:
                logger.error(f"Error in processing message : {e}")

    async def _setup_queues(self, channel_name: str,  queues: dict[str, str])->list[aio_pika.abc.AbstractQueue]:
        if self._channels[channel_name] is None or self._channels[channel_name].is_closed: #type: ignore
            await self._connect()

        channel = self._channels[channel_name]
        assert channel is not None

        exchange = await channel.declare_exchange(
            name="interview.exchange",
            type=aio_pika.ExchangeType.DIRECT,
            durable=True
        )

        queue_list:list[aio_pika.abc.AbstractQueue] = []
        for k,v in queues.items():
            logger.info(f"Setting up Queue {k}, Routing Key: {v}")
            queue = await channel.declare_queue(
                name=k,
                durable=True
            )
            await queue.bind(exchange=exchange, routing_key=v)
            queue_list.append(queue)

        return queue_list
   

    async def start_consuming(self):
        """Start consuming messages from the interview flow creation queue"""
        queue_config = {
            "ai_service.flow_updates" : "flow.ready"
        }
        self._queue_list = await self._setup_queues('consume', queues=queue_config)
        self._consumer_tags = [await queue.consume(self._process_message) for queue in self._queue_list]
        logger.info(f"Queue Consume started for {len(self._queue_list)} queues")
        # await asyncio.Future()

    async def send_message(self, exchange_name: str, routing_key: str, messsage_body: dict):
        """
        Send message to the publisher queue
        Args:
            exchange_name : Name of the exchange in the RabbitMQ
            routing_key: The routing key of queue binding
            message_body: The actual messaege body to send 
        """
        if self._channels['publish'] is None or self._channels['publish'].is_closed:
            await self._connect()

        channel = self._channels['publish']
        assert channel is not None

        exchange = await channel.declare_exchange(
            name=exchange_name,
            type=aio_pika.ExchangeType.DIRECT,
            durable=True
        )

        message = aio_pika.Message(
            body=json.dumps(messsage_body).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )

        await exchange.publish(message=message, routing_key=routing_key)
        logger.info(f"Published Message: {message} to {routing_key}")

msg_broker: Optional[MessageBroker] = None

def init_broker()->MessageBroker:
    global msg_broker
    if msg_broker is None:
        msg_broker = MessageBroker()
    return msg_broker
