import time
from typing import Optional, List, Tuple, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc, asc, text, case
from datetime import datetime, timedelta
import json

from app.models.user import User
from app.models.profile import UserProfile
from app.models.search import SavedSearch, SearchLog
from app.schemas.search import (
    SearchRequest, SearchFilters, SearchResponse, UserSearchResult,
    SearchStats, SavedSearchCreate, SavedSearchUpdate, SavedSearchResponse,
    SearchSuggestion, SearchSuggestionsResponse, SearchType, SortBy, SortOrder
)


class SearchService:
    """Service for user search and discovery functionality."""

    @staticmethod
    def search_users(
        db: Session,
        search_request: SearchRequest,
        current_user_id: Optional[int] = None,
        log_search: bool = True,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> SearchResponse:
        """
        Search for users based on criteria.
        """
        start_time = time.time()

        # Build the base query
        query = db.query(User, UserProfile).join(UserProfile, User.id == UserProfile.user_id)

        # Exclude current user from results
        if current_user_id:
            query = query.filter(User.id != current_user_id)

        # Apply filters
        query = SearchService._apply_filters(query, search_request)

        # Apply text search
        if search_request.query:
            query = SearchService._apply_text_search(query, search_request.query)

        # Get total count before pagination
        total_count = query.count()

        # Apply sorting
        query = SearchService._apply_sorting(query, search_request.sort_by, search_request.sort_order)

        # Apply pagination
        offset = (search_request.page - 1) * search_request.page_size
        results = query.offset(offset).limit(search_request.page_size).all()

        # Convert to response format
        user_results = []
        for user, profile in results:
            user_result = SearchService._convert_to_search_result(user, profile)
            user_results.append(user_result)

        # Calculate pagination info
        total_pages = (total_count + search_request.page_size - 1) // search_request.page_size
        has_next = search_request.page < total_pages
        has_previous = search_request.page > 1

        # Generate statistics
        stats = SearchService._generate_search_stats(db, search_request)

        # Calculate execution time
        execution_time = (time.time() - start_time) * 1000

        # Log the search
        if log_search:
            SearchService._log_search(
                db, search_request, total_count, current_user_id,
                execution_time, ip_address, user_agent
            )

        return SearchResponse(
            results=user_results,
            total_count=total_count,
            page=search_request.page,
            page_size=search_request.page_size,
            total_pages=total_pages,
            has_next=has_next,
            has_previous=has_previous,
            search_type=search_request.search_type,
            query=search_request.query,
            filters_applied=SearchService._count_applied_filters(search_request.filters),
            search_time_ms=execution_time,
            stats=stats
        )

    @staticmethod
    def _apply_filters(query, search_request: SearchRequest):
        """Apply search filters to the query."""
        if not search_request.filters:
            return query

        filters = search_request.filters

        # Role-based filtering
        if search_request.search_type == SearchType.LENDERS:
            query = query.filter(or_(User.role == "LENDER", User.role == "BOTH"))
        elif search_request.search_type == SearchType.BORROWERS:
            query = query.filter(or_(User.role == "BORROWER", User.role == "BOTH"))

        # Location filters
        if filters.country:
            query = query.filter(UserProfile.country == filters.country)
        if filters.state_province:
            query = query.filter(UserProfile.state_province == filters.state_province)
        if filters.city:
            query = query.filter(UserProfile.city == filters.city)

        # Financial filters
        if filters.min_loan_amount is not None:
            query = query.filter(
                or_(
                    UserProfile.min_loan_amount >= filters.min_loan_amount,
                    UserProfile.max_loan_amount >= filters.min_loan_amount
                )
            )
        if filters.max_loan_amount is not None:
            query = query.filter(
                or_(
                    UserProfile.min_loan_amount <= filters.max_loan_amount,
                    UserProfile.max_loan_amount <= filters.max_loan_amount
                )
            )

        if filters.min_interest_rate is not None:
            query = query.filter(UserProfile.preferred_interest_rate >= filters.min_interest_rate)
        if filters.max_interest_rate is not None:
            query = query.filter(UserProfile.preferred_interest_rate <= filters.max_interest_rate)

        if filters.loan_term_min is not None:
            query = query.filter(UserProfile.preferred_loan_term_min >= filters.loan_term_min)
        if filters.loan_term_max is not None:
            query = query.filter(UserProfile.preferred_loan_term_max <= filters.loan_term_max)

        # User criteria filters
        if filters.min_credit_score is not None:
            query = query.filter(UserProfile.credit_score >= filters.min_credit_score)
        if filters.max_credit_score is not None:
            query = query.filter(UserProfile.credit_score <= filters.max_credit_score)

        if filters.employment_status:
            query = query.filter(UserProfile.employment_status.in_(filters.employment_status))
        if filters.income_range:
            query = query.filter(UserProfile.income_range.in_(filters.income_range))

        if filters.min_years_employed is not None:
            query = query.filter(UserProfile.years_employed >= filters.min_years_employed)

        # Rating and trust filters
        if filters.min_rating is not None:
            query = query.filter(User.average_rating >= filters.min_rating)
        if filters.min_rating_count is not None:
            query = query.filter(User.total_ratings >= filters.min_rating_count)

        if filters.identity_verified is not None:
            query = query.filter(UserProfile.identity_verified == filters.identity_verified)
        if filters.income_verified is not None:
            query = query.filter(UserProfile.income_verified == filters.income_verified)
        if filters.bank_account_verified is not None:
            query = query.filter(UserProfile.bank_account_verified == filters.bank_account_verified)

        # Activity filters
        if filters.recently_active:
            recent_threshold = datetime.utcnow() - timedelta(days=7)
            query = query.filter(User.last_login >= recent_threshold)

        if filters.has_profile_picture:
            query = query.filter(UserProfile.avatar_url.isnot(None))

        if filters.profile_completion_min is not None:
            query = query.filter(UserProfile.profile_completion_percentage >= filters.profile_completion_min)

        return query

    @staticmethod
    def _apply_text_search(query, search_text: str):
        """Apply text search across relevant fields."""
        search_term = f"%{search_text.lower()}%"

        return query.filter(
            or_(
                func.lower(User.username).like(search_term),
                func.lower(UserProfile.display_name).like(search_term),
                func.lower(UserProfile.bio).like(search_term),
                func.lower(UserProfile.city).like(search_term),
                func.lower(UserProfile.state_province).like(search_term),
                func.lower(UserProfile.country).like(search_term),
                func.lower(UserProfile.loan_purpose).like(search_term),
                func.lower(UserProfile.employer_name).like(search_term)
            )
        )

    @staticmethod
    def _apply_sorting(query, sort_by: SortBy, sort_order: SortOrder):
        """Apply sorting to the query."""
        order_func = desc if sort_order == SortOrder.DESC else asc

        if sort_by == SortBy.RATING:
            query = query.order_by(order_func(User.average_rating), order_func(User.total_ratings))
        elif sort_by == SortBy.CREATED_AT:
            query = query.order_by(order_func(User.created_at))
        elif sort_by == SortBy.LAST_ACTIVE:
            query = query.order_by(order_func(User.last_login))
        elif sort_by == SortBy.LOAN_AMOUNT:
            query = query.order_by(order_func(UserProfile.max_loan_amount))
        elif sort_by == SortBy.INTEREST_RATE:
            query = query.order_by(order_func(UserProfile.preferred_interest_rate))
        else:  # RELEVANCE - default sorting
            query = query.order_by(
                order_func(User.average_rating),
                order_func(UserProfile.profile_completion_percentage),
                order_func(User.last_login)
            )

        return query

    @staticmethod
    def _convert_to_search_result(user: User, profile: UserProfile) -> UserSearchResult:
        """Convert database models to search result format."""

        # Calculate days since last login
        days_since_login = None
        is_recently_active = False
        if user.last_login:
            days_since_login = (datetime.utcnow() - user.last_login).days
            is_recently_active = days_since_login <= 7

        return UserSearchResult(
            id=user.id,
            username=user.username,
            role=user.role.value,
            created_at=user.created_at.isoformat(),
            last_login=user.last_login.isoformat() if user.last_login else None,
            display_name=profile.display_name,
            bio=profile.bio,
            country=profile.country if profile.show_location else None,
            state_province=profile.state_province if profile.show_location else None,
            city=profile.city if profile.show_location else None,
            min_loan_amount=profile.min_loan_amount,
            max_loan_amount=profile.max_loan_amount,
            preferred_interest_rate=profile.preferred_interest_rate,
            willing_to_lend_unsecured=profile.willing_to_lend_unsecured,
            average_rating=user.average_rating or 0.0,
            total_ratings=user.total_ratings or 0,
            identity_verified=profile.identity_verified,
            income_verified=profile.income_verified,
            bank_account_verified=profile.bank_account_verified,
            profile_completion_percentage=profile.profile_completion_percentage,
            is_recently_active=is_recently_active,
            days_since_last_login=days_since_login
        )

    @staticmethod
    def _generate_search_stats(db: Session, search_request: SearchRequest) -> SearchStats:
        """Generate search statistics."""
        # Get total user counts
        base_query = db.query(User).join(UserProfile)

        total_users = base_query.count()
        lenders_count = base_query.filter(or_(User.role == "LENDER", User.role == "BOTH")).count()
        borrowers_count = base_query.filter(or_(User.role == "BORROWER", User.role == "BOTH")).count()
        both_role_count = base_query.filter(User.role == "BOTH").count()
        verified_users = base_query.filter(UserProfile.identity_verified == True).count()

        # Calculate average rating
        avg_rating_result = base_query.with_entities(func.avg(User.average_rating)).scalar()
        average_rating = float(avg_rating_result) if avg_rating_result else 0.0

        return SearchStats(
            total_users=total_users,
            lenders_count=lenders_count,
            borrowers_count=borrowers_count,
            both_role_count=both_role_count,
            verified_users=verified_users,
            average_rating=round(average_rating, 2)
        )

    @staticmethod
    def _count_applied_filters(filters: Optional[SearchFilters]) -> int:
        """Count how many filters are applied."""
        if not filters:
            return 0

        count = 0
        filter_dict = filters.dict(exclude_unset=True)
        for key, value in filter_dict.items():
            if value is not None:
                if isinstance(value, list) and len(value) > 0:
                    count += 1
                elif not isinstance(value, list):
                    count += 1

        return count

    @staticmethod
    def _log_search(
        db: Session,
        search_request: SearchRequest,
        result_count: int,
        user_id: Optional[int],
        execution_time: float,
        ip_address: Optional[str],
        user_agent: Optional[str]
    ):
        """Log search for analytics."""
        try:
            search_log = SearchLog(
                user_id=user_id,
                search_type=search_request.search_type.value,
                query=search_request.query,
                filters_used=search_request.filters.dict(exclude_unset=True) if search_request.filters else None,
                result_count=result_count,
                page=search_request.page,
                page_size=search_request.page_size,
                execution_time_ms=execution_time,
                ip_address=ip_address,
                user_agent=user_agent
            )
            db.add(search_log)
            db.commit()
        except Exception:
            # Don't let logging errors affect search functionality
            db.rollback()

    # Saved Searches functionality

    @staticmethod
    def create_saved_search(
        db: Session,
        user_id: int,
        saved_search_data: SavedSearchCreate
    ) -> SavedSearch:
        """Create a new saved search for a user."""
        saved_search = SavedSearch(
            user_id=user_id,
            name=saved_search_data.name,
            description=saved_search_data.description,
            search_parameters=saved_search_data.search_request.dict(),
            notify_on_new_matches=saved_search_data.notify_on_new_matches
        )

        db.add(saved_search)
        db.commit()
        db.refresh(saved_search)

        return saved_search

    @staticmethod
    def get_user_saved_searches(
        db: Session,
        user_id: int,
        active_only: bool = True
    ) -> List[SavedSearch]:
        """Get all saved searches for a user."""
        query = db.query(SavedSearch).filter(SavedSearch.user_id == user_id)

        if active_only:
            query = query.filter(SavedSearch.is_active == True)

        return query.order_by(desc(SavedSearch.created_at)).all()

    @staticmethod
    def update_saved_search(
        db: Session,
        saved_search_id: int,
        user_id: int,
        update_data: SavedSearchUpdate
    ) -> Optional[SavedSearch]:
        """Update a saved search."""
        saved_search = db.query(SavedSearch).filter(
            SavedSearch.id == saved_search_id,
            SavedSearch.user_id == user_id
        ).first()

        if not saved_search:
            return None

        # Update fields
        for field, value in update_data.dict(exclude_unset=True).items():
            if field == "search_request":
                # Convert SearchRequest to dict
                setattr(saved_search, "search_parameters", value.dict())
            else:
                setattr(saved_search, field, value)

        saved_search.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(saved_search)

        return saved_search

    @staticmethod
    def delete_saved_search(
        db: Session,
        saved_search_id: int,
        user_id: int
    ) -> bool:
        """Delete a saved search."""
        saved_search = db.query(SavedSearch).filter(
            SavedSearch.id == saved_search_id,
            SavedSearch.user_id == user_id
        ).first()

        if not saved_search:
            return False

        db.delete(saved_search)
        db.commit()
        return True

    @staticmethod
    def run_saved_search(
        db: Session,
        saved_search_id: int,
        user_id: int
    ) -> Optional[SearchResponse]:
        """Run a saved search and return results."""
        saved_search = db.query(SavedSearch).filter(
            SavedSearch.id == saved_search_id,
            SavedSearch.user_id == user_id,
            SavedSearch.is_active == True
        ).first()

        if not saved_search:
            return None

        # Convert stored parameters back to SearchRequest
        try:
            search_request = SearchRequest(**saved_search.search_parameters)
        except Exception:
            return None

        # Run the search
        results = SearchService.search_users(
            db, search_request, current_user_id=user_id, log_search=False
        )

        # Update the saved search with new match count and last run time
        saved_search.update_match_count(results.total_count)
        db.commit()

        return results

    @staticmethod
    def get_search_suggestions(
        db: Session,
        query: str,
        suggestion_type: Optional[str] = None
    ) -> SearchSuggestionsResponse:
        """Get search suggestions for autocomplete."""
        suggestions = []

        if not query or len(query) < 2:
            return SearchSuggestionsResponse(query=query, suggestions=suggestions)

        query_like = f"%{query.lower()}%"

        # Location suggestions
        if not suggestion_type or suggestion_type == "location":
            # Cities
            city_results = db.query(
                UserProfile.city,
                func.count(UserProfile.city).label('count')
            ).filter(
                func.lower(UserProfile.city).like(query_like),
                UserProfile.city.isnot(None)
            ).group_by(UserProfile.city).order_by(desc('count')).limit(5).all()

            for city, count in city_results:
                suggestions.append(SearchSuggestion(type="city", value=city, count=count))

            # States/Provinces
            state_results = db.query(
                UserProfile.state_province,
                func.count(UserProfile.state_province).label('count')
            ).filter(
                func.lower(UserProfile.state_province).like(query_like),
                UserProfile.state_province.isnot(None)
            ).group_by(UserProfile.state_province).order_by(desc('count')).limit(3).all()

            for state, count in state_results:
                suggestions.append(SearchSuggestion(type="state", value=state, count=count))

        # Industry/Employment suggestions
        if not suggestion_type or suggestion_type == "employment":
            employer_results = db.query(
                UserProfile.employer_name,
                func.count(UserProfile.employer_name).label('count')
            ).filter(
                func.lower(UserProfile.employer_name).like(query_like),
                UserProfile.employer_name.isnot(None)
            ).group_by(UserProfile.employer_name).order_by(desc('count')).limit(3).all()

            for employer, count in employer_results:
                suggestions.append(SearchSuggestion(type="employer", value=employer, count=count))

        return SearchSuggestionsResponse(query=query, suggestions=suggestions)