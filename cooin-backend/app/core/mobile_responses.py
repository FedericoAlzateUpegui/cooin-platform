"""
Mobile-optimized response formatters for iOS app integration.
Standardizes all API responses for consistent mobile consumption.
"""

import time
import uuid
from typing import Any, Dict, List, Optional
from datetime import datetime
from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.config import settings


class MobileResponseFormatter:
    """Formats API responses for optimal mobile app consumption."""

    @staticmethod
    def success(
        data: Any = None,
        message: str = "Success",
        meta: Optional[Dict[str, Any]] = None,
        request: Optional[Request] = None
    ) -> Dict[str, Any]:
        """Format successful response for mobile apps."""

        response = {
            "success": True,
            "message": message,
            "data": data,
            "meta": {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "request_id": str(uuid.uuid4()),
                "server_time": int(time.time()),
                "api_version": "1.0.0"
            }
        }

        # Add request-specific metadata
        if request:
            response["meta"].update({
                "app_version": request.headers.get("X-App-Version"),
                "device_id": request.headers.get("X-Device-ID"),
                "ios_version": request.headers.get("X-iOS-Version"),
                "device_model": request.headers.get("X-Device-Model")
            })

        # Add custom metadata
        if meta:
            response["meta"].update(meta)

        return response

    @staticmethod
    def error(
        error_code: str,
        detail: str,
        status_code: int = 400,
        field_errors: Optional[List[Dict[str, Any]]] = None,
        meta: Optional[Dict[str, Any]] = None,
        request: Optional[Request] = None
    ) -> Dict[str, Any]:
        """Format error response for mobile apps."""

        response = {
            "success": False,
            "error_code": error_code,
            "detail": detail,
            "status_code": status_code,
            "meta": {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "request_id": str(uuid.uuid4()),
                "server_time": int(time.time()),
                "api_version": "1.0.0"
            }
        }

        # Add field errors for validation failures
        if field_errors:
            response["field_errors"] = field_errors

        # Add request-specific metadata
        if request:
            response["meta"].update({
                "app_version": request.headers.get("X-App-Version"),
                "device_id": request.headers.get("X-Device-ID")
            })

        # Add custom metadata
        if meta:
            response["meta"].update(meta)

        return response

    @staticmethod
    def paginated(
        data: List[Any],
        total: int,
        page: int,
        limit: int,
        message: str = "Data retrieved successfully",
        meta: Optional[Dict[str, Any]] = None,
        request: Optional[Request] = None
    ) -> Dict[str, Any]:
        """Format paginated response for mobile apps."""

        total_pages = (total + limit - 1) // limit if total > 0 else 1
        has_next = page < total_pages
        has_previous = page > 1

        pagination_meta = {
            "pagination": {
                "total": total,
                "page": page,
                "limit": limit,
                "total_pages": total_pages,
                "has_next": has_next,
                "has_previous": has_previous,
                "next_page": page + 1 if has_next else None,
                "previous_page": page - 1 if has_previous else None
            }
        }

        if meta:
            pagination_meta.update(meta)

        return MobileResponseFormatter.success(
            data=data,
            message=message,
            meta=pagination_meta,
            request=request
        )


class MobileJSONResponse(JSONResponse):
    """Custom JSON response class for mobile apps."""

    def __init__(
        self,
        content: Any = None,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
        media_type: Optional[str] = None,
        background=None,
        mobile_formatted: bool = False
    ):
        # Add mobile-specific headers
        mobile_headers = {
            "X-API-Version": "1.0.0",
            "X-Response-Time": str(int(time.time() * 1000)),  # milliseconds
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }

        if headers:
            mobile_headers.update(headers)

        super().__init__(
            content=content,
            status_code=status_code,
            headers=mobile_headers,
            media_type=media_type,
            background=background
        )


def format_user_for_mobile(user: Any, include_sensitive: bool = False) -> Dict[str, Any]:
    """Format user data for mobile app consumption."""

    user_data = {
        "id": user.id,
        "email": user.email if include_sensitive else None,
        "username": user.username,
        "role": user.role.value if hasattr(user.role, 'value') else user.role,
        "is_active": user.is_active,
        "is_verified": user.is_verified,
        "created_at": user.created_at.isoformat() + "Z" if user.created_at else None,
        "last_login": user.last_login.isoformat() + "Z" if user.last_login else None
    }

    # Remove None values for cleaner mobile responses
    return {k: v for k, v in user_data.items() if v is not None}


def format_profile_for_mobile(profile: Any, include_private: bool = False) -> Dict[str, Any]:
    """Format user profile data for mobile app consumption."""

    profile_data = {
        "id": profile.id,
        "user_id": profile.user_id,
        "display_name": profile.display_name,
        "bio": profile.bio,
        "avatar_url": profile.avatar_url,
        "banner_url": profile.banner_url,
        "country": profile.country if profile.show_location or include_private else None,
        "city": profile.city if profile.show_location or include_private else None,
        "income_range": profile.income_range if profile.show_income_range or include_private else None,
        "employment_status": profile.employment_status if profile.show_employment or include_private else None,
        "profile_completion_percentage": profile.profile_completion_percentage,
        "identity_verified": profile.identity_verified,
        "income_verified": profile.income_verified,
        "created_at": profile.created_at.isoformat() + "Z" if profile.created_at else None,
        "updated_at": profile.updated_at.isoformat() + "Z" if profile.updated_at else None
    }

    # Add private data if authorized
    if include_private:
        profile_data.update({
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "phone_number": profile.phone_number,
            "date_of_birth": profile.date_of_birth.isoformat() if profile.date_of_birth else None,
            "credit_score": profile.credit_score,
            "monthly_income": float(profile.monthly_income) if profile.monthly_income else None,
            "requested_loan_amount": float(profile.requested_loan_amount) if profile.requested_loan_amount else None,
            "loan_purpose": profile.loan_purpose,
            "max_acceptable_rate": float(profile.max_acceptable_rate) if profile.max_acceptable_rate else None
        })

    # Remove None values for cleaner mobile responses
    return {k: v for k, v in profile_data.items() if v is not None}


def format_connection_for_mobile(connection: Any) -> Dict[str, Any]:
    """Format connection data for mobile app consumption."""

    return {
        "id": connection.id,
        "requester_id": connection.requester_id,
        "requestee_id": connection.requestee_id,
        "status": connection.status.value if hasattr(connection.status, 'value') else connection.status,
        "message": connection.message,
        "proposed_loan_amount": float(connection.proposed_loan_amount) if connection.proposed_loan_amount else None,
        "proposed_interest_rate": float(connection.proposed_interest_rate) if connection.proposed_interest_rate else None,
        "proposed_term_months": connection.proposed_term_months,
        "created_at": connection.created_at.isoformat() + "Z" if connection.created_at else None,
        "updated_at": connection.updated_at.isoformat() + "Z" if connection.updated_at else None,
        "responded_at": connection.responded_at.isoformat() + "Z" if connection.responded_at else None
    }


def format_notification_for_mobile(notification: Any) -> Dict[str, Any]:
    """Format notification data for mobile app consumption."""

    return {
        "id": notification.id,
        "user_id": notification.user_id,
        "type": notification.type,
        "title": notification.title,
        "message": notification.message,
        "data": notification.data,
        "read": notification.read,
        "created_at": notification.created_at.isoformat() + "Z" if notification.created_at else None,
        "read_at": notification.read_at.isoformat() + "Z" if notification.read_at else None,
        "action_url": notification.action_url
    }