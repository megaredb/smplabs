import datetime
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict

ws_router = APIRouter()

class ConnectionManager:
    def __init__(self):
        # Зберігаємо підключення для нотифікацій
        self.notification_connections: List[WebSocket] = []
        # Зберігаємо підключення для чатів (імітація кімнат за campaign_id)
        self.chat_connections: Dict[str, Dict[str, WebSocket]] = {}

    # --- Нотифікації ---
    async def connect_notification(self, websocket: WebSocket):
        await websocket.accept()
        self.notification_connections.append(websocket)

    def disconnect_notification(self, websocket: WebSocket):
        if websocket in self.notification_connections:
            self.notification_connections.remove(websocket)

    async def broadcast_new_campaign(self, message: str):
        for connection in self.notification_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass

    # --- Чат ---
    async def connect_chat(self, websocket: WebSocket, campaign_id: str, user_id: str):
        await websocket.accept()
        if campaign_id not in self.chat_connections:
            self.chat_connections[campaign_id] = {}
        self.chat_connections[campaign_id][user_id] = websocket

    def disconnect_chat(self, campaign_id: str, user_id: str):
        if campaign_id in self.chat_connections and user_id in self.chat_connections[campaign_id]:
            del self.chat_connections[campaign_id][user_id]


manager = ConnectionManager()

@ws_router.websocket("/ws/notifications")
async def websocket_notifications(websocket: WebSocket):
    await manager.connect_notification(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Можна розсилати повідомлення всім при отриманні
            await manager.broadcast_new_campaign(data)
    except WebSocketDisconnect:
        manager.disconnect_notification(websocket)

@ws_router.websocket("/ws/chat/{campaign_id}/{user_id}")
async def websocket_chat(websocket: WebSocket, campaign_id: str, user_id: str):
    await manager.connect_chat(websocket, campaign_id, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Тет-а-тет логіка: очікуємо формат "target_user_id:текст_повідомлення"
            if ":" in data:
                target_id, msg = data.split(":", 1)
                target_id = target_id.strip()
                msg = msg.strip()
                
                # Відправляємо повідомлення конкретному учаснику (target_id)
                if campaign_id in manager.chat_connections and target_id in manager.chat_connections[campaign_id]:
                    target_ws = manager.chat_connections[campaign_id][target_id]
                    try:
                        await target_ws.send_text(f"[{timestamp}] {user_id}: {msg}")
                    except Exception:
                        pass
                    # Відправляємо копію собі, щоб бачити історію
                    await websocket.send_text(f"[{timestamp}] Ви (до {target_id}): {msg}")
                else:
                    # Якщо користувача немає в мережі
                    await websocket.send_text(f"[{timestamp}] Система: Користувач {target_id} не в мережі.")
            else:
                await websocket.send_text(f"[{timestamp}] Система: Неправильний формат. Використовуйте 'id_одержувача: повідомлення'")
            
    except WebSocketDisconnect:
        manager.disconnect_chat(campaign_id, user_id)
