from fastapi import FastAPI
import uvicorn
import asyncio
from .managers.socket_manager import init_socket
from .services import init_db, init_broker
from .logger import logger, setup_logging

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()

    broker = init_broker() 
    consumer_task = asyncio.create_task(broker.start_consuming())
    
    logger.info("Startup complete")
    
    yield
    
    logger.info("Shutdown initiated...")
    
    await broker.close()
    
    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        pass
        
    logger.info("Shutdown complete")


def create_app() -> FastAPI:
    """Function to create the FastAPI application"""
    app = FastAPI(lifespan=lifespan)
    init_socket(app=app)
    # Add cors

    # Add other routers

    # return app
    return app

if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=4002)