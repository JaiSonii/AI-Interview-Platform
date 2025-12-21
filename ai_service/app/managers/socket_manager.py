import socketio
from ..logger import logger
from fastapi import FastAPI
from typing import Any, Optional

class SocketManager:
    def __init__(self, app : FastAPI) -> None:
        self.sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode = "asgi")
        self.socket_app = socketio.ASGIApp(self.sio)
        app.mount("/ws", self.socket_app)
        logger.debug('Socket mounted on /ws')
        self._register_events()
        logger.debug("Socket Events registered")

    def _register_events(self):
        @self.sio.event
        async def connect(sid, env):
            logger.info(f"Client Connected SID : {sid}")

        @self.sio.event
        async def disconnect(sid):
            logger.info(f"Client disconnected SID : {sid}")

    async def emit(self, event: str, message : Any, room = None):
        await self.sio.emit(event=event, data=message, room=room)

socket_manager: Optional[SocketManager] = None

def init_socket(app: FastAPI):
    """
    Create the singleton instance IF NOT ALREADY CREATED.
    """
    global socket_manager
    if socket_manager is None:
        socket_manager = SocketManager(app)
    return socket_manager

