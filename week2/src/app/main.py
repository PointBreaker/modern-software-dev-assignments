from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional
import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from .db import init_db
from .routers import action_items, notes
from . import db

# 简单配置
class Config:
    def __init__(self):
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

config = Config()

# 初始化数据库
init_db()

app = FastAPI(
    title="Action Item Extractor",
    debug=config.debug
)

# 简单的日志配置
import logging
logging.basicConfig(level=getattr(logging, config.log_level))
logger = logging.getLogger(__name__)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全局异常处理器"""
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc) if config.debug else None
        }
    )


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    html_path = Path(__file__).resolve().parents[1] / "frontend" / "index.html"
    return html_path.read_text(encoding="utf-8")


# 简单的健康检查
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "action-item-extractor"}


app.include_router(notes.router)
app.include_router(action_items.router)


static_dir = Path(__file__).resolve().parents[1] / "frontend"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")