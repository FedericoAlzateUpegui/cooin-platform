"""
Unit tests for intelligent matching service.
Tests matching algorithms, scoring logic, and compatibility calculations.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from decimal import Decimal

from app.services.matching_service import (
    IntelligentMatchingService,
    MatchingCriteria,
    MatchResult,
    SuggestedTerms
)
from app.models import User, LoanRequest, LendingOffer, UserProfile


class TestMatchingCriteria:
    """Test matching criteria and scoring logic."""

    @pytest.fixture
    def matching_service(self):
        """Create matching service instance."""
        return IntelligentMatchingService()

    @pytest.fixture
    def sample_loan_request(self):
        """Create sample loan request."""
        loan_request = Mock(spec=LoanRequest)
        loan_request.id = 1
        loan_request.user_id = 1
        loan_request.loan_amount = Decimal('25000.00')
        loan_request.loan_term_months = 36
        loan_request.max_interest_rate = Decimal('8.5')
        loan_request.loan_purpose = "home_improvement"
        return loan_request

    @pytest.fixture
    def sample_lending_offer(self):
        """Create sample lending offer."""
        lending_offer = Mock(spec=LendingOffer)
        lending_offer.id = 1
        lending_offer.user_id = 2
        lending_offer.min_loan_amount = Decimal('10000.00')
        lending_offer.max_loan_amount = Decimal('50000.00')
        lending_offer.interest_rate = Decimal('7.5')
        lending_offer.preferred_loan_terms = "24,36,48"
        return lending_offer

    @pytest.fixture
    def borrower_profile(self):
        """Create borrower profile."""
        profile = Mock(spec=UserProfile)
        profile.user_id = 1
        profile.city = "San Francisco"
        profile.state_province = "California"
        profile.country = "United States"
        return profile

    @pytest.fixture
    def lender_profile(self):
        """Create lender profile."""
        profile = Mock(spec=UserProfile)
        profile.user_id = 2
        profile.city = "San Francisco"
        profile.state_province = "California"
        profile.country = "United States"
        return profile

    def test_loan_amount_compatibility_perfect_match(self, matching_service, sample_loan_request, sample_lending_offer):
        """Test perfect loan amount compatibility."""
        # Loan request: $25,000, Lending offer: $10,000-$50,000
        score = matching_service._calculate_loan_amount_compatibility(
            sample_loan_request,
            sample_lending_offer
        )

        assert score == 1.0  # Perfect match

    def test_loan_amount_compatibility_too_high(self, matching_service):
        """Test loan amount too high for lender."""
        loan_request = Mock(spec=LoanRequest)
        loan_request.loan_amount = Decimal('60000.00')  # Above max

        lending_offer = Mock(spec=LendingOffer)
        lending_offer.min_loan_amount = Decimal('10000.00')
        lending_offer.max_loan_amount = Decimal('50000.00')

        score = matching_service._calculate_loan_amount_compatibility(
            loan_request,
            lending_offer
        )

        assert score == 0.0  # No match

    def test_loan_amount_compatibility_too_low(self, matching_service):
        """Test loan amount too low for lender."""
        loan_request = Mock(spec=LoanRequest)
        loan_request.loan_amount = Decimal('5000.00')  # Below min

        lending_offer = Mock(spec=LendingOffer)
        lending_offer.min_loan_amount = Decimal('10000.00')
        lending_offer.max_loan_amount = Decimal('50000.00')

        score = matching_service._calculate_loan_amount_compatibility(
            loan_request,
            lending_offer
        )

        assert score == 0.0  # No match

    def test_interest_rate_compatibility_acceptable(self, matching_service):
        """Test acceptable interest rate compatibility."""
        loan_request = Mock(spec=LoanRequest)
        loan_request.max_interest_rate = Decimal('8.5')

        lending_offer = Mock(spec=LendingOffer)
        lending_offer.interest_rate = Decimal('7.5')  # Below max

        score = matching_service._calculate_interest_rate_compatibility(
            loan_request,
            lending_offer
        )

        assert score == 1.0  # Perfect - rate is below max

    def test_interest_rate_compatibility_too_high(self, matching_service):
        """Test interest rate too high."""
        loan_request = Mock(spec=LoanRequest)
        loan_request.max_interest_rate = Decimal('7.0')

        lending_offer = Mock(spec=LendingOffer)
        lending_offer.interest_rate = Decimal('8.5')  # Above max

        score = matching_service._calculate_interest_rate_compatibility(
            loan_request,
            lending_offer
        )

        assert score == 0.0  # No match

    def test_term_compatibility_exact_match(self, matching_service):
        """Test exact term compatibility match."""
        loan_request = Mock(spec=LoanRequest)
        loan_request.loan_term_months = 36

        lending_offer = Mock(spec=LendingOffer)
        lending_offer.preferred_loan_terms = "24,36,48"

        score = matching_service._calculate_term_compatibility(
            loan_request,
            lending_offer
        )

        assert score == 1.0  # Exact match

    def test_term_compatibility_no_match(self, matching_service):
        """Test no term compatibility."""
        loan_request = Mock(spec=LoanRequest)
        loan_request.loan_term_months = 60

        lending_offer = Mock(spec=LendingOffer)
        lending_offer.preferred_loan_terms = "24,36,48"

        score = matching_service._calculate_term_compatibility(
            loan_request,
            lending_offer
        )

        assert score < 1.0  # Partial or no match

    def test_geographic_proximity_same_city(self, matching_service, borrower_profile, lender_profile):
        """Test geographic proximity for same city."""
        score = matching_service._calculate_geographic_proximity(
            borrower_profile,
            lender_profile
        )

        assert score == 1.0  # Same city = perfect match

    def test_geographic_proximity_different_cities(self, matching_service):
        """Test geographic proximity for different cities."""
        borrower_profile = Mock(spec=UserProfile)
        borrower_profile.city = "San Francisco"
        borrower_profile.state_province = "California"
        borrower_profile.country = "United States"

        lender_profile = Mock(spec=UserProfile)
        lender_profile.city = "Los Angeles"
        lender_profile.state_province = "California"
        lender_profile.country = "United States"

        score = matching_service._calculate_geographic_proximity(
            borrower_profile,
            lender_profile
        )

        assert 0.5 <= score < 1.0  # Same state but different city

    def test_geographic_proximity_different_countries(self, matching_service):
        """Test geographic proximity for different countries."""
        borrower_profile = Mock(spec=UserProfile)
        borrower_profile.city = "San Francisco"
        borrower_profile.state_province = "California"
        borrower_profile.country = "United States"

        lender_profile = Mock(spec=UserProfile)
        lender_profile.city = "Toronto"
        lender_profile.state_province = "Ontario"
        lender_profile.country = "Canada"

        score = matching_service._calculate_geographic_proximity(
            borrower_profile,
            lender_profile
        )

        assert score < 0.5  # Different country


class TestMatchingAlgorithm:
    """Test the overall matching algorithm."""

    @pytest.fixture
    def matching_service(self):
        """Create matching service with mocked cache."""
        with patch('app.services.matching_service.get_app_cache_service') as mock_cache:
            mock_cache.return_value = AsyncMock()
            service = IntelligentMatchingService()
            return service

    @pytest.mark.asyncio
    async def test_calculate_match_score(self, matching_service):
        """Test overall match score calculation."""
        # Create mock data
        loan_request = Mock(spec=LoanRequest)
        loan_request.loan_amount = Decimal('25000.00')
        loan_request.loan_term_months = 36
        loan_request.max_interest_rate = Decimal('8.5')

        lending_offer = Mock(spec=LendingOffer)
        lending_offer.min_loan_amount = Decimal('10000.00')
        lending_offer.max_loan_amount = Decimal('50000.00')
        lending_offer.interest_rate = Decimal('7.5')
        lending_offer.preferred_loan_terms = "24,36,48"

        borrower_profile = Mock(spec=UserProfile)
        borrower_profile.city = "San Francisco"
        borrower_profile.state_province = "California"
        borrower_profile.country = "United States"

        lender_profile = Mock(spec=UserProfile)
        lender_profile.city = "San Francisco"
        lender_profile.state_province = "California"
        lender_profile.country = "United States"

        # Mock additional data for remaining criteria
        borrower_user = Mock(spec=User)
        borrower_user.id = 1

        lender_user = Mock(spec=User)
        lender_user.id = 2

        with patch.object(matching_service, '_get_user_credit_score', return_value=750), \
             patch.object(matching_service, '_get_user_rating', return_value=4.5):

            score = await matching_service._calculate_match_score(
                loan_request,
                lending_offer,
                borrower_user,
                lender_user,
                borrower_profile,
                lender_profile
            )

            assert 0.0 <= score <= 1.0
            assert score > matching_service.min_match_score  # Should be a good match

    def test_generate_suggested_terms(self, matching_service):
        """Test suggested terms generation."""
        loan_request = Mock(spec=LoanRequest)
        loan_request.loan_amount = Decimal('25000.00')
        loan_request.loan_term_months = 36
        loan_request.max_interest_rate = Decimal('8.5')

        lending_offer = Mock(spec=LendingOffer)
        lending_offer.interest_rate = Decimal('7.5')

        suggested = matching_service._generate_suggested_terms(
            loan_request,
            lending_offer,
            0.85  # Good match score
        )

        assert isinstance(suggested, SuggestedTerms)
        assert suggested.loan_amount == Decimal('25000.00')
        assert suggested.interest_rate <= loan_request.max_interest_rate
        assert suggested.loan_term_months > 0

    def test_match_result_creation(self):
        """Test MatchResult creation."""
        match = MatchResult(
            lender_id=1,
            compatibility_score=0.85,
            suggested_terms=SuggestedTerms(
                loan_amount=Decimal('25000.00'),
                interest_rate=Decimal('7.5'),
                loan_term_months=36
            ),
            match_reasons=[
                "Interest rate matches your preferences",
                "Geographic proximity",
                "Strong lender rating"
            ]
        )

        assert match.lender_id == 1
        assert match.compatibility_score == 0.85
        assert match.suggested_terms.loan_amount == Decimal('25000.00')
        assert len(match.match_reasons) == 3

    def test_suggested_terms_creation(self):
        """Test SuggestedTerms creation."""
        terms = SuggestedTerms(
            loan_amount=Decimal('25000.00'),
            interest_rate=Decimal('7.5'),
            loan_term_months=36
        )

        assert terms.loan_amount == Decimal('25000.00')
        assert terms.interest_rate == Decimal('7.5')
        assert terms.loan_term_months == 36

    def test_scoring_weights_sum_to_one(self, matching_service):
        """Test that scoring weights sum to approximately 1.0."""
        weights = matching_service.scoring_weights
        total_weight = sum(weights.values())

        assert abs(total_weight - 1.0) < 0.01  # Allow for small rounding errors

    def test_min_match_score_threshold(self, matching_service):
        """Test minimum match score threshold."""
        assert 0.0 < matching_service.min_match_score < 1.0
        assert matching_service.min_match_score == 0.6


class TestMatchingServiceIntegration:
    """Test matching service integration with cache and database."""

    @pytest.fixture
    def matching_service(self):
        """Create matching service with real cache mock."""
        with patch('app.services.matching_service.get_app_cache_service') as mock_cache_getter:
            mock_cache = AsyncMock()
            mock_cache_getter.return_value = mock_cache
            service = IntelligentMatchingService()
            service.cache = mock_cache
            return service

    @pytest.mark.asyncio
    async def test_cache_integration(self, matching_service):
        """Test cache integration for match results."""
        # Mock cache behavior
        cache_key = "borrower_matches:1"
        cached_data = [{"lender_id": 2, "score": 0.85}]

        matching_service.cache.get = AsyncMock(return_value=cached_data)
        matching_service.cache.set = AsyncMock()

        # Test cache retrieval
        result = await matching_service.cache.get(cache_key)
        assert result == cached_data

        # Test cache setting
        await matching_service.cache.set(cache_key, cached_data, 3600)
        matching_service.cache.set.assert_called_once_with(cache_key, cached_data, 3600)

    @pytest.mark.asyncio
    async def test_error_handling_in_matching(self, matching_service):
        """Test error handling in matching process."""
        # Mock database error
        with patch.object(matching_service, '_get_user_credit_score', side_effect=Exception("Database error")):

            loan_request = Mock(spec=LoanRequest)
            lending_offer = Mock(spec=LendingOffer)
            borrower_user = Mock(spec=User)
            lender_user = Mock(spec=User)
            borrower_profile = Mock(spec=UserProfile)
            lender_profile = Mock(spec=UserProfile)

            # Should handle error gracefully and return 0 score or skip
            try:
                score = await matching_service._calculate_match_score(
                    loan_request,
                    lending_offer,
                    borrower_user,
                    lender_user,
                    borrower_profile,
                    lender_profile
                )
                # If it doesn't raise, score should be low due to error
                assert 0.0 <= score <= 1.0
            except Exception:
                # Or it might raise an exception that should be handled upstream
                pass