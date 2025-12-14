from app.logger import setup_logging, logger
from app.services.db_service import get_db
from app.services.message_broker import get_message_broker
import asyncio

async def main():
    setup_logging()
    msg_broker = get_message_broker()
    db = get_db()
    await db.connect()
    logger.info("Database Connected")
    try:
        await msg_broker.start_consuming()
    except asyncio.CancelledError:
        pass
    finally:
        await db.disconnect()
        await msg_broker.close()