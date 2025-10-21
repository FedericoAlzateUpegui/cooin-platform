"""
Intelligent matching algorithm for connecting borrowers and lenders.
Uses multiple factors to create optimal loan matches with scoring system.
"""

import logging
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from app.models import User, UserProfile, Rating, Connection
from app.core.config import settings
from app.services.cache_service import get_app_cache_service

logger = logging.getLogger(__name__)

# Placeholder types for models not yet implemented
class LoanRequest:
    """Placeholder for LoanRequest model - not yet implemented"""
    pass

class LendingOffer:
    """Placeholder for LendingOffer model - not yet implemented"""
    pass


class MatchingCriteria(Enum):
    """Criteria used for loan matching."""
    LOAN_AMOUNT = "loan_amount"
    INTEREST_RATE = "interest_rate"
    LOAN_TERM = "loan_term"
    CREDIT_SCORE = "credit_score"
    GEOGRAPHIC_PROXIMITY = "geographic_proximity"
    USER_RATING = "user_rating"
    PREVIOUS_HISTORY = "previous_history"
    RISK_TOLERANCE = "risk_tolerance"
    LOAN_PURPOSE = "loan_purpose"


@dataclass
class MatchScore:
    """Container for match scoring details."""
    total_score: float
    criteria_scores: Dict[str, float]
    confidence_level: str
    risk_assessment: str
    recommendation_strength: str


@dataclass
class LoanMatch:
    """Container for a loan match result."""
    borrower_id: int
    lender_id: int
    loan_request_id: int
    lending_offer_id: int
    match_score: MatchScore
    estimated_approval_probability: float
    suggested_terms: Dict[str, Any]
    match_reasons: List[str]


class IntelligentMatchingService:
    """Advanced matching service for loan requests and lending offers."""

    def __init__(self):
        self.cache = get_app_cache_service()
        self.min_match_score = 0.6  # Minimum score to consider a match
        self.max_matches_per_request = 10

        # Scoring weights for different criteria
        self.scoring_weights = {
            MatchingCriteria.LOAN_AMOUNT: 0.25,
            MatchingCriteria.INTEREST_RATE: 0.20,
            MatchingCriteria.LOAN_TERM: 0.15,
            MatchingCriteria.CREDIT_SCORE: 0.15,
            MatchingCriteria.USER_RATING: 0.10,
            MatchingCriteria.GEOGRAPHIC_PROXIMITY: 0.05,
            MatchingCriteria.PREVIOUS_HISTORY: 0.05,
            MatchingCriteria.RISK_TOLERANCE: 0.03,
            MatchingCriteria.LOAN_PURPOSE: 0.02
        }

    async def find_matches_for_borrower(
        self,
        loan_request_id: int,
        db: Session,
        limit: int = None
    ) -> List[LoanMatch]:
        """Find best lending offers for a loan request."""

        limit = limit or self.max_matches_per_request
        cache_key = f"borrower_matches:{loan_request_id}:{limit}"

        # Check cache first
        cached_matches = await self.cache.get(cache_key)
        if cached_matches:
            logger.info(f"Retrieved {len(cached_matches)} cached matches for borrower request {loan_request_id}")
            return cached_matches

        # Get loan request with borrower info
        loan_request = db.query(LoanRequest).filter(
            LoanRequest.id == loan_request_id,
            LoanRequest.status == "active"
        ).first()

        if not loan_request:
            logger.warning(f"Loan request {loan_request_id} not found or not active")
            return []

        # Get borrower profile and ratings
        borrower = db.query(User).join(UserProfile).filter(User.id == loan_request.borrower_id).first()
        borrower_rating = self._get_user_average_rating(loan_request.borrower_id, db)

        # Find potential lending offers
        potential_offers = self._get_compatible_lending_offers(loan_request, db)

        matches = []
        for offer in potential_offers:
            # Get lender info
            lender = db.query(User).join(UserProfile).filter(User.id == offer.lender_id).first()
            lender_rating = self._get_user_average_rating(offer.lender_id, db)

            # Calculate match score
            match_score = self._calculate_match_score(
                loan_request, offer, borrower, lender, borrower_rating, lender_rating, db
            )

            if match_score.total_score >= self.min_match_score:
                # Generate suggested terms and probability
                suggested_terms = self._generate_suggested_terms(loan_request, offer, match_score)
                approval_probability = self._estimate_approval_probability(match_score, borrower_rating, lender_rating)
                match_reasons = self._generate_match_reasons(match_score)

                loan_match = LoanMatch(
                    borrower_id=loan_request.borrower_id,
                    lender_id=offer.lender_id,
                    loan_request_id=loan_request_id,
                    lending_offer_id=offer.id,
                    match_score=match_score,
                    estimated_approval_probability=approval_probability,
                    suggested_terms=suggested_terms,
                    match_reasons=match_reasons
                )
                matches.append(loan_match)

        # Sort by total score and limit results
        matches.sort(key=lambda x: x.match_score.total_score, reverse=True)
        matches = matches[:limit]

        # Cache results for 30 minutes
        await self.cache.set(cache_key, matches, 1800)

        logger.info(f"Found {len(matches)} matches for borrower request {loan_request_id}")
        return matches

    async def find_matches_for_lender(
        self,
        lending_offer_id: int,
        db: Session,
        limit: int = None
    ) -> List[LoanMatch]:
        """Find best loan requests for a lending offer."""

        limit = limit or self.max_matches_per_request
        cache_key = f"lender_matches:{lending_offer_id}:{limit}"

        # Check cache first
        cached_matches = await self.cache.get(cache_key)
        if cached_matches:
            logger.info(f"Retrieved {len(cached_matches)} cached matches for lender offer {lending_offer_id}")
            return cached_matches

        # Get lending offer with lender info
        lending_offer = db.query(LendingOffer).filter(
            LendingOffer.id == lending_offer_id,
            LendingOffer.status == "active"
        ).first()

        if not lending_offer:
            logger.warning(f"Lending offer {lending_offer_id} not found or not active")
            return []

        # Get lender profile and ratings
        lender = db.query(User).join(UserProfile).filter(User.id == lending_offer.lender_id).first()
        lender_rating = self._get_user_average_rating(lending_offer.lender_id, db)

        # Find potential loan requests
        potential_requests = self._get_compatible_loan_requests(lending_offer, db)

        matches = []
        for request in potential_requests:
            # Get borrower info
            borrower = db.query(User).join(UserProfile).filter(User.id == request.borrower_id).first()
            borrower_rating = self._get_user_average_rating(request.borrower_id, db)

            # Calculate match score
            match_score = self._calculate_match_score(
                request, lending_offer, borrower, lender, borrower_rating, lender_rating, db
            )

            if match_score.total_score >= self.min_match_score:
                # Generate suggested terms and probability
                suggested_terms = self._generate_suggested_terms(request, lending_offer, match_score)
                approval_probability = self._estimate_approval_probability(match_score, borrower_rating, lender_rating)
                match_reasons = self._generate_match_reasons(match_score)

                loan_match = LoanMatch(
                    borrower_id=request.borrower_id,
                    lender_id=lending_offer.lender_id,
                    loan_request_id=request.id,
                    lending_offer_id=lending_offer_id,
                    match_score=match_score,
                    estimated_approval_probability=approval_probability,
                    suggested_terms=suggested_terms,
                    match_reasons=match_reasons
                )
                matches.append(loan_match)

        # Sort by total score and limit results
        matches.sort(key=lambda x: x.match_score.total_score, reverse=True)
        matches = matches[:limit]

        # Cache results for 30 minutes
        await self.cache.set(cache_key, matches, 1800)

        logger.info(f"Found {len(matches)} matches for lender offer {lending_offer_id}")
        return matches

    def _get_compatible_lending_offers(self, loan_request: LoanRequest, db: Session) -> List[LendingOffer]:
        """Get lending offers that are potentially compatible with a loan request."""

        # Basic compatibility filters
        return db.query(LendingOffer).filter(
            LendingOffer.status == "active",
            LendingOffer.lender_id != loan_request.borrower_id,  # Can't lend to yourself
            LendingOffer.min_amount <= loan_request.amount,
            LendingOffer.max_amount >= loan_request.amount,
            LendingOffer.min_term <= loan_request.term_months,
            LendingOffer.max_term >= loan_request.term_months,
            # Interest rate compatibility (with some flexibility)
            or_(
                LendingOffer.min_interest_rate <= loan_request.max_interest_rate * 1.1,
                LendingOffer.min_interest_rate.is_(None)
            )
        ).limit(50).all()  # Limit initial candidates

    def _get_compatible_loan_requests(self, lending_offer: LendingOffer, db: Session) -> List[LoanRequest]:
        """Get loan requests that are potentially compatible with a lending offer."""

        # Basic compatibility filters
        return db.query(LoanRequest).filter(
            LoanRequest.status == "active",
            LoanRequest.borrower_id != lending_offer.lender_id,  # Can't borrow from yourself
            LoanRequest.amount >= lending_offer.min_amount,
            LoanRequest.amount <= lending_offer.max_amount,
            LoanRequest.term_months >= lending_offer.min_term,
            LoanRequest.term_months <= lending_offer.max_term,
            # Interest rate compatibility (with some flexibility)
            or_(
                LoanRequest.max_interest_rate >= lending_offer.min_interest_rate * 0.9,
                lending_offer.min_interest_rate.is_(None)
            )
        ).limit(50).all()  # Limit initial candidates

    def _calculate_match_score(
        self,
        loan_request: LoanRequest,
        lending_offer: LendingOffer,
        borrower: User,
        lender: User,
        borrower_rating: float,
        lender_rating: float,
        db: Session
    ) -> MatchScore:
        """Calculate comprehensive match score between a loan request and lending offer."""

        criteria_scores = {}

        # 1. Loan Amount Compatibility (25%)
        amount_score = self._score_amount_compatibility(loan_request.amount, lending_offer.min_amount, lending_offer.max_amount)
        criteria_scores[MatchingCriteria.LOAN_AMOUNT.value] = amount_score

        # 2. Interest Rate Compatibility (20%)
        rate_score = self._score_interest_rate_compatibility(loan_request.max_interest_rate, lending_offer.min_interest_rate)
        criteria_scores[MatchingCriteria.INTEREST_RATE.value] = rate_score

        # 3. Loan Term Compatibility (15%)
        term_score = self._score_term_compatibility(loan_request.term_months, lending_offer.min_term, lending_offer.max_term)
        criteria_scores[MatchingCriteria.LOAN_TERM.value] = term_score

        # 4. Credit Score Compatibility (15%)
        credit_score = self._score_credit_compatibility(
            getattr(loan_request, 'credit_score', None),
            getattr(lending_offer, 'min_credit_score', None)
        )
        criteria_scores[MatchingCriteria.CREDIT_SCORE.value] = credit_score

        # 5. User Rating Score (10%)
        rating_score = self._score_user_ratings(borrower_rating, lender_rating)
        criteria_scores[MatchingCriteria.USER_RATING.value] = rating_score

        # 6. Geographic Proximity (5%)
        geo_score = self._score_geographic_proximity(borrower, lender)
        criteria_scores[MatchingCriteria.GEOGRAPHIC_PROXIMITY.value] = geo_score

        # 7. Previous History (5%)
        history_score = self._score_previous_history(borrower.id, lender.id, db)
        criteria_scores[MatchingCriteria.PREVIOUS_HISTORY.value] = history_score

        # 8. Risk Tolerance (3%)
        risk_score = self._score_risk_tolerance(loan_request, lending_offer)
        criteria_scores[MatchingCriteria.RISK_TOLERANCE.value] = risk_score

        # 9. Loan Purpose Compatibility (2%)
        purpose_score = self._score_loan_purpose(loan_request.purpose, getattr(lending_offer, 'preferred_purposes', None))
        criteria_scores[MatchingCriteria.LOAN_PURPOSE.value] = purpose_score

        # Calculate weighted total score
        total_score = sum(
            criteria_scores[criteria.value] * self.scoring_weights[criteria]
            for criteria in MatchingCriteria
        )

        # Determine confidence and risk levels
        confidence_level = self._determine_confidence_level(total_score)
        risk_assessment = self._assess_risk_level(criteria_scores, borrower_rating)
        recommendation_strength = self._determine_recommendation_strength(total_score, confidence_level)

        return MatchScore(
            total_score=round(total_score, 3),
            criteria_scores=criteria_scores,
            confidence_level=confidence_level,
            risk_assessment=risk_assessment,
            recommendation_strength=recommendation_strength
        )

    def _score_amount_compatibility(self, requested_amount: float, min_amount: float, max_amount: float) -> float:
        """Score how well the requested amount fits within the lending range."""
        if min_amount <= requested_amount <= max_amount:
            # Perfect fit gets full score
            return 1.0
        elif requested_amount < min_amount:
            # Below minimum - score based on how close
            return max(0.0, 1.0 - (min_amount - requested_amount) / min_amount)
        else:
            # Above maximum - score based on how close
            return max(0.0, 1.0 - (requested_amount - max_amount) / max_amount)

    def _score_interest_rate_compatibility(self, max_borrower_rate: float, min_lender_rate: float) -> float:
        """Score interest rate compatibility between borrower and lender."""
        if not max_borrower_rate or not min_lender_rate:
            return 0.7  # Neutral score if rates not specified

        if max_borrower_rate >= min_lender_rate:
            # Compatible rates
            overlap = max_borrower_rate - min_lender_rate
            return min(1.0, 0.7 + (overlap / max_borrower_rate) * 0.3)
        else:
            # Incompatible rates - score based on gap
            gap = min_lender_rate - max_borrower_rate
            return max(0.0, 0.5 - (gap / max_borrower_rate))

    def _score_term_compatibility(self, requested_term: int, min_term: int, max_term: int) -> float:
        """Score loan term compatibility."""
        if min_term <= requested_term <= max_term:
            return 1.0
        elif requested_term < min_term:
            return max(0.0, 1.0 - (min_term - requested_term) / min_term)
        else:
            return max(0.0, 1.0 - (requested_term - max_term) / max_term)

    def _score_credit_compatibility(self, borrower_credit: Optional[int], min_required_credit: Optional[int]) -> float:
        """Score credit score compatibility."""
        if not borrower_credit or not min_required_credit:
            return 0.6  # Neutral score if credit info not available

        if borrower_credit >= min_required_credit:
            # Exceeds minimum - bonus for higher scores
            excess = borrower_credit - min_required_credit
            return min(1.0, 0.8 + (excess / 100) * 0.2)
        else:
            # Below minimum - penalty based on gap
            gap = min_required_credit - borrower_credit
            return max(0.0, 0.8 - (gap / 100) * 0.8)

    def _score_user_ratings(self, borrower_rating: float, lender_rating: float) -> float:
        """Score based on user ratings."""
        avg_rating = (borrower_rating + lender_rating) / 2
        return min(1.0, avg_rating / 5.0)  # Normalize to 0-1 scale

    def _score_geographic_proximity(self, borrower: User, lender: User) -> float:
        """Score based on geographic proximity."""
        # Simplified implementation - in real app would use actual location data
        borrower_location = getattr(borrower.profile, 'location', '') if borrower.profile else ''
        lender_location = getattr(lender.profile, 'location', '') if lender.profile else ''

        if not borrower_location or not lender_location:
            return 0.5  # Neutral if no location data

        # Simple string matching - in real implementation would use geographic distance
        if borrower_location.lower() == lender_location.lower():
            return 1.0
        elif any(word in lender_location.lower() for word in borrower_location.lower().split()):
            return 0.7
        else:
            return 0.3

    def _score_previous_history(self, borrower_id: int, lender_id: int, db: Session) -> float:
        """Score based on previous interaction history."""
        # Check if they have previous successful transactions
        connection = db.query(Connection).filter(
            or_(
                and_(Connection.requester_id == borrower_id, Connection.addressee_id == lender_id),
                and_(Connection.requester_id == lender_id, Connection.addressee_id == borrower_id)
            ),
            Connection.status == "accepted"
        ).first()

        if connection:
            return 1.0  # Bonus for previous successful connection
        else:
            return 0.5  # Neutral if no history

    def _score_risk_tolerance(self, loan_request: LoanRequest, lending_offer: LendingOffer) -> float:
        """Score risk tolerance compatibility."""
        # Simplified implementation - would use more sophisticated risk assessment
        borrower_risk = getattr(loan_request, 'risk_category', 'medium')
        lender_tolerance = getattr(lending_offer, 'risk_tolerance', 'medium')

        risk_matrix = {
            ('low', 'high'): 1.0,
            ('low', 'medium'): 0.8,
            ('low', 'low'): 0.6,
            ('medium', 'high'): 0.9,
            ('medium', 'medium'): 1.0,
            ('medium', 'low'): 0.4,
            ('high', 'high'): 1.0,
            ('high', 'medium'): 0.5,
            ('high', 'low'): 0.1
        }

        return risk_matrix.get((borrower_risk, lender_tolerance), 0.5)

    def _score_loan_purpose(self, requested_purpose: str, preferred_purposes: Optional[List[str]]) -> float:
        """Score loan purpose compatibility."""
        if not preferred_purposes:
            return 0.8  # Neutral if no preference specified

        if requested_purpose.lower() in [p.lower() for p in preferred_purposes]:
            return 1.0
        else:
            return 0.3

    def _get_user_average_rating(self, user_id: int, db: Session) -> float:
        """Get average rating for a user."""
        avg_rating = db.query(func.avg(UserRating.rating)).filter(
            UserRating.rated_user_id == user_id
        ).scalar()

        return float(avg_rating or 4.0)  # Default to 4.0 if no ratings

    def _generate_suggested_terms(self, loan_request: LoanRequest, lending_offer: LendingOffer, match_score: MatchScore) -> Dict[str, Any]:
        """Generate suggested loan terms based on the match."""
        suggested_amount = loan_request.amount

        # Suggest interest rate based on compatibility
        if lending_offer.min_interest_rate and loan_request.max_interest_rate:
            suggested_rate = (lending_offer.min_interest_rate + loan_request.max_interest_rate) / 2
        elif lending_offer.min_interest_rate:
            suggested_rate = lending_offer.min_interest_rate
        elif loan_request.max_interest_rate:
            suggested_rate = loan_request.max_interest_rate
        else:
            suggested_rate = 8.5  # Default rate

        # Adjust rate based on match score
        rate_adjustment = (match_score.total_score - 0.7) * 2  # -0.4 to +0.6 adjustment
        suggested_rate = max(3.0, min(25.0, suggested_rate + rate_adjustment))

        return {
            "amount": suggested_amount,
            "interest_rate": round(suggested_rate, 2),
            "term_months": loan_request.term_months,
            "monthly_payment": round((suggested_amount * (suggested_rate/100/12)) /
                                   (1 - (1 + suggested_rate/100/12)**(-loan_request.term_months)), 2)
        }

    def _estimate_approval_probability(self, match_score: MatchScore, borrower_rating: float, lender_rating: float) -> float:
        """Estimate probability of loan approval."""
        base_probability = match_score.total_score * 0.7
        rating_bonus = ((borrower_rating + lender_rating) / 2 - 3.0) * 0.1  # Bonus for high ratings

        return min(0.95, max(0.05, base_probability + rating_bonus))

    def _generate_match_reasons(self, match_score: MatchScore) -> List[str]:
        """Generate human-readable reasons for the match."""
        reasons = []

        # Add reasons based on high-scoring criteria
        if match_score.criteria_scores.get('loan_amount', 0) > 0.8:
            reasons.append("Loan amount perfectly matches lender's capacity")

        if match_score.criteria_scores.get('interest_rate', 0) > 0.8:
            reasons.append("Interest rate expectations are well aligned")

        if match_score.criteria_scores.get('user_rating', 0) > 0.8:
            reasons.append("Both users have excellent ratings")

        if match_score.criteria_scores.get('previous_history', 0) > 0.8:
            reasons.append("Previous successful interaction history")

        if match_score.criteria_scores.get('geographic_proximity', 0) > 0.8:
            reasons.append("Located in the same area")

        if not reasons:
            reasons.append("Good overall compatibility across multiple factors")

        return reasons

    def _determine_confidence_level(self, total_score: float) -> str:
        """Determine confidence level for the match."""
        if total_score >= 0.85:
            return "very_high"
        elif total_score >= 0.75:
            return "high"
        elif total_score >= 0.65:
            return "medium"
        else:
            return "low"

    def _assess_risk_level(self, criteria_scores: Dict[str, float], borrower_rating: float) -> str:
        """Assess overall risk level of the match."""
        credit_score = criteria_scores.get('credit_score', 0.5)
        rating_score = criteria_scores.get('user_rating', 0.5)

        risk_score = (credit_score * 0.6) + (rating_score * 0.4)

        if risk_score >= 0.8 and borrower_rating >= 4.5:
            return "low"
        elif risk_score >= 0.6 and borrower_rating >= 3.5:
            return "medium"
        else:
            return "high"

    def _determine_recommendation_strength(self, total_score: float, confidence_level: str) -> str:
        """Determine recommendation strength."""
        if total_score >= 0.8 and confidence_level in ["high", "very_high"]:
            return "strong"
        elif total_score >= 0.7 and confidence_level in ["medium", "high", "very_high"]:
            return "moderate"
        else:
            return "weak"

    async def invalidate_matches_cache(self, user_id: int, match_type: str = "all"):
        """Invalidate cached matches for a user."""
        if match_type in ["all", "borrower"]:
            # Find all loan requests for this user and clear their caches
            pattern = f"borrower_matches:*"  # Would need to implement pattern-based cache clearing
            await self.cache.delete_pattern(pattern)

        if match_type in ["all", "lender"]:
            # Find all lending offers for this user and clear their caches
            pattern = f"lender_matches:*"  # Would need to implement pattern-based cache clearing
            await self.cache.delete_pattern(pattern)

        logger.info(f"Invalidated {match_type} match caches for user {user_id}")


# Global matching service instance
_matching_service: Optional[IntelligentMatchingService] = None


def get_matching_service() -> IntelligentMatchingService:
    """Get matching service instance."""
    global _matching_service
    if _matching_service is None:
        _matching_service = IntelligentMatchingService()
    return _matching_service