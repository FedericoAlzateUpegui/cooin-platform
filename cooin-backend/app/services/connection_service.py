from datetime import datetime, timedelta
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from fastapi import HTTPException, status
import logging
import time

from app.models import User, UserProfile, Connection, Message
from app.models.connection import ConnectionStatus, ConnectionType
from app.models.user import UserRole
from app.schemas.connection import (
    ConnectionCreate, ConnectionUpdate, MatchingCriteria, MatchingResult, MessageCreate
)

logger = logging.getLogger(__name__)


class ConnectionService:
    """Service class for connection and matching operations."""

    @staticmethod
    def create_connection(
        db: Session,
        requester_id: int,
        connection_data: ConnectionCreate
    ) -> Connection:
        """Create a new connection request."""
        try:
            # Validate users exist
            requester = db.query(User).filter(User.id == requester_id).first()
            receiver = db.query(User).filter(User.id == connection_data.receiver_id).first()

            if not requester or not receiver:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )

            # Prevent self-connection
            if requester_id == connection_data.receiver_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot create connection with yourself"
                )

            # Check for existing connection
            existing = db.query(Connection).filter(
                or_(
                    and_(
                        Connection.requester_id == requester_id,
                        Connection.receiver_id == connection_data.receiver_id
                    ),
                    and_(
                        Connection.requester_id == connection_data.receiver_id,
                        Connection.receiver_id == requester_id
                    )
                ),
                Connection.status.in_([ConnectionStatus.PENDING, ConnectionStatus.ACCEPTED])
            ).first()

            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Connection already exists between these users"
                )

            # Validate connection type based on user roles
            ConnectionService._validate_connection_type(
                requester, receiver, connection_data.connection_type
            )

            # Set expiration date (30 days for pending connections)
            expires_at = datetime.utcnow() + timedelta(days=30)

            # Create connection
            connection = Connection(
                requester_id=requester_id,
                receiver_id=connection_data.receiver_id,
                connection_type=ConnectionType(connection_data.connection_type),
                message=connection_data.message,
                loan_amount_requested=connection_data.loan_amount_requested,
                loan_term_months=connection_data.loan_term_months,
                interest_rate_proposed=connection_data.interest_rate_proposed,
                loan_purpose=connection_data.loan_purpose,
                priority_level=connection_data.priority_level,
                expires_at=expires_at
            )

            db.add(connection)
            db.commit()
            db.refresh(connection)

            logger.info(f"Connection created: {requester_id} -> {connection_data.receiver_id}")
            return connection

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating connection: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not create connection"
            )

    @staticmethod
    def _validate_connection_type(requester: User, receiver: User, connection_type: str):
        """Validate that connection type makes sense for user roles."""
        if connection_type == "lending_inquiry":
            if not receiver.is_lender:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot send lending inquiry to a non-lender"
                )
        elif connection_type == "borrowing_request":
            if not receiver.is_borrower:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot send borrowing request to a non-borrower"
                )

    @staticmethod
    def get_connection(db: Session, connection_id: int, user_id: int) -> Optional[Connection]:
        """Get connection by ID if user has access."""
        connection = db.query(Connection).filter(
            Connection.id == connection_id,
            or_(
                Connection.requester_id == user_id,
                Connection.receiver_id == user_id
            )
        ).first()
        return connection

    @staticmethod
    def update_connection(
        db: Session,
        connection_id: int,
        user_id: int,
        connection_update: ConnectionUpdate
    ) -> Connection:
        """Update connection (accept, reject, etc.)."""
        try:
            connection = ConnectionService.get_connection(db, connection_id, user_id)
            if not connection:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Connection not found"
                )

            # Only receiver can change status
            if connection_update.status and connection.receiver_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only the receiver can change connection status"
                )

            # Update fields based on user permissions
            if connection_update.status:
                if connection_update.status == "accepted":
                    connection.accept_connection(connection_update.response_message)
                elif connection_update.status == "rejected":
                    connection.reject_connection(connection_update.response_message)
                elif connection_update.status == "blocked":
                    connection.block_connection()

            # Update notes based on user role
            if connection_update.requester_notes and connection.requester_id == user_id:
                connection.requester_notes = connection_update.requester_notes

            if connection_update.receiver_notes and connection.receiver_id == user_id:
                connection.receiver_notes = connection_update.receiver_notes

            # Update interest rate (both parties can propose)
            if connection_update.interest_rate_proposed:
                connection.interest_rate_proposed = connection_update.interest_rate_proposed

            connection.updated_at = datetime.utcnow()

            # Check for mutual connection
            if connection.status == ConnectionStatus.ACCEPTED:
                mutual = db.query(Connection).filter(
                    Connection.requester_id == connection.receiver_id,
                    Connection.receiver_id == connection.requester_id,
                    Connection.status == ConnectionStatus.ACCEPTED
                ).first()
                if mutual:
                    connection.is_mutual = True
                    mutual.is_mutual = True

            db.commit()
            db.refresh(connection)

            logger.info(f"Connection updated: {connection_id} by user {user_id}")
            return connection

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating connection: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not update connection"
            )

    @staticmethod
    def get_user_connections(
        db: Session,
        user_id: int,
        status_filter: Optional[str] = None,
        connection_type_filter: Optional[str] = None,
        sent_only: bool = False,
        received_only: bool = False,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[Connection], int]:
        """Get user's connections with filtering and pagination."""
        try:
            # Base query
            query = db.query(Connection).filter(
                or_(
                    Connection.requester_id == user_id,
                    Connection.receiver_id == user_id
                )
            )

            # Apply filters
            if status_filter:
                query = query.filter(Connection.status == ConnectionStatus(status_filter))

            if connection_type_filter:
                query = query.filter(Connection.connection_type == ConnectionType(connection_type_filter))

            if sent_only:
                query = query.filter(Connection.requester_id == user_id)
            elif received_only:
                query = query.filter(Connection.receiver_id == user_id)

            # Get total count
            total_count = query.count()

            # Apply pagination and ordering
            connections = query.order_by(desc(Connection.created_at)).offset(
                (page - 1) * page_size
            ).limit(page_size).all()

            return connections, total_count

        except Exception as e:
            logger.error(f"Error getting user connections: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not retrieve connections"
            )

    @staticmethod
    def get_connection_stats(db: Session, user_id: int) -> dict:
        """Get connection statistics for a user."""
        try:
            stats = {
                "total_connections": 0,
                "pending_sent": 0,
                "pending_received": 0,
                "accepted_connections": 0,
                "rejected_connections": 0,
                "mutual_connections": 0,
                "recent_activity": 0
            }

            # Total connections
            stats["total_connections"] = db.query(Connection).filter(
                or_(
                    Connection.requester_id == user_id,
                    Connection.receiver_id == user_id
                )
            ).count()

            # Pending sent
            stats["pending_sent"] = db.query(Connection).filter(
                Connection.requester_id == user_id,
                Connection.status == ConnectionStatus.PENDING
            ).count()

            # Pending received
            stats["pending_received"] = db.query(Connection).filter(
                Connection.receiver_id == user_id,
                Connection.status == ConnectionStatus.PENDING
            ).count()

            # Accepted connections
            stats["accepted_connections"] = db.query(Connection).filter(
                or_(
                    Connection.requester_id == user_id,
                    Connection.receiver_id == user_id
                ),
                Connection.status == ConnectionStatus.ACCEPTED
            ).count()

            # Rejected connections
            stats["rejected_connections"] = db.query(Connection).filter(
                or_(
                    Connection.requester_id == user_id,
                    Connection.receiver_id == user_id
                ),
                Connection.status == ConnectionStatus.REJECTED
            ).count()

            # Mutual connections
            stats["mutual_connections"] = db.query(Connection).filter(
                or_(
                    Connection.requester_id == user_id,
                    Connection.receiver_id == user_id
                ),
                Connection.is_mutual == True
            ).count()

            # Recent activity (last 7 days)
            week_ago = datetime.utcnow() - timedelta(days=7)
            stats["recent_activity"] = db.query(Connection).filter(
                or_(
                    Connection.requester_id == user_id,
                    Connection.receiver_id == user_id
                ),
                Connection.created_at >= week_ago
            ).count()

            return stats

        except Exception as e:
            logger.error(f"Error getting connection stats: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not retrieve connection statistics"
            )

    @staticmethod
    def delete_connection(db: Session, connection_id: int, user_id: int) -> bool:
        """Delete/cancel a connection."""
        try:
            connection = ConnectionService.get_connection(db, connection_id, user_id)
            if not connection:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Connection not found"
                )

            # Only allow deletion if user is requester and connection is pending
            if connection.requester_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only the requester can cancel a connection"
                )

            if connection.status != ConnectionStatus.PENDING:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Can only cancel pending connections"
                )

            db.delete(connection)
            db.commit()

            logger.info(f"Connection deleted: {connection_id} by user {user_id}")
            return True

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting connection: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not delete connection"
            )

    @staticmethod
    def find_matches(
        db: Session,
        current_user: User,
        criteria: MatchingCriteria,
        limit: int = 20
    ) -> dict:
        """Find matching users based on criteria."""
        start_time = time.time()

        try:

            # Start with base query for public profiles
            query = db.query(User, UserProfile).join(UserProfile).filter(
                UserProfile.is_profile_public == True,
                User.is_active == True,
                User.id != current_user.id  # Exclude current user
            )

            # Filter by role (opposite of current user's interest)
            if criteria.user_role:
                if criteria.user_role == "lender":
                    query = query.filter(User.role.in_([UserRole.LENDER, UserRole.BOTH]))
                elif criteria.user_role == "borrower":
                    query = query.filter(User.role.in_([UserRole.BORROWER, UserRole.BOTH]))

            # Location filter
            if criteria.location:
                query = query.filter(
                    or_(
                        UserProfile.city.ilike(f"%{criteria.location}%"),
                        UserProfile.state_province.ilike(f"%{criteria.location}%"),
                        UserProfile.country.ilike(f"%{criteria.location}%")
                    )
                )

            # Loan amount filters
            if criteria.min_loan_amount:
                query = query.filter(
                    or_(
                        UserProfile.max_loan_amount >= criteria.min_loan_amount,
                        UserProfile.requested_loan_amount >= criteria.min_loan_amount
                    )
                )

            if criteria.max_loan_amount:
                query = query.filter(
                    or_(
                        UserProfile.min_loan_amount <= criteria.max_loan_amount,
                        UserProfile.requested_loan_amount <= criteria.max_loan_amount
                    )
                )

            # Loan purpose filter
            if criteria.loan_purpose:
                query = query.filter(UserProfile.loan_purpose == criteria.loan_purpose)

            # Verification filter
            if criteria.verified_only:
                query = query.filter(UserProfile.identity_verified == True)

            # Income range filter
            if criteria.income_range:
                query = query.filter(UserProfile.income_range == criteria.income_range)

            # Execute query
            results = query.limit(limit * 2).all()  # Get more results for scoring

            # Calculate compatibility scores and create matches
            matches = []
            for user, profile in results:
                score = ConnectionService._calculate_compatibility_score(
                    current_user, user, profile, criteria
                )

                if score > 30:  # Minimum compatibility threshold
                    match_reasons = ConnectionService._generate_match_reasons(
                        current_user, user, profile, criteria
                    )

                    # Format loan amount range
                    loan_amount_range = None
                    if profile.min_loan_amount and profile.max_loan_amount:
                        loan_amount_range = f"${profile.min_loan_amount:,.0f} - ${profile.max_loan_amount:,.0f}"
                    elif profile.requested_loan_amount:
                        loan_amount_range = f"${profile.requested_loan_amount:,.0f}"

                    match = MatchingResult(
                        user_id=user.id,
                        compatibility_score=score,
                        match_reasons=match_reasons,
                        public_name=profile.public_name,
                        location_string=profile.location_string,
                        profile_completion_percentage=profile.profile_completion_percentage,
                        is_verified=profile.identity_verified,
                        loan_amount_range=loan_amount_range
                    )
                    matches.append(match)

            # Sort by compatibility score
            matches.sort(key=lambda x: x.compatibility_score, reverse=True)
            matches = matches[:limit]

            search_time_ms = int((time.time() - start_time) * 1000)
            logger.info(f"Found {len(matches)} matches for user {current_user.id} in {search_time_ms}ms")

            return {
                "matches": matches,
                "total_matches": len(matches),
                "search_criteria": criteria,
                "search_time_ms": search_time_ms
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error finding matches: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not find matches"
            )

    @staticmethod
    def _calculate_compatibility_score(
        current_user: User,
        potential_match: User,
        match_profile: UserProfile,
        criteria: MatchingCriteria
    ) -> float:
        """Calculate compatibility score between users."""
        score = 0.0
        max_score = 100.0

        # Profile completion bonus (10 points max)
        completion_bonus = min(match_profile.profile_completion_percentage / 10, 10)
        score += completion_bonus

        # Verification bonus (15 points)
        if match_profile.identity_verified:
            score += 15

        # Role compatibility (20 points)
        if current_user.is_borrower and potential_match.is_lender:
            score += 20
        elif current_user.is_lender and potential_match.is_borrower:
            score += 20
        elif current_user.role == potential_match.role:
            score += 10  # Same role, might be for networking

        # Location match (15 points)
        if criteria.location and match_profile.location_string:
            if criteria.location.lower() in match_profile.location_string.lower():
                score += 15

        # Loan amount compatibility (20 points)
        if criteria.min_loan_amount and criteria.max_loan_amount:
            if match_profile.min_loan_amount and match_profile.max_loan_amount:
                # Check for overlap in loan amount ranges
                overlap = min(criteria.max_loan_amount, match_profile.max_loan_amount) - \
                         max(criteria.min_loan_amount, match_profile.min_loan_amount)
                if overlap > 0:
                    score += 20

        # Loan purpose match (10 points)
        if criteria.loan_purpose and match_profile.loan_purpose == criteria.loan_purpose:
            score += 10

        # Interest rate compatibility (10 points)
        if criteria.max_interest_rate and match_profile.preferred_interest_rate:
            if match_profile.preferred_interest_rate <= criteria.max_interest_rate:
                score += 10

        return min(score, max_score)

    @staticmethod
    def _generate_match_reasons(
        current_user: User,
        potential_match: User,
        match_profile: UserProfile,
        criteria: MatchingCriteria
    ) -> List[str]:
        """Generate reasons why this is a good match."""
        reasons = []

        # Profile completion
        if match_profile.profile_completion_percentage >= 80:
            reasons.append("Complete profile with detailed information")

        # Verification status
        if match_profile.identity_verified:
            reasons.append("Verified user with confirmed identity")

        # Role compatibility
        if current_user.is_borrower and potential_match.is_lender:
            reasons.append("Experienced lender matching your borrowing needs")
        elif current_user.is_lender and potential_match.is_borrower:
            reasons.append("Active borrower seeking loans in your range")

        # Location match
        if criteria.location and match_profile.location_string:
            if criteria.location.lower() in match_profile.location_string.lower():
                reasons.append(f"Located in your preferred area ({match_profile.location_string})")

        # Loan amount compatibility
        if criteria.min_loan_amount and criteria.max_loan_amount:
            if match_profile.min_loan_amount and match_profile.max_loan_amount:
                reasons.append(f"Loan amount matches your range (${match_profile.min_loan_amount:,.0f}-${match_profile.max_loan_amount:,.0f})")

        # Loan purpose match
        if criteria.loan_purpose and match_profile.loan_purpose == criteria.loan_purpose:
            reasons.append(f"Specializes in {criteria.loan_purpose.replace('_', ' ')} loans")

        return reasons[:3]  # Limit to top 3 reasons

    # Messaging Methods
    @staticmethod
    def send_message(
        db: Session,
        connection_id: int,
        sender_id: int,
        message_data: MessageCreate
    ) -> Optional[Message]:
        """Send a message in a connection."""
        try:
            # Validate connection exists and user has access
            connection = db.query(Connection).filter(
                Connection.id == connection_id,
                or_(
                    Connection.requester_id == sender_id,
                    Connection.receiver_id == sender_id
                ),
                Connection.status == ConnectionStatus.ACCEPTED
            ).first()

            if not connection:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Connection not found or not active"
                )

            # Determine receiver
            receiver_id = connection.receiver_id if sender_id == connection.requester_id else connection.requester_id

            # Create message
            message = Message(
                connection_id=connection_id,
                sender_id=sender_id,
                receiver_id=receiver_id,
                content=message_data.content,
                message_type=message_data.message_type
            )

            db.add(message)

            # Update connection stats
            connection.last_message_at = datetime.utcnow()
            connection.message_count += 1

            db.commit()
            db.refresh(message)

            logger.info(f"Message sent: connection {connection_id}, sender {sender_id}")
            return message

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error sending message: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not send message"
            )

    @staticmethod
    def get_connection_messages(
        db: Session,
        connection_id: int,
        user_id: int,
        page: int = 1,
        page_size: int = 50
    ) -> Optional[dict]:
        """Get messages for a connection."""
        try:
            # Validate user has access to connection
            connection = db.query(Connection).filter(
                Connection.id == connection_id,
                or_(
                    Connection.requester_id == user_id,
                    Connection.receiver_id == user_id
                )
            ).first()

            if not connection:
                return None

            # Get messages
            messages_query = db.query(Message).filter(
                Message.connection_id == connection_id,
                Message.is_deleted == False
            ).filter(
                or_(
                    and_(Message.sender_id == user_id, Message.deleted_by_sender == False),
                    and_(Message.receiver_id == user_id, Message.deleted_by_receiver == False)
                )
            )

            total_count = messages_query.count()

            # Get unread count for current user
            unread_count = messages_query.filter(
                Message.receiver_id == user_id,
                Message.is_read == False
            ).count()

            # Apply pagination and ordering (newest first)
            messages = messages_query.order_by(desc(Message.created_at)).offset(
                (page - 1) * page_size
            ).limit(page_size).all()

            return {
                "messages": messages,
                "total_count": total_count,
                "unread_count": unread_count,
                "page": page,
                "page_size": page_size,
                "has_next": total_count > page * page_size,
                "has_previous": page > 1
            }

        except Exception as e:
            logger.error(f"Error getting connection messages: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not retrieve messages"
            )

    @staticmethod
    def mark_message_read(
        db: Session,
        message_id: int,
        user_id: int,
        connection_id: int
    ) -> bool:
        """Mark a message as read."""
        try:
            # Validate user has access to the connection
            connection = db.query(Connection).filter(
                Connection.id == connection_id,
                or_(
                    Connection.requester_id == user_id,
                    Connection.receiver_id == user_id
                )
            ).first()

            if not connection:
                return False

            # Find message and mark as read if user is receiver
            message = db.query(Message).filter(
                Message.id == message_id,
                Message.connection_id == connection_id,
                Message.receiver_id == user_id
            ).first()

            if message and not message.is_read:
                message.mark_as_read()
                db.commit()
                return True

            return False

        except Exception as e:
            logger.error(f"Error marking message as read: {e}")
            db.rollback()
            return False

    @staticmethod
    def block_connection(db: Session, connection_id: int, user_id: int) -> bool:
        """Block a connection."""
        try:
            connection = db.query(Connection).filter(
                Connection.id == connection_id,
                or_(
                    Connection.requester_id == user_id,
                    Connection.receiver_id == user_id
                )
            ).first()

            if not connection:
                return False

            connection.block_connection()
            db.commit()

            logger.info(f"Connection blocked: {connection_id} by user {user_id}")
            return True

        except Exception as e:
            db.rollback()
            logger.error(f"Error blocking connection: {e}")
            return False

    @staticmethod
    def report_connection(
        db: Session,
        connection_id: int,
        reporter_id: int,
        reason: str
    ) -> bool:
        """Report a connection for inappropriate behavior."""
        try:
            connection = db.query(Connection).filter(
                Connection.id == connection_id,
                or_(
                    Connection.requester_id == reporter_id,
                    Connection.receiver_id == reporter_id
                )
            ).first()

            if not connection:
                return False

            # Here you would typically create a Report record
            # For now, we'll log the report and block the connection
            logger.warning(f"Connection reported: {connection_id} by user {reporter_id}, reason: {reason}")

            # You can add a Report model later to track these properly
            connection.block_connection()
            db.commit()

            return True

        except Exception as e:
            db.rollback()
            logger.error(f"Error reporting connection: {e}")
            return False

    @staticmethod
    def get_connection_by_id(db: Session, connection_id: int, user_id: int) -> Optional[Connection]:
        """Get a specific connection by ID."""
        return ConnectionService.get_connection(db, connection_id, user_id)

    @staticmethod
    def get_pending_requests(
        db: Session,
        user_id: int,
        page: int = 1,
        page_size: int = 20
    ) -> dict:
        """Get pending connection requests received by the user."""
        try:
            # Get pending requests where user is the receiver
            query = db.query(Connection).filter(
                Connection.receiver_id == user_id,
                Connection.status == ConnectionStatus.PENDING
            )

            total_count = query.count()

            # Apply pagination and ordering
            connections = query.order_by(desc(Connection.created_at)).offset(
                (page - 1) * page_size
            ).limit(page_size).all()

            return {
                "connections": connections,
                "total_count": total_count,
                "page": page,
                "page_size": page_size,
                "has_next": total_count > page * page_size,
                "has_previous": page > 1
            }

        except Exception as e:
            logger.error(f"Error getting pending requests: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not retrieve pending requests"
            )

    @staticmethod
    def expire_old_connections(db: Session) -> int:
        """Expire old pending connections (utility method for background tasks)."""
        try:
            expired_count = 0
            now = datetime.utcnow()

            # Find expired pending connections
            expired_connections = db.query(Connection).filter(
                Connection.status == ConnectionStatus.PENDING,
                Connection.expires_at < now
            ).all()

            for connection in expired_connections:
                connection.expire_connection()
                expired_count += 1

            if expired_count > 0:
                db.commit()
                logger.info(f"Expired {expired_count} old connections")

            return expired_count

        except Exception as e:
            db.rollback()
            logger.error(f"Error expiring connections: {e}")
            return 0