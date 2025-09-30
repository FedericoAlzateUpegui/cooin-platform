from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_active_user, get_database
from app.models.user import User
from app.models.connection import Connection
from app.schemas.connection import (
    ConnectionCreate, ConnectionUpdate, ConnectionResponse,
    ConnectionListResponse, ConnectionStatsResponse, MatchingCriteria,
    MatchingResponse, MessageCreate, MessageResponse, MessageListResponse
)
from app.services.connection_service import ConnectionService

router = APIRouter()


@router.post("/", response_model=ConnectionResponse, status_code=status.HTTP_201_CREATED)
async def create_connection(
    connection_data: ConnectionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Create a new connection request."""
    if connection_data.receiver_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create connection with yourself"
        )

    connection = ConnectionService.create_connection(
        db=db,
        requester_id=current_user.id,
        connection_data=connection_data
    )
    return connection


@router.get("/", response_model=ConnectionListResponse)
async def get_connections(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    status_filter: Optional[str] = Query(None, description="Filter by connection status"),
    connection_type: Optional[str] = Query(None, description="Filter by connection type"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Get paginated list of user's connections."""
    try:
        connections, total_count = ConnectionService.get_user_connections(
            db=db,
            user_id=current_user.id,
            page=page,
            page_size=page_size,
            status_filter=status_filter,
            connection_type_filter=connection_type
        )

        # Convert to response schema
        from app.schemas.connection import ConnectionListResponse
        response = ConnectionListResponse(
            connections=[ConnectionResponse.model_validate(conn) for conn in connections],
            total_count=total_count,
            page=page,
            page_size=page_size,
            has_next=(page * page_size) < total_count,
            has_previous=page > 1
        )
        return response
    except Exception as e:
        # Log the error for debugging
        import logging
        logging.error(f"Error in get_connections: {e}")
        raise


@router.get("/stats", response_model=ConnectionStatsResponse)
async def get_connection_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Get connection statistics for the current user."""
    stats = ConnectionService.get_connection_stats(db=db, user_id=current_user.id)
    return stats


@router.get("/pending", response_model=ConnectionListResponse)
async def get_pending_connections(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Get pending connection requests received by the user."""
    connections = ConnectionService.get_pending_requests(
        db=db,
        user_id=current_user.id,
        page=page,
        page_size=page_size
    )
    return connections


@router.get("/{connection_id}", response_model=ConnectionResponse)
async def get_connection(
    connection_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Get a specific connection by ID."""
    connection = ConnectionService.get_connection_by_id(
        db=db,
        connection_id=connection_id,
        user_id=current_user.id
    )
    if not connection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found"
        )
    return connection


@router.put("/{connection_id}", response_model=ConnectionResponse)
async def update_connection(
    connection_id: int,
    connection_data: ConnectionUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Update a connection (accept, reject, etc.). """
    connection = ConnectionService.update_connection(
        db=db,
        connection_id=connection_id,
        user_id=current_user.id,
        connection_update=connection_data
    )
    if not connection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found or you don't have permission to update it"
        )
    return connection


@router.delete("/{connection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_connection(
    connection_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Delete/cancel a connection."""
    success = ConnectionService.delete_connection(
        db=db,
        connection_id=connection_id,
        user_id=current_user.id
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found or you don't have permission to delete it"
        )


@router.post("/matching/search", response_model=MatchingResponse)
async def search_matches(
    criteria: MatchingCriteria,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Find potential matches based on criteria."""
    matches = ConnectionService.find_matches(
        db=db,
        current_user=current_user,
        criteria=criteria
    )
    return matches


@router.post("/{connection_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def send_message(
    connection_id: int,
    message_data: MessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Send a message in a connection."""
    message = ConnectionService.send_message(
        db=db,
        connection_id=connection_id,
        sender_id=current_user.id,
        message_data=message_data
    )
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found or you don't have permission to send messages"
        )
    return message


@router.get("/{connection_id}/messages", response_model=MessageListResponse)
async def get_messages(
    connection_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Get messages for a connection."""
    messages = ConnectionService.get_connection_messages(
        db=db,
        connection_id=connection_id,
        user_id=current_user.id,
        page=page,
        page_size=page_size
    )
    if messages is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found or you don't have access"
        )
    return messages


@router.put("/{connection_id}/messages/{message_id}/read", status_code=status.HTTP_204_NO_CONTENT)
async def mark_message_read(
    connection_id: int,
    message_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Mark a message as read."""
    success = ConnectionService.mark_message_read(
        db=db,
        message_id=message_id,
        user_id=current_user.id,
        connection_id=connection_id
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found or you don't have permission"
        )


@router.post("/{connection_id}/block", status_code=status.HTTP_204_NO_CONTENT)
async def block_connection(
    connection_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Block a connection/user."""
    success = ConnectionService.block_connection(
        db=db,
        connection_id=connection_id,
        user_id=current_user.id
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found"
        )


@router.post("/{connection_id}/report", status_code=status.HTTP_204_NO_CONTENT)
async def report_connection(
    connection_id: int,
    reason: str = Query(..., description="Reason for reporting"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Report a connection for inappropriate behavior."""
    success = ConnectionService.report_connection(
        db=db,
        connection_id=connection_id,
        reporter_id=current_user.id,
        reason=reason
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found"
        )