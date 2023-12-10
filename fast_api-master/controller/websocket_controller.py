from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect
from model.websocket_model import WebSocketModel
from datetime import datetime
import json

router = APIRouter()
manager = WebSocketModel()


@router.websocket("/ws/{contact_id}")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(data)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        message = {"time": current_time, "message": "Offline"}
        await manager.broadcast(json.dumps(message))
