from datetime import datetime
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_

from app.models.system_message import SystemMessage, SystemMessageType, SystemMessagePriority
from app.models.user import User
from app.schemas.system_message import (
    SystemMessageCreate,
    SystemMessageBulkCreate,
    SystemMessageUpdate,
    SystemMessageStats
)


class SystemMessageService:
    """Service for managing system messages."""

    @staticmethod
    def create_message(
        db: Session,
        user_id: int,
        title: str,
        content: str,
        message_type: SystemMessageType,
        priority: SystemMessagePriority = SystemMessagePriority.MEDIUM,
        action_url: Optional[str] = None,
        action_label: Optional[str] = None,
        image_url: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[str] = None,
        expires_at: Optional[datetime] = None
    ) -> SystemMessage:
        """Create a new system message for a user."""
        message = SystemMessage(
            user_id=user_id,
            title=title,
            content=content,
            message_type=message_type,
            priority=priority,
            action_url=action_url,
            action_label=action_label,
            image_url=image_url,
            category=category,
            tags=tags,
            expires_at=expires_at
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    @staticmethod
    def create_bulk_messages(
        db: Session,
        user_ids: List[int],
        title: str,
        content: str,
        message_type: SystemMessageType,
        priority: SystemMessagePriority = SystemMessagePriority.MEDIUM,
        action_url: Optional[str] = None,
        action_label: Optional[str] = None,
        image_url: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[str] = None,
        expires_at: Optional[datetime] = None
    ) -> List[SystemMessage]:
        """Create system messages for multiple users."""
        messages = []
        for user_id in user_ids:
            message = SystemMessage(
                user_id=user_id,
                title=title,
                content=content,
                message_type=message_type,
                priority=priority,
                action_url=action_url,
                action_label=action_label,
                image_url=image_url,
                category=category,
                tags=tags,
                expires_at=expires_at
            )
            messages.append(message)

        db.bulk_save_objects(messages)
        db.commit()
        return messages

    @staticmethod
    def get_user_messages(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 50,
        message_type: Optional[SystemMessageType] = None,
        priority: Optional[SystemMessagePriority] = None,
        is_read: Optional[bool] = None,
        is_archived: Optional[bool] = None,
        include_expired: bool = False
    ) -> tuple[List[SystemMessage], int]:
        """Get paginated system messages for a user."""
        query = db.query(SystemMessage).filter(
            SystemMessage.user_id == user_id,
            SystemMessage.is_deleted == False
        )

        # Filter by message type
        if message_type:
            query = query.filter(SystemMessage.message_type == message_type)

        # Filter by priority
        if priority:
            query = query.filter(SystemMessage.priority == priority)

        # Filter by read status
        if is_read is not None:
            query = query.filter(SystemMessage.is_read == is_read)

        # Filter by archived status
        if is_archived is not None:
            query = query.filter(SystemMessage.is_archived == is_archived)

        # Filter expired messages
        if not include_expired:
            query = query.filter(
                or_(
                    SystemMessage.expires_at.is_(None),
                    SystemMessage.expires_at > datetime.utcnow()
                )
            )

        # Get total count
        total_count = query.count()

        # Order by priority and creation date
        priority_order = {
            SystemMessagePriority.URGENT: 1,
            SystemMessagePriority.HIGH: 2,
            SystemMessagePriority.MEDIUM: 3,
            SystemMessagePriority.LOW: 4
        }

        messages = query.order_by(
            SystemMessage.is_read.asc(),  # Unread first
            SystemMessage.created_at.desc()  # Newest first
        ).offset(skip).limit(limit).all()

        return messages, total_count

    @staticmethod
    def get_message_by_id(
        db: Session,
        message_id: int,
        user_id: int
    ) -> Optional[SystemMessage]:
        """Get a specific system message by ID."""
        return db.query(SystemMessage).filter(
            SystemMessage.id == message_id,
            SystemMessage.user_id == user_id,
            SystemMessage.is_deleted == False
        ).first()

    @staticmethod
    def mark_as_read(
        db: Session,
        message_id: int,
        user_id: int
    ) -> Optional[SystemMessage]:
        """Mark a message as read."""
        message = db.query(SystemMessage).filter(
            SystemMessage.id == message_id,
            SystemMessage.user_id == user_id
        ).first()

        if message and not message.is_read:
            message.mark_as_read()
            db.commit()
            db.refresh(message)

        return message

    @staticmethod
    def mark_all_as_read(
        db: Session,
        user_id: int
    ) -> int:
        """Mark all messages as read for a user."""
        updated = db.query(SystemMessage).filter(
            SystemMessage.user_id == user_id,
            SystemMessage.is_read == False,
            SystemMessage.is_deleted == False
        ).update({
            "is_read": True,
            "read_at": datetime.utcnow()
        })
        db.commit()
        return updated

    @staticmethod
    def archive_message(
        db: Session,
        message_id: int,
        user_id: int
    ) -> Optional[SystemMessage]:
        """Archive a message."""
        message = db.query(SystemMessage).filter(
            SystemMessage.id == message_id,
            SystemMessage.user_id == user_id
        ).first()

        if message:
            message.archive()
            db.commit()
            db.refresh(message)

        return message

    @staticmethod
    def delete_message(
        db: Session,
        message_id: int,
        user_id: int
    ) -> bool:
        """Soft delete a message."""
        message = db.query(SystemMessage).filter(
            SystemMessage.id == message_id,
            SystemMessage.user_id == user_id
        ).first()

        if message:
            message.soft_delete()
            db.commit()
            return True

        return False

    @staticmethod
    def get_unread_count(
        db: Session,
        user_id: int
    ) -> int:
        """Get count of unread messages for a user."""
        return db.query(SystemMessage).filter(
            SystemMessage.user_id == user_id,
            SystemMessage.is_read == False,
            SystemMessage.is_deleted == False,
            SystemMessage.is_archived == False,
            or_(
                SystemMessage.expires_at.is_(None),
                SystemMessage.expires_at > datetime.utcnow()
            )
        ).count()

    @staticmethod
    def get_message_stats(
        db: Session,
        user_id: int
    ) -> SystemMessageStats:
        """Get statistics about user's system messages."""
        total = db.query(SystemMessage).filter(
            SystemMessage.user_id == user_id,
            SystemMessage.is_deleted == False
        ).count()

        unread = db.query(SystemMessage).filter(
            SystemMessage.user_id == user_id,
            SystemMessage.is_read == False,
            SystemMessage.is_deleted == False
        ).count()

        archived = db.query(SystemMessage).filter(
            SystemMessage.user_id == user_id,
            SystemMessage.is_archived == True,
            SystemMessage.is_deleted == False
        ).count()

        # Messages by type
        type_counts = db.query(
            SystemMessage.message_type,
            func.count(SystemMessage.id)
        ).filter(
            SystemMessage.user_id == user_id,
            SystemMessage.is_deleted == False
        ).group_by(SystemMessage.message_type).all()

        messages_by_type = {
            str(msg_type.value): count for msg_type, count in type_counts
        }

        # Messages by priority
        priority_counts = db.query(
            SystemMessage.priority,
            func.count(SystemMessage.id)
        ).filter(
            SystemMessage.user_id == user_id,
            SystemMessage.is_deleted == False
        ).group_by(SystemMessage.priority).all()

        messages_by_priority = {
            str(priority.value): count for priority, count in priority_counts
        }

        return SystemMessageStats(
            total_messages=total,
            unread_messages=unread,
            archived_messages=archived,
            messages_by_type=messages_by_type,
            messages_by_priority=messages_by_priority
        )

    @staticmethod
    def cleanup_expired_messages(db: Session) -> int:
        """Delete expired messages (scheduled job)."""
        deleted = db.query(SystemMessage).filter(
            SystemMessage.expires_at.isnot(None),
            SystemMessage.expires_at < datetime.utcnow()
        ).update({
            "is_deleted": True,
            "deleted_at": datetime.utcnow()
        })
        db.commit()
        return deleted


# Pre-defined educational content templates
class EducationalContentTemplates:
    """Templates for educational messages about lending business."""

    LENDING_TIPS = [
        {
            "title": "Tip: Verify Borrower's Credit History",
            "content": "Before lending money, always verify the borrower's credit history and financial stability. A good credit score indicates responsible financial behavior and increases the likelihood of timely repayment.",
            "category": "Risk Management",
            "tags": "credit,verification,best-practices"
        },
        {
            "title": "Diversify Your Lending Portfolio",
            "content": "Don't put all your eggs in one basket. Spread your lending across multiple borrowers with different risk profiles. This reduces your overall risk and protects your capital.",
            "category": "Portfolio Management",
            "tags": "diversification,risk-management,strategy"
        },
        {
            "title": "Set Clear Repayment Terms",
            "content": "Always establish clear, written repayment terms including amount, interest rate, payment schedule, and consequences of late payment. Clear terms prevent misunderstandings and disputes.",
            "category": "Best Practices",
            "tags": "contracts,terms,agreements"
        },
        {
            "title": "Understanding Interest Rate Calculations",
            "content": "Learn how to calculate simple vs compound interest. Simple interest is calculated only on the principal amount, while compound interest is calculated on principal plus accumulated interest. This affects your returns significantly.",
            "category": "Financial Literacy",
            "tags": "interest,calculations,finance"
        },
        {
            "title": "Assess Borrower Creditworthiness",
            "content": "Key factors to assess: stable income, employment history, existing debt levels, payment history, and debt-to-income ratio. These indicators help predict repayment ability.",
            "category": "Credit Assessment",
            "tags": "creditworthiness,assessment,evaluation"
        },
        {
            "title": "Document Everything",
            "content": "Maintain detailed records of all lending transactions, communications, and payments. Proper documentation protects both lender and borrower in case of disputes.",
            "category": "Legal Protection",
            "tags": "documentation,legal,records"
        },
        {
            "title": "Red Flags to Watch For",
            "content": "Be cautious of: reluctance to provide information, inconsistent income sources, multiple recent loan applications, or pressure to lend quickly. These may indicate higher risk.",
            "category": "Risk Management",
            "tags": "red-flags,warning-signs,fraud-prevention"
        },
        {
            "title": "Know Your Local Lending Laws",
            "content": "Lending regulations vary by location. Familiarize yourself with maximum interest rates (usury laws), required disclosures, and collection practices in your jurisdiction.",
            "category": "Legal Compliance",
            "tags": "legal,regulations,compliance"
        }
    ]

    SAFETY_TIPS = [
        {
            "title": "Never Share Banking Passwords",
            "content": "Never give anyone your banking passwords, PIN codes, or full account numbers. Legitimate borrowers don't need this information. Protect your financial accounts at all times.",
            "category": "Security",
            "tags": "security,passwords,safety"
        },
        {
            "title": "Meet in Public Places",
            "content": "When meeting borrowers for the first time, choose public locations like cafes or bank lobbies. Never meet at your home or isolated locations for safety.",
            "category": "Personal Safety",
            "tags": "safety,meetings,security"
        },
        {
            "title": "Verify Identity Documents",
            "content": "Always verify government-issued ID documents. Cross-check photo, name, and other details. Consider using identity verification services for added security.",
            "category": "Verification",
            "tags": "identity,verification,fraud-prevention"
        },
        {
            "title": "Trust Your Instincts",
            "content": "If something feels wrong or too good to be true, it probably is. Don't let pressure or urgency override your judgment. It's okay to say no to a lending opportunity.",
            "category": "Safety",
            "tags": "intuition,safety,decision-making"
        }
    ]

    @staticmethod
    def get_random_educational_tip() -> dict:
        """Get a random educational tip."""
        import random
        return random.choice(EducationalContentTemplates.LENDING_TIPS)

    @staticmethod
    def get_random_safety_tip() -> dict:
        """Get a random safety tip."""
        import random
        return random.choice(EducationalContentTemplates.SAFETY_TIPS)
