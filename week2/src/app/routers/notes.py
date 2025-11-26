from __future__ import annotations

from typing import Any, Dict, List
import logging

from fastapi import APIRouter, HTTPException

from .. import db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("")
def create_note(payload: Dict[str, Any]) -> Dict[str, Any]:
    """创建新笔记"""
    try:
        content = str(payload.get("content", "")).strip()
        if not content:
            raise HTTPException(status_code=400, detail="content is required")

        note_id = db.insert_note(content)
        note = db.get_note(note_id)

        if note is None:
            raise HTTPException(status_code=500, detail="Failed to create note")

        logger.info(f"Created note with id: {note_id}")
        return {
            "success": True,
            "data": {
                "id": note["id"],
                "content": note["content"],
                "created_at": note["created_at"],
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating note: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to create note")


@router.get("/{note_id}")
def get_single_note(note_id: int) -> Dict[str, Any]:
    """获取单个笔记"""
    try:
        row = db.get_note(note_id)
        if row is None:
            raise HTTPException(status_code=404, detail="note not found")

        return {
            "success": True,
            "data": {
                "id": row["id"],
                "content": row["content"],
                "created_at": row["created_at"]
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting note {note_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to get note")


@router.get("")
def list_notes() -> Dict[str, Any]:
    """获取所有笔记"""
    try:
        notes = db.list_notes()
        return {
            "success": True,
            "data": [
                {"id": note["id"], "content": note["content"], "created_at": note["created_at"]}
                for note in notes
            ]
        }
    except Exception as e:
        logger.error(f"Error listing notes: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to list notes")


