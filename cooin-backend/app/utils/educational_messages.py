"""
Utility module for sending educational messages to users.
Can be used manually or scheduled via background tasks.
"""

from sqlalchemy.orm import Session
from app.models.system_message import SystemMessageType, SystemMessagePriority
from app.services.system_message_service import SystemMessageService, EducationalContentTemplates
from app.models.user import User
import random


class EducationalMessageSender:
    """Helper class to send educational messages to users."""

    @staticmethod
    def send_welcome_message(db: Session, user_id: int):
        """Send welcome message to new user."""
        SystemMessageService.create_message(
            db=db,
            user_id=user_id,
            title="Welcome to Cooin!",
            content="Welcome to Cooin, your trusted platform for peer-to-peer lending. "
                   "We're here to help you make informed lending and borrowing decisions. "
                   "You'll receive educational tips about lending best practices, safety reminders, "
                   "and important platform updates. Let's get started!",
            message_type=SystemMessageType.ANNOUNCEMENT,
            priority=SystemMessagePriority.HIGH,
            category="Welcome",
            tags="welcome,onboarding"
        )

    @staticmethod
    def send_random_educational_tip(db: Session, user_id: int):
        """Send a random educational tip to a user."""
        tip = EducationalContentTemplates.get_random_educational_tip()

        SystemMessageService.create_message(
            db=db,
            user_id=user_id,
            title=tip["title"],
            content=tip["content"],
            message_type=SystemMessageType.EDUCATIONAL,
            priority=SystemMessagePriority.MEDIUM,
            category=tip.get("category"),
            tags=tip.get("tags")
        )

    @staticmethod
    def send_random_safety_tip(db: Session, user_id: int):
        """Send a random safety tip to a user."""
        tip = EducationalContentTemplates.get_random_safety_tip()

        SystemMessageService.create_message(
            db=db,
            user_id=user_id,
            title=tip["title"],
            content=tip["content"],
            message_type=SystemMessageType.SAFETY_TIP,
            priority=SystemMessagePriority.HIGH,
            category=tip.get("category"),
            tags=tip.get("tags")
        )

    @staticmethod
    def send_daily_tip_to_all_users(db: Session):
        """Send a daily educational tip to all active users."""
        # Get all active users
        users = db.query(User).filter(User.is_active == True).all()

        tip = EducationalContentTemplates.get_random_educational_tip()

        user_ids = [user.id for user in users]

        if user_ids:
            SystemMessageService.create_bulk_messages(
                db=db,
                user_ids=user_ids,
                title=tip["title"],
                content=tip["content"],
                message_type=SystemMessageType.EDUCATIONAL,
                priority=SystemMessagePriority.MEDIUM,
                category=tip.get("category"),
                tags=tip.get("tags")
            )

        return len(user_ids)

    @staticmethod
    def send_match_notification(db: Session, user_id: int, match_name: str, connection_id: int):
        """Send notification when user gets a new match."""
        SystemMessageService.create_message(
            db=db,
            user_id=user_id,
            title="You have a new match!",
            content=f"Great news! You matched with {match_name}. "
                   f"You can now view their profile and start connecting.",
            message_type=SystemMessageType.MATCH_NOTIFICATION,
            priority=SystemMessagePriority.HIGH,
            action_url=f"/connections/{connection_id}",
            action_label="View Match",
            category="Matches",
            tags="match,connection"
        )

    @staticmethod
    def send_connection_accepted_notification(db: Session, user_id: int, accepter_name: str, connection_id: int):
        """Send notification when connection request is accepted."""
        SystemMessageService.create_message(
            db=db,
            user_id=user_id,
            title="Connection Accepted!",
            content=f"{accepter_name} accepted your connection request. "
                   f"You can now view their full profile and connect.",
            message_type=SystemMessageType.MATCH_NOTIFICATION,
            priority=SystemMessagePriority.HIGH,
            action_url=f"/connections/{connection_id}",
            action_label="View Connection",
            category="Connections",
            tags="connection,accepted"
        )

    @staticmethod
    def send_profile_completion_reminder(db: Session, user_id: int):
        """Send reminder to complete profile."""
        SystemMessageService.create_message(
            db=db,
            user_id=user_id,
            title="Complete Your Profile",
            content="Complete your profile to increase your chances of finding the right lending "
                   "or borrowing matches. A complete profile builds trust and credibility.",
            message_type=SystemMessageType.REMINDER,
            priority=SystemMessagePriority.MEDIUM,
            action_url="/profile/setup",
            action_label="Complete Profile",
            category="Profile",
            tags="profile,reminder"
        )

    @staticmethod
    def send_feature_announcement(db: Session, title: str, content: str, action_url: str = None, action_label: str = None):
        """Send feature announcement to all active users."""
        users = db.query(User).filter(User.is_active == True).all()
        user_ids = [user.id for user in users]

        if user_ids:
            SystemMessageService.create_bulk_messages(
                db=db,
                user_ids=user_ids,
                title=title,
                content=content,
                message_type=SystemMessageType.FEATURE_UPDATE,
                priority=SystemMessagePriority.MEDIUM,
                action_url=action_url,
                action_label=action_label,
                category="Features",
                tags="announcement,features"
            )

        return len(user_ids)

    @staticmethod
    def send_security_alert(db: Session, user_id: int, alert_content: str):
        """Send urgent security alert to user."""
        SystemMessageService.create_message(
            db=db,
            user_id=user_id,
            title="Security Alert",
            content=alert_content,
            message_type=SystemMessageType.SAFETY_TIP,
            priority=SystemMessagePriority.URGENT,
            category="Security",
            tags="security,alert,urgent"
        )


# Example usage in background tasks or scheduled jobs
def send_weekly_educational_content(db: Session):
    """
    Send weekly educational content to all users.
    This can be scheduled to run once a week.
    """
    return EducationalMessageSender.send_daily_tip_to_all_users(db)


def send_onboarding_sequence(db: Session, user_id: int, day: int):
    """
    Send educational onboarding sequence over multiple days.

    Args:
        db: Database session
        user_id: User ID
        day: Day number in onboarding sequence (1-7)
    """
    if day == 1:
        EducationalMessageSender.send_welcome_message(db, user_id)
    elif day == 2:
        EducationalMessageSender.send_random_safety_tip(db, user_id)
    elif day == 3:
        EducationalMessageSender.send_random_educational_tip(db, user_id)
    elif day == 5:
        EducationalMessageSender.send_profile_completion_reminder(db, user_id)
    elif day == 7:
        EducationalMessageSender.send_random_educational_tip(db, user_id)
