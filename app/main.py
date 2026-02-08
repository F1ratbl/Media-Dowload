import os
import uuid
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.services.history import HistoryManager
from app.services.downloader import download_worker, fetch_video_info, download_tasks
from typing import Optional
from app.database import engine, Base
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Statik Dosyalar (Logo, CSS vb.)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class URLRequest(BaseModel):
    url: str

class DownloadRequest(BaseModel):
    url: str
    type: str = "video"
    title: str
    thumbnail: str
    format_id: Optional[str] = None

# Endpoints
@app.get("/")
async def read_index():
    return FileResponse('templates/index.html')

@app.get("/history")
def get_history():
    return HistoryManager.load()

@app.post("/analyze")
def analyze_video(request: URLRequest):
    try:
        return fetch_video_info(request.url)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail="Video bulunamadı.")

@app.post("/start_download")
def start_download(request: DownloadRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    background_tasks.add_task(
        download_worker, 
        task_id, 
        request.url, 
        request.type, 
        request.title, 
        request.thumbnail,
        request.format_id
    )
    return {"task_id": task_id}

@app.get("/task_status/{task_id}")
def get_task_status(task_id: str):
    task = download_tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.get("/get_file/{task_id}")
def get_file(task_id: str):
    task = download_tasks.get(task_id)
    if not task or task["status"] != "completed":
        raise HTTPException(status_code=400, detail="File not ready")
    
    filepath = task["filepath"]
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File deleted or missing")

    return FileResponse(
        path=filepath, 
        filename=os.path.basename(filepath),
        media_type='application/octet-stream',
        headers={"Content-Disposition": f"attachment; filename={os.path.basename(filepath)}"}
    )