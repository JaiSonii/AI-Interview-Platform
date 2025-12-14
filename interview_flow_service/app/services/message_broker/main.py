import aio_pika
from typing import Optional
import asyncio
import json
import httpx

from ..resume_parser import get_resume_parser_service
from ..db_service import get_db
from ..job_question import get_job_question_service

from app.config import settings
from app.logger import logger
from app.services.interview_flow import get_interview_flow_service

class MessageBroker:
    def __init__(self):
        self._user = settings.RABBITMQ_USER
        self._password = settings.RABBITMQ_PASSWORD
        self._host = settings.RABBITMQ_HOST
        self._port = settings.RABBITMQ_PORT
        self.interview_flow_service = get_interview_flow_service()
        self.resume_parser = get_resume_parser_service()
        self._job_question_service = get_job_question_service()
        self.db = get_db()
        self._httpx_client = httpx.AsyncClient(timeout=30)

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

        if self._httpx_client:
            await self._httpx_client.aclose()
        
        if self._connection:
            await self._connection.close()
            
        await self.db.disconnect()

    async def _process_message(self, message: aio_pika.abc.AbstractIncomingMessage):
        async with message.process():
            try:
                payload = json.loads(message.body)
                routing_key = message.routing_key
                if routing_key == 'flow.create':
                    await self._handle_interview_flow_creation(payload)
                elif routing_key == 'job.question.create':
                    await self._handle_job_question_creation(payload)
                else:
                    raise KeyError(f"Invalid routing Key {routing_key}")
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
            "interview.flow.create": "flow.create",
            "interview.job.question": "job.question.create"
        }
        self._queue_list = await self._setup_queues('consume', queues=queue_config)
        self._consumer_tags = [await queue.consume(self._process_message) for queue in self._queue_list]
        logger.info(f"Queue Consume started for {len(self._queue_list)} queues")
        await asyncio.Future()

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

    async def _fetch_resume_data(self, url: str) -> bytes:
        """
        Fetch resume data from the S3 URL
        """
        response = await self._httpx_client.get(url)
        response.raise_for_status()
        return response.content
        

    async def _handle_interview_flow_creation(self,payload: dict):
        resume_s3_url = payload.get("resume_url", None)
        application_id = payload.get("application_id", None)
        session_id = payload.get("session_id", None)

        if not resume_s3_url:
            raise ValueError("Resume S3 URL is required in the payload")
        if not application_id:
            raise ValueError("Application Id is required in the payload")
        if not session_id:
            raise ValueError("Session Id not provided")
        
        application = await self.db.get_application_by_id(application_id)

        if application is None or application.job is None:
            raise ValueError("Application info not found for the given application ID")
        
        resume_data = await self._fetch_resume_data(resume_s3_url)
        parsed_resume = await self.resume_parser.invoke(bytes_data=resume_data)
        
        interview_flow_data = await get_interview_flow_service().invoke(
            job_info=application.job.model_dump(),
            candidate_info = parsed_resume.model_dump()
        )
        await self.db.save_interview_flow(application_id, interview_flow_data.model_dump())
        if session_id:
            await self.send_message('interview.exchange', 'flow.ready', {
                "application_id": application_id,
                "session_id": session_id,
                "status": "READY"
            })

    async def _handle_job_question_creation(self, payload: dict):
        job_id = payload.get('job_id', None)
        if job_id is None:
            raise ValueError("Job Id not provided")
        
        job = await self.db.get_job_by_id(job_id)
        if not job:
            raise ValueError(f"Job not found with id: {job_id}")
        
        job_dict = job.model_dump()

        ai_payload = {
            "job_id" : job_id,
            "role" : job_dict.get('role', None),
            "exp_range" : job_dict.get('exp_range', None),
            "description" : job_dict.get('description', None)
        }

        job_questions = await self._job_question_service.invoke(**ai_payload)
        await self.db.save_job_questions(job_id, job_questions.model_dump())



if __name__ == "__main__":
    import asyncio

    async def main():
        broker = MessageBroker()

        print("🚀 Starting MessageBroker consumer...")
        await broker.start_consuming()

        # Keep the process alive forever
        print("🟢 Consumer is running. Press Ctrl+C to stop.")
        while True:
            await asyncio.sleep(60)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Consumer stopped by user")
