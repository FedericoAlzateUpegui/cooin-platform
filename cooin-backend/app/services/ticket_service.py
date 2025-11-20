from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from app.models.ticket import Ticket, TicketStatus, TicketType, LoanType, WarrantyType
from app.models.connection import Connection, ConnectionStatus, ConnectionType
from app.models.user import User
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketFilter, CreateDealFromTicket
from app.core.exceptions import NotFoundError, BusinessLogicError, AuthorizationError, ErrorMessages


class TicketService:
    """Service for managing tickets (lending offers and borrowing requests)."""

    @staticmethod
    def create_ticket(db: Session, ticket_data: TicketCreate, user_id: int) -> Ticket:
        """Create a new ticket."""
        # Verify user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundError("User not found")

        # Verify user role matches ticket type
        if ticket_data.ticket_type == TicketType.LENDING_OFFER and not user.is_lender:
            raise BusinessLogicError(ErrorMessages.ONLY_LENDERS_CREATE_LENDING_OFFERS)
        if ticket_data.ticket_type == TicketType.BORROWING_REQUEST and not user.is_borrower:
            raise BusinessLogicError(ErrorMessages.ONLY_BORROWERS_CREATE_BORROWING_REQUESTS)

        # Create ticket
        ticket = Ticket(
            user_id=user_id,
            ticket_type=ticket_data.ticket_type,
            status=TicketStatus.ACTIVE,
            title=ticket_data.title,
            description=ticket_data.description,
            amount=ticket_data.amount,
            min_amount=ticket_data.min_amount,
            max_amount=ticket_data.max_amount,
            interest_rate=ticket_data.interest_rate,
            min_interest_rate=ticket_data.min_interest_rate,
            max_interest_rate=ticket_data.max_interest_rate,
            term_months=ticket_data.term_months,
            min_term_months=ticket_data.min_term_months,
            max_term_months=ticket_data.max_term_months,
            loan_type=ticket_data.loan_type,
            loan_purpose=ticket_data.loan_purpose,
            warranty_type=ticket_data.warranty_type,
            warranty_description=ticket_data.warranty_description,
            warranty_value=ticket_data.warranty_value,
            requirements=ticket_data.requirements,
            preferred_location=ticket_data.preferred_location,
            flexible_terms=ticket_data.flexible_terms,
            is_public=ticket_data.is_public,
            expires_at=ticket_data.expires_at,
            views_count=0,
            responses_count=0,
            deals_created=0
        )

        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        return ticket

    @staticmethod
    def get_ticket(db: Session, ticket_id: int, increment_view: bool = False) -> Ticket:
        """Get a ticket by ID."""
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            raise NotFoundError(f"Ticket with ID {ticket_id} not found")

        if increment_view:
            ticket.views_count = (ticket.views_count or 0) + 1
            ticket.last_viewed_at = datetime.utcnow()
            db.commit()
            db.refresh(ticket)

        return ticket

    @staticmethod
    def get_user_tickets(
        db: Session,
        user_id: int,
        ticket_type: Optional[TicketType] = None,
        status: Optional[TicketStatus] = None,
        skip: int = 0,
        limit: int = 20
    ) -> tuple[List[Ticket], int]:
        """Get all tickets for a specific user."""
        query = db.query(Ticket).filter(Ticket.user_id == user_id)

        if ticket_type:
            query = query.filter(Ticket.ticket_type == ticket_type)
        if status:
            query = query.filter(Ticket.status == status)

        total = query.count()
        tickets = query.order_by(Ticket.created_at.desc()).offset(skip).limit(limit).all()
        return tickets, total

    @staticmethod
    def list_tickets(
        db: Session,
        filters: TicketFilter,
        current_user_id: Optional[int] = None
    ) -> tuple[List[Ticket], int]:
        """List tickets with filtering and pagination."""
        query = db.query(Ticket)

        # Only show public tickets or user's own tickets
        if current_user_id:
            query = query.filter(
                or_(
                    Ticket.is_public == True,
                    Ticket.user_id == current_user_id
                )
            )
        else:
            query = query.filter(Ticket.is_public == True)

        # Apply filters
        if filters.ticket_type:
            query = query.filter(Ticket.ticket_type == filters.ticket_type)

        if filters.status:
            query = query.filter(Ticket.status == filters.status)

        if filters.loan_type:
            query = query.filter(Ticket.loan_type == filters.loan_type)

        if filters.warranty_type:
            query = query.filter(Ticket.warranty_type == filters.warranty_type)

        # Amount range filters
        if filters.min_amount:
            query = query.filter(
                or_(
                    Ticket.amount >= filters.min_amount,
                    Ticket.max_amount >= filters.min_amount
                )
            )

        if filters.max_amount:
            query = query.filter(
                or_(
                    Ticket.amount <= filters.max_amount,
                    Ticket.min_amount <= filters.max_amount
                )
            )

        # Interest rate filters
        if filters.min_interest_rate:
            query = query.filter(
                or_(
                    Ticket.interest_rate >= filters.min_interest_rate,
                    Ticket.max_interest_rate >= filters.min_interest_rate
                )
            )

        if filters.max_interest_rate:
            query = query.filter(
                or_(
                    Ticket.interest_rate <= filters.max_interest_rate,
                    Ticket.min_interest_rate <= filters.max_interest_rate
                )
            )

        # Term filters
        if filters.min_term_months:
            query = query.filter(
                or_(
                    Ticket.term_months >= filters.min_term_months,
                    Ticket.max_term_months >= filters.min_term_months
                )
            )

        if filters.max_term_months:
            query = query.filter(
                or_(
                    Ticket.term_months <= filters.max_term_months,
                    Ticket.min_term_months <= filters.max_term_months
                )
            )

        # Location filter
        if filters.location:
            query = query.filter(
                Ticket.preferred_location.ilike(f"%{filters.location}%")
            )

        # Flexible terms filter
        if filters.flexible_terms_only:
            query = query.filter(Ticket.flexible_terms == True)

        # Count total before pagination
        total = query.count()

        # Apply sorting
        if filters.sort_by == "created_at":
            sort_column = Ticket.created_at
        elif filters.sort_by == "amount":
            sort_column = Ticket.amount
        elif filters.sort_by == "interest_rate":
            sort_column = Ticket.interest_rate
        elif filters.sort_by == "views_count":
            sort_column = Ticket.views_count
        else:
            sort_column = Ticket.created_at

        if filters.sort_order == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

        # Apply pagination
        skip = (filters.page - 1) * filters.page_size
        tickets = query.offset(skip).limit(filters.page_size).all()

        return tickets, total

    @staticmethod
    def update_ticket(
        db: Session,
        ticket_id: int,
        user_id: int,
        ticket_data: TicketUpdate
    ) -> Ticket:
        """Update a ticket."""
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            raise NotFoundError(f"Ticket with ID {ticket_id} not found")

        # Verify ownership
        if ticket.user_id != user_id:
            raise AuthorizationError("You can only update your own tickets")

        # Update fields if provided
        update_data = ticket_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(ticket, field, value)

        ticket.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(ticket)
        return ticket

    @staticmethod
    def delete_ticket(db: Session, ticket_id: int, user_id: int) -> bool:
        """Delete (mark as cancelled) a ticket."""
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            raise NotFoundError(f"Ticket with ID {ticket_id} not found")

        # Verify ownership
        if ticket.user_id != user_id:
            raise AuthorizationError("You can only delete your own tickets")

        # Mark as cancelled instead of deleting
        ticket.status = TicketStatus.CANCELLED
        ticket.updated_at = datetime.utcnow()
        db.commit()
        return True

    @staticmethod
    def create_deal_from_ticket(
        db: Session,
        deal_data: CreateDealFromTicket,
        user_id: int
    ) -> Connection:
        """Create a connection (deal) from a ticket."""
        # Get the ticket
        ticket = db.query(Ticket).filter(Ticket.id == deal_data.ticket_id).first()
        if not ticket:
            raise NotFoundError(ErrorMessages.TICKET_NOT_FOUND)

        # Verify ticket is active
        if ticket.status != TicketStatus.ACTIVE:
            raise BusinessLogicError(ErrorMessages.TICKET_INACTIVE)

        # Verify ticket is public or user has access
        if not ticket.is_public and ticket.user_id != user_id:
            raise AuthorizationError("Cannot access private ticket")

        # Verify user is not creating deal with their own ticket
        if ticket.user_id == user_id:
            raise BusinessLogicError(ErrorMessages.CANNOT_CREATE_DEAL_WITH_OWN_TICKET)

        # Verify user role is compatible
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundError("User not found")

        if ticket.ticket_type == TicketType.LENDING_OFFER and not user.is_borrower:
            raise BusinessLogicError(ErrorMessages.ONLY_BORROWERS_RESPOND_TO_LENDING_OFFERS)
        if ticket.ticket_type == TicketType.BORROWING_REQUEST and not user.is_lender:
            raise BusinessLogicError(ErrorMessages.ONLY_LENDERS_RESPOND_TO_BORROWING_REQUESTS)

        # Check if connection already exists between these users
        existing_connection = db.query(Connection).filter(
            or_(
                and_(
                    Connection.requester_id == user_id,
                    Connection.receiver_id == ticket.user_id
                ),
                and_(
                    Connection.requester_id == ticket.user_id,
                    Connection.receiver_id == user_id
                )
            ),
            Connection.source_ticket_id == ticket.id
        ).first()

        if existing_connection:
            raise BusinessLogicError(ErrorMessages.DEAL_ALREADY_EXISTS)

        # Determine connection type based on ticket type
        if ticket.ticket_type == TicketType.LENDING_OFFER:
            connection_type = ConnectionType.LENDER_TO_BORROWER
            requester_id = ticket.user_id  # Lender
            receiver_id = user_id  # Borrower
        else:  # BORROWING_REQUEST
            connection_type = ConnectionType.BORROWER_TO_LENDER
            requester_id = user_id  # Lender
            receiver_id = ticket.user_id  # Borrower

        # Create the connection (deal)
        connection = Connection(
            requester_id=requester_id,
            receiver_id=receiver_id,
            connection_type=connection_type,
            status=ConnectionStatus.PENDING,
            initial_message=deal_data.message,
            source_ticket_id=ticket.id,
            proposed_amount=deal_data.proposed_amount or ticket.amount,
            proposed_interest_rate=deal_data.proposed_interest_rate or ticket.interest_rate,
            proposed_term_months=deal_data.proposed_term_months or ticket.term_months
        )

        db.add(connection)

        # Update ticket stats
        ticket.responses_count = (ticket.responses_count or 0) + 1
        ticket.deals_created = (ticket.deals_created or 0) + 1
        ticket.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(connection)
        return connection

    @staticmethod
    def get_ticket_stats(db: Session, user_id: int) -> dict:
        """Get statistics for user's tickets."""
        tickets = db.query(Ticket).filter(Ticket.user_id == user_id).all()

        stats = {
            "total_tickets": len(tickets),
            "active_tickets": len([t for t in tickets if t.status == TicketStatus.ACTIVE]),
            "completed_tickets": len([t for t in tickets if t.status == TicketStatus.COMPLETED]),
            "total_views": sum(t.views_count or 0 for t in tickets),
            "total_responses": sum(t.responses_count or 0 for t in tickets),
            "total_deals": sum(t.deals_created or 0 for t in tickets),
            "lending_offers": len([t for t in tickets if t.ticket_type == TicketType.LENDING_OFFER]),
            "borrowing_requests": len([t for t in tickets if t.ticket_type == TicketType.BORROWING_REQUEST])
        }

        return stats
