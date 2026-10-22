import os
import json
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from database.database import db_manager
from core.orchestrator import AutoAuditOrchestrator

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_manager.connect_db()
    yield
    db_manager.close_db()

app = FastAPI(
    title="AutoAudit AI Pro API",
    description="Backend for Autonomous Multi-Agent Website Auditor",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AutoAudit AI Backend is running! 🚀"}

# --- Live WebSocket Route ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print("Frontend UI Connected via WebSocket!")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print("Frontend UI Disconnected.")

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"WebSocket Error: {e}")

manager = ConnectionManager()

@app.websocket("/ws/audit-logs")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
                if payload.get("action") == "START_SCAN":
                    target_url = payload.get("url")
                    if not target_url:
                        await manager.broadcast({"agent": "System", "status": "error", "message": "URL not provided!"})
                        continue
                        
                    orchestrator = AutoAuditOrchestrator(target_url, manager)
                    asyncio.create_task(orchestrator.run_audit())
            except json.JSONDecodeError:
                await manager.broadcast({"agent": "System", "status": "error", "message": "Invalid command format."})
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# --- Download Report API ---
@app.get("/download-report/{filename}")
async def download_report(filename: str):
    file_path = os.path.join(os.getcwd(), "outputs", filename)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename, media_type='text/markdown')
    return {"error": "Report not found."}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)