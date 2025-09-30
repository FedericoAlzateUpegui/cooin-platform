from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_active_user, get_database
from app.models.user import User
from app.schemas.search import (
    SearchRequest, SearchResponse, SavedSearchCreate, SavedSearchUpdate,
    SavedSearchResponse, SearchSuggestionsResponse, SearchType, SortBy, SortOrder
)
from app.services.search_service import SearchService

router = APIRouter()


@router.post("/", response_model=SearchResponse)
async def search_users(
    search_request: SearchRequest,
    request: Request,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """
    Search for users based on specified criteria.
    Supports filtering by location, financial criteria, ratings, and more.
    """
    # Extract request metadata for logging
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("User-Agent")

    return SearchService.search_users(
        db=db,
        search_request=search_request,
        current_user_id=current_user.id,
        ip_address=ip_address,
        user_agent=user_agent
    )


@router.get("/quick", response_model=SearchResponse)
async def quick_search(
    search_type: SearchType = Query(SearchType.ALL_USERS, description="Type of users to search for"),
    query: Optional[str] = Query(None, description="Search query text"),
    country: Optional[str] = Query(None, description="Country filter"),
    min_rating: Optional[float] = Query(None, ge=1.0, le=5.0, description="Minimum rating"),
    verified_only: bool = Query(False, description="Show only verified users"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=50, description="Items per page"),
    sort_by: SortBy = Query(SortBy.RELEVANCE, description="Sort criteria"),
    request: Request = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """
    Quick search endpoint with common filters as query parameters.
    Useful for simple searches and mobile apps.
    """
    from app.schemas.search import SearchFilters

    # Build search filters
    filters = SearchFilters()
    if country:
        filters.country = country
    if min_rating:
        filters.min_rating = min_rating
    if verified_only:
        filters.identity_verified = True

    # Create search request
    search_request = SearchRequest(
        search_type=search_type,
        query=query,
        filters=filters,
        page=page,
        page_size=page_size,
        sort_by=sort_by
    )

    # Extract request metadata
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("User-Agent")

    return SearchService.search_users(
        db=db,
        search_request=search_request,
        current_user_id=current_user.id,
        ip_address=ip_address,
        user_agent=user_agent
    )


@router.get("/suggestions", response_model=SearchSuggestionsResponse)
async def get_search_suggestions(
    query: str = Query(..., min_length=2, max_length=100, description="Search query for suggestions"),
    suggestion_type: Optional[str] = Query(None, description="Type of suggestions (location, employment, etc.)"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Get autocomplete suggestions for search queries."""
    return SearchService.get_search_suggestions(
        db=db,
        query=query,
        suggestion_type=suggestion_type
    )


# Saved Searches endpoints

@router.post("/saved", response_model=SavedSearchResponse, status_code=status.HTTP_201_CREATED)
async def create_saved_search(
    saved_search_data: SavedSearchCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Create a new saved search."""
    saved_search = SearchService.create_saved_search(
        db=db,
        user_id=current_user.id,
        saved_search_data=saved_search_data
    )

    return SavedSearchResponse(
        id=saved_search.id,
        name=saved_search.name,
        description=saved_search.description,
        search_request=SearchRequest(**saved_search.search_parameters),
        notify_on_new_matches=saved_search.notify_on_new_matches,
        is_active=saved_search.is_active,
        created_at=saved_search.created_at.isoformat(),
        updated_at=saved_search.updated_at.isoformat(),
        last_run_at=saved_search.last_run_at.isoformat() if saved_search.last_run_at else None,
        match_count=saved_search.match_count
    )


@router.get("/saved", response_model=List[SavedSearchResponse])
async def get_saved_searches(
    active_only: bool = Query(True, description="Return only active saved searches"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Get all saved searches for the current user."""
    saved_searches = SearchService.get_user_saved_searches(
        db=db,
        user_id=current_user.id,
        active_only=active_only
    )

    return [
        SavedSearchResponse(
            id=ss.id,
            name=ss.name,
            description=ss.description,
            search_request=SearchRequest(**ss.search_parameters),
            notify_on_new_matches=ss.notify_on_new_matches,
            is_active=ss.is_active,
            created_at=ss.created_at.isoformat(),
            updated_at=ss.updated_at.isoformat(),
            last_run_at=ss.last_run_at.isoformat() if ss.last_run_at else None,
            match_count=ss.match_count
        )
        for ss in saved_searches
    ]


@router.get("/saved/{saved_search_id}", response_model=SavedSearchResponse)
async def get_saved_search(
    saved_search_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Get a specific saved search."""
    saved_searches = SearchService.get_user_saved_searches(
        db=db,
        user_id=current_user.id,
        active_only=False
    )

    saved_search = next((ss for ss in saved_searches if ss.id == saved_search_id), None)
    if not saved_search:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Saved search not found"
        )

    return SavedSearchResponse(
        id=saved_search.id,
        name=saved_search.name,
        description=saved_search.description,
        search_request=SearchRequest(**saved_search.search_parameters),
        notify_on_new_matches=saved_search.notify_on_new_matches,
        is_active=saved_search.is_active,
        created_at=saved_search.created_at.isoformat(),
        updated_at=saved_search.updated_at.isoformat(),
        last_run_at=saved_search.last_run_at.isoformat() if saved_search.last_run_at else None,
        match_count=saved_search.match_count
    )


@router.put("/saved/{saved_search_id}", response_model=SavedSearchResponse)
async def update_saved_search(
    saved_search_id: int,
    update_data: SavedSearchUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Update a saved search."""
    saved_search = SearchService.update_saved_search(
        db=db,
        saved_search_id=saved_search_id,
        user_id=current_user.id,
        update_data=update_data
    )

    if not saved_search:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Saved search not found"
        )

    return SavedSearchResponse(
        id=saved_search.id,
        name=saved_search.name,
        description=saved_search.description,
        search_request=SearchRequest(**saved_search.search_parameters),
        notify_on_new_matches=saved_search.notify_on_new_matches,
        is_active=saved_search.is_active,
        created_at=saved_search.created_at.isoformat(),
        updated_at=saved_search.updated_at.isoformat(),
        last_run_at=saved_search.last_run_at.isoformat() if saved_search.last_run_at else None,
        match_count=saved_search.match_count
    )


@router.delete("/saved/{saved_search_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_saved_search(
    saved_search_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Delete a saved search."""
    success = SearchService.delete_saved_search(
        db=db,
        saved_search_id=saved_search_id,
        user_id=current_user.id
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Saved search not found"
        )


@router.post("/saved/{saved_search_id}/run", response_model=SearchResponse)
async def run_saved_search(
    saved_search_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """Run a saved search and get current results."""
    results = SearchService.run_saved_search(
        db=db,
        saved_search_id=saved_search_id,
        user_id=current_user.id
    )

    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Saved search not found or inactive"
        )

    return results


# Enhanced search endpoints for loans and lending offers

@router.get("/loan-requests")
async def search_loan_requests(
    q: Optional[str] = Query(None, description="Search query"),
    min_amount: Optional[float] = Query(None, description="Minimum loan amount"),
    max_amount: Optional[float] = Query(None, description="Maximum loan amount"),
    min_rate: Optional[float] = Query(None, description="Minimum interest rate"),
    max_rate: Optional[float] = Query(None, description="Maximum interest rate"),
    min_term: Optional[int] = Query(None, description="Minimum term in months"),
    max_term: Optional[int] = Query(None, description="Maximum term in months"),
    purpose: Optional[str] = Query(None, description="Loan purpose"),
    country: Optional[str] = Query(None, description="Country filter"),
    state: Optional[str] = Query(None, description="State/Province filter"),
    city: Optional[str] = Query(None, description="City filter"),
    verified_only: bool = Query(False, description="Only verified users"),
    sort_by: str = Query("created_date", regex="^(created_date|amount|rate|term|rating)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """
    Search loan requests with advanced filtering.
    Returns paginated loan requests with detailed filtering options.
    """
    try:
        from app.models.loan import LoanRequest
        from sqlalchemy import or_

        # Build base query
        query = db.query(LoanRequest).join(User).filter(
            LoanRequest.status == "active"
        )

        # Apply text search
        if q:
            query = query.filter(
                or_(
                    LoanRequest.purpose.ilike(f"%{q}%"),
                    LoanRequest.description.ilike(f"%{q}%"),
                    User.username.ilike(f"%{q}%")
                )
            )

        # Apply filters
        if min_amount is not None:
            query = query.filter(LoanRequest.amount >= min_amount)
        if max_amount is not None:
            query = query.filter(LoanRequest.amount <= max_amount)
        if min_rate is not None:
            query = query.filter(LoanRequest.max_interest_rate >= min_rate)
        if max_rate is not None:
            query = query.filter(LoanRequest.max_interest_rate <= max_rate)
        if min_term is not None:
            query = query.filter(LoanRequest.term_months >= min_term)
        if max_term is not None:
            query = query.filter(LoanRequest.term_months <= max_term)
        if purpose:
            query = query.filter(LoanRequest.purpose.ilike(f"%{purpose}%"))
        if verified_only:
            query = query.filter(User.is_verified == True)

        # Get total count
        total_count = query.count()

        # Apply sorting
        if sort_by == "amount":
            order_col = LoanRequest.amount
        elif sort_by == "rate":
            order_col = LoanRequest.max_interest_rate
        elif sort_by == "term":
            order_col = LoanRequest.term_months
        elif sort_by == "rating":
            order_col = User.average_rating
        else:  # created_date
            order_col = LoanRequest.created_at

        if sort_order == "asc":
            query = query.order_by(order_col.asc())
        else:
            query = query.order_by(order_col.desc())

        # Apply pagination
        offset = (page - 1) * page_size
        loan_requests = query.offset(offset).limit(page_size).all()

        # Format results
        results = []
        for lr in loan_requests:
            result = {
                "id": lr.id,
                "amount": lr.amount,
                "purpose": lr.purpose,
                "description": lr.description,
                "max_interest_rate": lr.max_interest_rate,
                "term_months": lr.term_months,
                "created_at": lr.created_at.isoformat(),
                "borrower": {
                    "id": lr.borrower.id,
                    "username": lr.borrower.username,
                    "rating": lr.borrower.average_rating or 0.0,
                    "verified": lr.borrower.is_verified
                }
            }
            results.append(result)

        # Calculate pagination
        total_pages = (total_count + page_size - 1) // page_size

        return {
            "success": True,
            "data": {
                "results": results,
                "total_count": total_count,
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_previous": page > 1
            },
            "message": f"Found {total_count} loan requests"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search loan requests"
        )


@router.get("/lending-offers")
async def search_lending_offers(
    q: Optional[str] = Query(None, description="Search query"),
    min_amount: Optional[float] = Query(None, description="Minimum loan amount"),
    max_amount: Optional[float] = Query(None, description="Maximum loan amount"),
    min_rate: Optional[float] = Query(None, description="Minimum interest rate"),
    max_rate: Optional[float] = Query(None, description="Maximum interest rate"),
    min_term: Optional[int] = Query(None, description="Minimum term in months"),
    max_term: Optional[int] = Query(None, description="Maximum term in months"),
    country: Optional[str] = Query(None, description="Country filter"),
    state: Optional[str] = Query(None, description="State/Province filter"),
    city: Optional[str] = Query(None, description="City filter"),
    verified_only: bool = Query(False, description="Only verified users"),
    sort_by: str = Query("created_date", regex="^(created_date|amount|rate|term|rating)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """
    Search lending offers with advanced filtering.
    Returns paginated lending offers with detailed filtering options.
    """
    try:
        from app.models.loan import LendingOffer
        from sqlalchemy import or_

        # Build base query
        query = db.query(LendingOffer).join(User).filter(
            LendingOffer.status == "active"
        )

        # Apply text search
        if q:
            query = query.filter(
                or_(
                    LendingOffer.description.ilike(f"%{q}%"),
                    User.username.ilike(f"%{q}%")
                )
            )

        # Apply filters
        if min_amount is not None:
            query = query.filter(LendingOffer.max_amount >= min_amount)
        if max_amount is not None:
            query = query.filter(LendingOffer.min_amount <= max_amount)
        if min_rate is not None:
            query = query.filter(LendingOffer.min_interest_rate >= min_rate)
        if max_rate is not None:
            query = query.filter(LendingOffer.min_interest_rate <= max_rate)
        if min_term is not None:
            query = query.filter(LendingOffer.max_term >= min_term)
        if max_term is not None:
            query = query.filter(LendingOffer.min_term <= max_term)
        if verified_only:
            query = query.filter(User.is_verified == True)

        # Get total count
        total_count = query.count()

        # Apply sorting
        if sort_by == "amount":
            order_col = LendingOffer.max_amount
        elif sort_by == "rate":
            order_col = LendingOffer.min_interest_rate
        elif sort_by == "term":
            order_col = LendingOffer.max_term
        elif sort_by == "rating":
            order_col = User.average_rating
        else:  # created_date
            order_col = LendingOffer.created_at

        if sort_order == "asc":
            query = query.order_by(order_col.asc())
        else:
            query = query.order_by(order_col.desc())

        # Apply pagination
        offset = (page - 1) * page_size
        lending_offers = query.offset(offset).limit(page_size).all()

        # Format results
        results = []
        for lo in lending_offers:
            result = {
                "id": lo.id,
                "min_amount": lo.min_amount,
                "max_amount": lo.max_amount,
                "min_interest_rate": lo.min_interest_rate,
                "min_term": lo.min_term,
                "max_term": lo.max_term,
                "description": lo.description,
                "created_at": lo.created_at.isoformat(),
                "lender": {
                    "id": lo.lender.id,
                    "username": lo.lender.username,
                    "rating": lo.lender.average_rating or 0.0,
                    "verified": lo.lender.is_verified
                }
            }
            results.append(result)

        # Calculate pagination
        total_pages = (total_count + page_size - 1) // page_size

        return {
            "success": True,
            "data": {
                "results": results,
                "total_count": total_count,
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_previous": page > 1
            },
            "message": f"Found {total_count} lending offers"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search lending offers"
        )