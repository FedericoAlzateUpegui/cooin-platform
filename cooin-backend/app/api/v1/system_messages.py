from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional
import math

from app.db.base import get_db
from app.core.deps import get_current_active_user as get_current_user
from app.models.user import User
from app.models.system_message import SystemMessageType, SystemMessagePriority
from app.schemas.system_message import (
    SystemMessageResponse,
    SystemMessageListResponse,
    SystemMessageUpdate,
    SystemMessageStats
)
from app.services.system_message_service import SystemMessageService

router = APIRouter()


@router.get("/", response_model=SystemMessageListResponse)
def get_system_messages(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    message_type: Optional[SystemMessageType] = Query(None, description="Filter by message type"),
    priority: Optional[SystemMessagePriority] = Query(None, description="Filter by priority"),
    is_read: Optional[bool] = Query(None, description="Filter by read status"),
    is_archived: Optional[bool] = Query(None, description="Filter by archived status"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get paginated system messages for the current user.

    - **page**: Page number (starts at 1)
    - **page_size**: Number of items per page (max 100)
    - **message_type**: Filter by message type (optional)
    - **priority**: Filter by priority level (optional)
    - **is_read**: Filter by read status (optional)
    - **is_archived**: Filter by archived status (optional)
    """
    skip = (page - 1) * page_size

    messages, total_count = SystemMessageService.get_user_messages(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=page_size,
        message_type=message_type,
        priority=priority,
        is_read=is_read,
        is_archived=is_archived
    )

    unread_count = SystemMessageService.get_unread_count(db=db, user_id=current_user.id)
    total_pages = math.ceil(total_count / page_size) if total_count > 0 else 0

    return SystemMessageListResponse(
        messages=messages,
        total_count=total_count,
        unread_count=unread_count,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/stats", response_model=SystemMessageStats)
def get_message_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get statistics about user's system messages.

    Returns:
    - Total message count
    - Unread message count
    - Archived message count
    - Messages breakdown by type
    - Messages breakdown by priority
    """
    return SystemMessageService.get_message_stats(db=db, user_id=current_user.id)


@router.get("/unread-count")
def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get count of unread system messages.
    Useful for notification badges.
    """
    count = SystemMessageService.get_unread_count(db=db, user_id=current_user.id)
    return {"unread_count": count}


@router.get("/{message_id}", response_model=SystemMessageResponse)
def get_system_message(
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific system message by ID.
    """
    message = SystemMessageService.get_message_by_id(
        db=db,
        message_id=message_id,
        user_id=current_user.id
    )

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="System message not found"
        )

    return message


@router.put("/{message_id}/read", response_model=SystemMessageResponse)
def mark_message_as_read(
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark a system message as read.
    """
    message = SystemMessageService.mark_as_read(
        db=db,
        message_id=message_id,
        user_id=current_user.id
    )

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="System message not found"
        )

    return message


@router.put("/read-all")
def mark_all_as_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark all system messages as read.
    """
    updated_count = SystemMessageService.mark_all_as_read(
        db=db,
        user_id=current_user.id
    )

    return {
        "message": "All messages marked as read",
        "updated_count": updated_count
    }


@router.put("/{message_id}/archive", response_model=SystemMessageResponse)
def archive_message(
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Archive a system message.
    Archived messages are hidden from main view but can be accessed via filters.
    """
    message = SystemMessageService.archive_message(
        db=db,
        message_id=message_id,
        user_id=current_user.id
    )

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="System message not found"
        )

    return message


@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message(
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a system message (soft delete).
    """
    deleted = SystemMessageService.delete_message(
        db=db,
        message_id=message_id,
        user_id=current_user.id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="System message not found"
        )

    return None
