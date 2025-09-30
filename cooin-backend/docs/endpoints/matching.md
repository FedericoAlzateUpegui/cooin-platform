# Intelligent Matching Endpoints

The matching system uses AI-powered algorithms to connect borrowers with suitable lenders based on multiple compatibility factors.

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/matching/borrower/matches/{loan_request_id}` | Get matches for borrower |
| GET | `/api/v1/matching/lender/matches/{lending_offer_id}` | Get matches for lender |
| GET | `/api/v1/matching/suggestions/borrower/{loan_request_id}` | Get borrower suggestions |
| GET | `/api/v1/matching/suggestions/lender/{lending_offer_id}` | Get lender suggestions |
| GET | `/api/v1/matching/health` | Matching service health |

## Get Borrower Matches

Find compatible lenders for a loan request using AI-powered matching.

### Request

```http
GET /api/v1/matching/borrower/matches/123?limit=10&min_score=0.7
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `loan_request_id` | integer | Yes | ID of the loan request (path parameter) |
| `limit` | integer | No | Number of matches to return (1-20, default: 10) |
| `offset` | integer | No | Number of matches to skip (default: 0) |
| `min_score` | float | No | Minimum compatibility score (0.0-1.0, default: 0.6) |

### Response

```json
{
  "success": true,
  "data": {
    "loan_request": {
      "id": 123,
      "loan_amount": 25000.00,
      "loan_purpose": "home_improvement",
      "max_interest_rate": 8.5,
      "loan_term_months": 36
    },
    "matches": [
      {
        "lender_id": 456,
        "lender_info": {
          "username": "reliable_lender",
          "rating": 4.8,
          "total_loans_funded": 25,
          "city": "San Francisco",
          "state": "California"
        },
        "compatibility_score": 0.87,
        "match_reasons": [
          "Interest rate matches your preferences (7.2% vs max 8.5%)",
          "Geographic proximity (same city)",
          "Strong lender rating (4.8/5.0)",
          "Experience with home improvement loans",
          "Preferred loan term matches (36 months)"
        ],
        "suggested_terms": {
          "loan_amount": 25000.00,
          "interest_rate": 7.2,
          "loan_term_months": 36,
          "monthly_payment": 775.50,
          "total_interest": 2918.00
        },
        "risk_assessment": {
          "risk_level": "low",
          "confidence_score": 0.92,
          "factors": [
            "Stable employment history",
            "Good credit score range",
            "Low debt-to-income ratio"
          ]
        }
      }
    ],
    "pagination": {
      "limit": 10,
      "offset": 0,
      "total_count": 15,
      "has_next": true,
      "has_previous": false
    },
    "matching_summary": {
      "total_eligible_lenders": 45,
      "matches_above_threshold": 15,
      "avg_compatibility_score": 0.73,
      "top_match_score": 0.87
    }
  }
}
```

## Get Lender Matches

Find compatible borrowers for a lending offer.

### Request

```http
GET /api/v1/matching/lender/matches/789?limit=15
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Response

```json
{
  "success": true,
  "data": {
    "lending_offer": {
      "id": 789,
      "available_amount": 100000.00,
      "min_loan_amount": 10000.00,
      "max_loan_amount": 50000.00,
      "interest_rate": 7.5,
      "preferred_loan_terms": "24,36,48"
    },
    "matches": [
      {
        "borrower_id": 321,
        "borrower_info": {
          "username": "homeowner_borrower",
          "rating": 4.6,
          "city": "San Francisco",
          "employment_status": "employed_full_time",
          "loan_purpose": "home_improvement"
        },
        "loan_request": {
          "id": 555,
          "loan_amount": 30000.00,
          "max_interest_rate": 8.0,
          "loan_term_months": 36
        },
        "compatibility_score": 0.91,
        "match_reasons": [
          "Loan amount within your range ($30K of $10K-$50K)",
          "Acceptable interest rate (7.5% vs max 8.0%)",
          "Perfect term match (36 months)",
          "Low-risk borrower profile",
          "Home improvement specialty match"
        ],
        "risk_assessment": {
          "risk_level": "low",
          "credit_score_range": "720-780",
          "debt_to_income": 0.25,
          "employment_years": 5
        }
      }
    ]
  }
}
```

## Matching Algorithm

The intelligent matching system evaluates compatibility using multiple weighted criteria:

### Scoring Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Loan Amount | 25% | How well the requested amount fits the lender's range |
| Interest Rate | 20% | Rate compatibility and acceptance |
| Term Compatibility | 15% | Matching loan duration preferences |
| Geographic Proximity | 10% | Physical distance consideration |
| Credit Score | 10% | Borrower creditworthiness |
| User Rating | 8% | Historical performance ratings |
| Experience Match | 7% | Lender experience with loan purpose |
| Risk Profile | 3% | Overall risk assessment alignment |
| Response History | 2% | Historical response and engagement rates |

### Compatibility Score

Scores range from 0.0 to 1.0:
- **0.9-1.0**: Excellent match (highly recommended)
- **0.8-0.9**: Very good match (recommended)
- **0.7-0.8**: Good match (suitable)
- **0.6-0.7**: Fair match (consider with caution)
- **< 0.6**: Poor match (filtered out by default)

## Get Match Suggestions

Get AI-generated suggestions to improve matching potential.

### Request

```http
GET /api/v1/matching/suggestions/borrower/123
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Response

```json
{
  "success": true,
  "data": {
    "suggestions": [
      {
        "type": "profile_improvement",
        "priority": "high",
        "title": "Complete Income Verification",
        "message": "Add income verification to increase your match score by up to 15%",
        "action": "upload_documents",
        "estimated_impact": 0.15
      },
      {
        "type": "loan_terms",
        "priority": "medium",
        "title": "Consider Flexible Loan Terms",
        "message": "Accepting 48-month terms would increase your matches by 40%",
        "action": "update_preferences",
        "estimated_impact": 0.08
      },
      {
        "type": "geographic",
        "priority": "low",
        "title": "Expand Geographic Range",
        "message": "Including nearby states could add 12 potential matches",
        "action": "update_location_preferences",
        "estimated_impact": 0.05
      }
    ],
    "overall_score_potential": 0.78,
    "current_score": 0.65,
    "improvement_potential": 0.13
  }
}
```

## Mobile-Optimized Endpoints

Mobile apps should use the mobile-specific endpoints for optimized responses:

### Mobile Borrower Matches

```http
GET /api/v1/mobile/matching/mobile/borrower/matches/123
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Response includes simplified data structure optimized for mobile consumption:

```json
{
  "success": true,
  "data": {
    "matches": [
      {
        "lender_id": 456,
        "score": 0.87,
        "rate": 7.2,
        "rating": 4.8,
        "city": "San Francisco",
        "match_summary": "Great rate, same city, excellent rating"
      }
    ]
  },
  "timestamp": "2024-01-15T10:30:00Z",
  "request_id": "mobile_req_123"
}
```

## Error Handling

### Common Error Responses

**404 Not Found**
```json
{
  "success": false,
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Loan request not found or access denied"
  }
}
```

**403 Forbidden**
```json
{
  "success": false,
  "error": {
    "code": "AUTHORIZATION_ERROR",
    "message": "You can only access matches for your own loan requests"
  }
}
```

**422 Validation Error**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid parameters",
    "details": {
      "min_score": "Must be between 0.0 and 1.0"
    }
  }
}
```

## Caching

Matching results are cached for performance:
- **Cache Duration**: 30 minutes for basic matches
- **Cache Invalidation**: Automatic when profile/preferences change
- **Real-time Updates**: WebSocket notifications for new matches

## Rate Limiting

Matching endpoints have specific rate limits:
- **Standard matching**: 30 requests per minute
- **Mobile matching**: 60 requests per minute
- **Suggestions**: 10 requests per minute

## Code Examples

### JavaScript

```javascript
// Get borrower matches
const getBorrowerMatches = async (loanRequestId, options = {}) => {
  const params = new URLSearchParams({
    limit: options.limit || 10,
    min_score: options.minScore || 0.6,
    ...options
  });

  const response = await fetch(
    `/api/v1/matching/borrower/matches/${loanRequestId}?${params}`,
    {
      headers: {
        'Authorization': `Bearer ${getAccessToken()}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return await response.json();
};

// Get match suggestions
const getMatchSuggestions = async (loanRequestId) => {
  const response = await fetch(
    `/api/v1/matching/suggestions/borrower/${loanRequestId}`,
    {
      headers: {
        'Authorization': `Bearer ${getAccessToken()}`,
      },
    }
  );

  const data = await response.json();
  return data.success ? data.data.suggestions : [];
};
```

### Python

```python
class MatchingClient:
    def __init__(self, api_client):
        self.api = api_client

    def get_borrower_matches(self, loan_request_id, limit=10, min_score=0.6):
        params = {
            'limit': limit,
            'min_score': min_score
        }

        response = self.api.get(
            f"/matching/borrower/matches/{loan_request_id}",
            params=params
        )

        return response.json()

    def get_lender_matches(self, lending_offer_id, **kwargs):
        response = self.api.get(
            f"/matching/lender/matches/{lending_offer_id}",
            params=kwargs
        )

        return response.json()

# Usage
matching = MatchingClient(api_client)
matches = matching.get_borrower_matches(
    loan_request_id=123,
    limit=20,
    min_score=0.7
)

for match in matches['data']['matches']:
    print(f"Lender: {match['lender_info']['username']}")
    print(f"Score: {match['compatibility_score']}")
    print(f"Rate: {match['suggested_terms']['interest_rate']}%")
```

## Performance Considerations

- **First Load**: Initial matches may take 2-3 seconds for complex calculations
- **Subsequent Loads**: Cached results return in < 100ms
- **Background Processing**: Match scores are updated every 4 hours
- **Real-time Updates**: WebSocket notifications for new high-score matches