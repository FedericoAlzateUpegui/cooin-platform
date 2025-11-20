from typing import List
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.ticket import TicketType, TicketStatus
from app.schemas.ticket import (
    TicketCreate,
    TicketUpdate,
    TicketResponse,
    TicketListResponse,
    TicketFilter,
    CreateDealFromTicket,
    TicketStats
)
from app.schemas.connection import ConnectionResponse
from app.services.ticket_service import TicketService

router = APIRouter()


@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(
    ticket_data: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new ticket (lending offer or borrowing request).

    - **ticket_type**: Type of ticket (LENDING_OFFER or BORROWING_REQUEST)
    - **title**: Short descriptive title
    - **description**: Detailed description
    - **amount**: Loan amount
    - **interest_rate**: Annual interest rate (%)
    - **term_months**: Loan term in months
    - **loan_type**: Type of loan (PERSONAL, BUSINESS, etc.)
    - **loan_purpose**: Purpose/reason for the loan
    """
    ticket = TicketService.create_ticket(db, ticket_data, current_user.id)
    return ticket


@router.get("/", response_model=TicketListResponse)
def list_tickets(
    ticket_type: TicketType = Query(None, description="Filter by ticket type"),
    status: TicketStatus = Query(TicketStatus.ACTIVE, description="Filter by status"),
    loan_type: str = Query(None, description="Filter by loan type"),
    min_amount: float = Query(None, gt=0, description="Minimum amount"),
    max_amount: float = Query(None, gt=0, description="Maximum amount"),
    min_interest_rate: float = Query(None, ge=0, le=100),
    max_interest_rate: float = Query(None, ge=0, le=100),
    min_term_months: int = Query(None, gt=0),
    max_term_months: int = Query(None, gt=0),
    location: str = Query(None, description="Location filter"),
    flexible_terms_only: bool = Query(False),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort_by: str = Query("created_at", description="Field to sort by"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all public tickets with filtering and pagination.

    Returns tickets that match the specified filters, sorted by the requested field.
    """
    filters = TicketFilter(
        ticket_type=ticket_type,
        status=status,
        loan_type=loan_type,
        min_amount=min_amount,
        max_amount=max_amount,
        min_interest_rate=min_interest_rate,
        max_interest_rate=max_interest_rate,
        min_term_months=min_term_months,
        max_term_months=max_term_months,
        location=location,
        flexible_terms_only=flexible_terms_only,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order
    )

    tickets, total = TicketService.list_tickets(db, filters, current_user.id)

    total_pages = (total + page_size - 1) // page_size

    return TicketListResponse(
        tickets=tickets,
        total_count=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/my-tickets", response_model=TicketListResponse)
def get_my_tickets(
    ticket_type: TicketType = Query(None),
    status: TicketStatus = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all tickets created by the current user."""
    skip = (page - 1) * page_size
    tickets, total = TicketService.get_user_tickets(
        db,
        current_user.id,
        ticket_type=ticket_type,
        status=status,
        skip=skip,
        limit=page_size
    )

    total_pages = (total + page_size - 1) // page_size

    return TicketListResponse(
        tickets=tickets,
        total_count=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/stats", response_model=TicketStats)
def get_my_ticket_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get statistics for current user's tickets."""
    stats = TicketService.get_ticket_stats(db, current_user.id)
    return stats


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific ticket by ID.

    Increments the view count when accessed.
    """
    # Only increment view if not the ticket owner
    ticket = TicketService.get_ticket(db, ticket_id, increment_view=True)

    # Don't increment view for own tickets
    if ticket.user_id == current_user.id:
        ticket.views_count = (ticket.views_count or 1) - 1  # Undo the increment
        db.commit()

    return ticket


@router.put("/{ticket_id}", response_model=TicketResponse)
def update_ticket(
    ticket_id: int,
    ticket_data: TicketUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a ticket.

    Only the ticket owner can update their tickets.
    """
    ticket = TicketService.update_ticket(db, ticket_id, current_user.id, ticket_data)
    return ticket


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete (cancel) a ticket.

    Only the ticket owner can delete their tickets.
    This marks the ticket as CANCELLED rather than removing it from the database.
    """
    TicketService.delete_ticket(db, ticket_id, current_user.id)
    return None


@router.post("/create-deal", response_model=ConnectionResponse, status_code=status.HTTP_201_CREATED)
def create_deal_from_ticket(
    deal_data: CreateDealFromTicket,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a deal (connection) from a ticket.

    This allows users to respond to tickets and initiate a lending/borrowing connection.

    - **ticket_id**: ID of the ticket to respond to
    - **message**: Message to the ticket creator
    - **proposed_amount**: Optional counter-offer for amount (if ticket allows flexible terms)
    - **proposed_interest_rate**: Optional counter-offer for interest rate
    - **proposed_term_months**: Optional counter-offer for term length
    """
    connection = TicketService.create_deal_from_ticket(db, deal_data, current_user.id)
    return connection
