//
//  Models.swift
//  Cooin
//
//  Data models for the Cooin app
//

import Foundation

// MARK: - API Response Models

struct APIResponse<T: Codable>: Codable {
    let success: Bool
    let data: T?
    let message: String?
    let error: APIErrorResponse?
}

struct MobileAPIResponse<T: Codable>: Codable {
    let success: Bool
    let data: T?
    let timestamp: String
    let requestId: String?

    enum CodingKeys: String, CodingKey {
        case success, data, timestamp
        case requestId = "request_id"
    }
}

struct APIErrorResponse: Codable {
    let code: String?
    let message: String
    let details: [String: String]?
}

// MARK: - User Models

struct User: Codable, Identifiable {
    let id: Int
    let email: String
    let username: String
    let role: String
    let isActive: Bool?
    let isVerified: Bool?
    let profileCompletion: Double?
    let createdAt: String?

    enum CodingKeys: String, CodingKey {
        case id, email, username, role
        case isActive = "is_active"
        case isVerified = "is_verified"
        case profileCompletion = "profile_completion"
        case createdAt = "created_at"
    }
}

struct UserRegistration: Codable {
    let email: String
    let username: String
    let password: String
    let confirmPassword: String
    let role: String
    let agreeToTerms: Bool

    enum CodingKeys: String, CodingKey {
        case email, username, password, role
        case confirmPassword = "confirm_password"
        case agreeToTerms = "agree_to_terms"
    }
}

struct LoginRequest: Codable {
    let email: String
    let password: String
    let rememberMe: Bool

    enum CodingKeys: String, CodingKey {
        case email, password
        case rememberMe = "remember_me"
    }
}

// MARK: - Authentication Models

struct Tokens: Codable {
    let accessToken: String
    let refreshToken: String
    let tokenType: String
    let expiresIn: Int

    enum CodingKeys: String, CodingKey {
        case accessToken = "access_token"
        case refreshToken = "refresh_token"
        case tokenType = "token_type"
        case expiresIn = "expires_in"
    }
}

struct AuthResponse: Codable {
    let user: User
    let tokens: Tokens
}

struct AuthResponseData: Codable {
    let user: User
    let tokens: Tokens
}

struct UserData: Codable {
    let user: User
}

// MARK: - Analytics Models

struct MobileAnalytics: Codable {
    let platformStats: PlatformStats
    let growthTrends: GrowthTrends
    let financialOverview: FinancialOverview

    enum CodingKeys: String, CodingKey {
        case platformStats = "platform_stats"
        case growthTrends = "growth_trends"
        case financialOverview = "financial_overview"
    }

    static let empty = MobileAnalytics(
        platformStats: PlatformStats(totalUsers: 0, activeUsers: 0, loanRequests: 0, lendingOffers: 0),
        growthTrends: GrowthTrends(userGrowth: 0, activityGrowth: 0),
        financialOverview: FinancialOverview(avgLoanAmount: "$0", totalVolume: "$0")
    )
}

struct PlatformStats: Codable {
    let totalUsers: Int
    let activeUsers: Int
    let loanRequests: Int
    let lendingOffers: Int

    enum CodingKeys: String, CodingKey {
        case totalUsers = "total_users"
        case activeUsers = "active_users"
        case loanRequests = "loan_requests"
        case lendingOffers = "lending_offers"
    }
}

struct GrowthTrends: Codable {
    let userGrowth: Double
    let activityGrowth: Double

    enum CodingKeys: String, CodingKey {
        case userGrowth = "user_growth"
        case activityGrowth = "activity_growth"
    }
}

struct FinancialOverview: Codable {
    let avgLoanAmount: String
    let totalVolume: String

    enum CodingKeys: String, CodingKey {
        case avgLoanAmount = "avg_loan_amount"
        case totalVolume = "total_volume"
    }
}

// MARK: - Profile Models

struct UserProfile: Codable, Identifiable {
    let id: Int?
    let firstName: String?
    let lastName: String?
    let displayName: String?
    let bio: String?
    let city: String?
    let stateProvince: String?
    let country: String?

    enum CodingKeys: String, CodingKey {
        case id
        case firstName = "first_name"
        case lastName = "last_name"
        case displayName = "display_name"
        case bio, city
        case stateProvince = "state_province"
        case country
    }
}

// MARK: - Loan Models

struct LoanRequest: Codable, Identifiable {
    let id: Int
    let loanAmount: Double
    let loanPurpose: String
    let maxInterestRate: Double
    let loanTermMonths: Int
    let description: String?

    enum CodingKeys: String, CodingKey {
        case id
        case loanAmount = "loan_amount"
        case loanPurpose = "loan_purpose"
        case maxInterestRate = "max_interest_rate"
        case loanTermMonths = "loan_term_months"
        case description
    }
}

struct LendingOffer: Codable, Identifiable {
    let id: Int
    let availableAmount: Double
    let minLoanAmount: Double
    let maxLoanAmount: Double
    let interestRate: Double
    let preferredLoanTerms: String

    enum CodingKeys: String, CodingKey {
        case id
        case availableAmount = "available_amount"
        case minLoanAmount = "min_loan_amount"
        case maxLoanAmount = "max_loan_amount"
        case interestRate = "interest_rate"
        case preferredLoanTerms = "preferred_loan_terms"
    }
}

// MARK: - Matching Models

struct LoanMatch: Codable, Identifiable {
    let id: Int
    let lenderId: Int?
    let borrowerId: Int?
    let compatibilityScore: Double
    let matchReasons: [String]
    let suggestedTerms: SuggestedTerms?

    enum CodingKeys: String, CodingKey {
        case id
        case lenderId = "lender_id"
        case borrowerId = "borrower_id"
        case compatibilityScore = "compatibility_score"
        case matchReasons = "match_reasons"
        case suggestedTerms = "suggested_terms"
    }
}

struct SuggestedTerms: Codable {
    let loanAmount: Double
    let interestRate: Double
    let loanTermMonths: Int
    let monthlyPayment: Double?
    let totalInterest: Double?

    enum CodingKeys: String, CodingKey {
        case loanAmount = "loan_amount"
        case interestRate = "interest_rate"
        case loanTermMonths = "loan_term_months"
        case monthlyPayment = "monthly_payment"
        case totalInterest = "total_interest"
    }
}