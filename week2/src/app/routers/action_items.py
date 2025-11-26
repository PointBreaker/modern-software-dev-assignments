from __future__ import annotations

from typing import Any, Dict, List, Optional
import logging
import time

from fastapi import APIRouter, HTTPException

from .. import db
from ..services.extract import extract_action_items, extract_action_items_llm

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.post("/extract")
def extract(payload: Dict[str, Any]) -> Dict[str, Any]:
    """从文本中提取待办事项（基于规则）"""
    start_time = time.time()
    try:
        text = str(payload.get("text", "")).strip()
        if not text:
            raise HTTPException(status_code=400, detail="text is required")

        note_id: Optional[int] = None
        if payload.get("save_note"):
            note_id = db.insert_note(text)
            logger.info(f"Saved note with id: {note_id}")

        # 提取action items
        items = extract_action_items(text)

        # 批量插入数据库
        if items:
            ids = db.insert_action_items(items, note_id=note_id)
            logger.info(f"Extracted and saved {len(items)} action items")
        else:
            ids = []
            logger.info("No action items found in text")

        duration = time.time() - start_time
        return {
            "success": True,
            "data": {
                "note_id": note_id,
                "items": [{"id": i, "text": t} for i, t in zip(ids, items)],
                "extraction_method": "rule_based",
                "processing_time_ms": round(duration * 1000, 2)
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error extracting action items: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to extract action items")


@router.post("/extract-llm")
def extract_with_llm(payload: Dict[str, Any]) -> Dict[str, Any]:
    """使用LLM从文本中提取待办事项"""
    start_time = time.time()
    try:
        text = str(payload.get("text", "")).strip()
        if not text:
            raise HTTPException(status_code=400, detail="text is required")

        note_id: Optional[int] = None
        if payload.get("save_note"):
            note_id = db.insert_note(text)
            logger.info(f"Saved note with id: {note_id}")

        # 使用LLM提取action items
        logger.info("Starting LLM extraction...")
        items = extract_action_items_llm(text)

        # 批量插入数据库
        if items:
            ids = db.insert_action_items(items, note_id=note_id)
            logger.info(f"Extracted and saved {len(items)} action items using LLM")
        else:
            ids = []
            logger.info("No action items found in text using LLM")

        duration = time.time() - start_time
        return {
            "success": True,
            "data": {
                "note_id": note_id,
                "items": [{"id": i, "text": t} for i, t in zip(ids, items)],
                "extraction_method": "llm",
                "processing_time_ms": round(duration * 1000, 2)
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error extracting action items with LLM: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to extract action items with LLM")


@router.get("")
def list_all(note_id: Optional[int] = None, done: Optional[bool] = None) -> Dict[str, Any]:
    """获取所有待办事项"""
    try:
        rows = db.list_action_items(note_id=note_id)

        # 过滤完成状态
        if done is not None:
            rows = [r for r in rows if bool(r["done"]) == done]

        return {
            "success": True,
            "data": [
                {
                    "id": r["id"],
                    "note_id": r["note_id"],
                    "text": r["text"],
                    "done": bool(r["done"]),
                    "created_at": r["created_at"],
                }
                for r in rows
            ]
        }
    except Exception as e:
        logger.error(f"Error listing action items: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to list action items")


@router.post("/{action_item_id}/done")
def mark_done(action_item_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
    """标记待办事项完成状态"""
    try:
        done = bool(payload.get("done", True))
        db.mark_action_item_done(action_item_id, done)

        action_text = "completed" if done else "reopened"
        logger.info(f"Action item {action_item_id} {action_text}")

        return {
            "success": True,
            "data": {
                "id": action_item_id,
                "done": done
            }
        }
    except Exception as e:
        logger.error(f"Error updating action item {action_item_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to update action item")


@router.delete("/{action_item_id}")
def delete_action_item(action_item_id: int) -> Dict[str, Any]:
    """删除待办事项"""
    try:
        success = db.delete_action_item(action_item_id)
        if not success:
            raise HTTPException(status_code=404, detail="Action item not found")

        logger.info(f"Deleted action item {action_item_id}")
        return {
            "success": True,
            "message": "Action item deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting action item {action_item_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to delete action item")


