//
//  APIClient.swift
//  Cooin
//
//  API Client for Cooin Backend
//

import Foundation
import Combine

class APIClient: ObservableObject {
    static let shared = APIClient()

    // API Base URL Configuration
    // Automatically detects simulator vs. physical device
    private let baseURL: String = {
        #if targetEnvironment(simulator)
        // iOS Simulator - use localhost
        return "http://127.0.0.1:8000/api/v1"
        #else
        // Physical Device - UPDATE THIS WITH YOUR MAC'S IP ADDRESS
        // Find your Mac's IP: ifconfig | grep "inet " | grep -v 127.0.0.1
        // Example: return "http://192.168.1.100:8000/api/v1"
        // Or use ngrok: return "https://your-id.ngrok.io/api/v1"

        // TODO: Replace with your Mac's local IP address for device testing
        return "http://192.168.1.9:8000/api/v1"
        #endif
    }()

    var cancellables = Set<AnyCancellable>()

    // MARK: - Authentication

    func register(user: UserRegistration) -> AnyPublisher<AuthResponse, APIError> {
        let url = URL(string: "\(baseURL)/auth/register")!

        return URLSession.shared.dataTaskPublisher(for: createRequest(url: url, method: "POST", body: user))
            .tryMap { data, response -> Data in
                // Check HTTP status code
                guard let httpResponse = response as? HTTPURLResponse else {
                    throw APIError.networkError(NSError(domain: "Invalid response", code: 0))
                }

                // Handle error status codes
                if httpResponse.statusCode == 409 {
                    // Parse conflict error (duplicate email/username)
                    if let errorResponse = try? JSONDecoder().decode(BackendErrorResponse.self, from: data) {
                        throw APIError.conflict(errorResponse.error.detailedMessage)
                    }
                    throw APIError.serverError("Email or username already exists")
                } else if httpResponse.statusCode == 429 {
                    // Handle rate limiting
                    let retryAfter = (httpResponse.value(forHTTPHeaderField: "Retry-After") as? NSString)?.integerValue
                    throw APIError.rateLimited(retryAfter: retryAfter)
                } else if httpResponse.statusCode >= 400 {
                    // Parse other error responses including validation errors (422)
                    if let errorResponse = try? JSONDecoder().decode(BackendErrorResponse.self, from: data) {
                        throw APIError.serverError(errorResponse.error.detailedMessage)
                    }
                    throw APIError.serverError("Registration failed with status \(httpResponse.statusCode)")
                }

                return data
            }
            .tryMap { data -> AuthResponse in
                // Backend returns user data but no tokens for registration
                // Parse the response and create empty tokens
                struct RegisterResponse: Codable {
                    let user: User
                    let message: String?
                }

                let registerResponse = try JSONDecoder().decode(RegisterResponse.self, from: data)
                // Registration doesn't return tokens, so create a default response
                return AuthResponse(
                    user: registerResponse.user,
                    tokens: Tokens(accessToken: "", refreshToken: "", tokenType: "bearer", expiresIn: 0)
                )
            }
            .mapError { error -> APIError in
                if let apiError = error as? APIError {
                    return apiError
                }
                return APIError.networkError(error)
            }
            .eraseToAnyPublisher()
    }

    func login(email: String, password: String) -> AnyPublisher<AuthResponse, APIError> {
        let url = URL(string: "\(baseURL)/auth/login")!
        let loginRequest = LoginRequest(email: email, password: password, rememberMe: false)

        return URLSession.shared.dataTaskPublisher(for: createRequest(url: url, method: "POST", body: loginRequest))
            .tryMap { data, response -> Data in
                // Check HTTP status code
                guard let httpResponse = response as? HTTPURLResponse else {
                    throw APIError.networkError(NSError(domain: "Invalid response", code: 0))
                }

                // Handle error status codes
                if httpResponse.statusCode == 401 {
                    throw APIError.unauthorized
                } else if httpResponse.statusCode == 429 {
                    // Handle rate limiting
                    let retryAfter = (httpResponse.value(forHTTPHeaderField: "Retry-After") as? NSString)?.integerValue
                    throw APIError.rateLimited(retryAfter: retryAfter)
                } else if httpResponse.statusCode >= 400 {
                    // Parse error responses including validation errors
                    if let errorResponse = try? JSONDecoder().decode(BackendErrorResponse.self, from: data) {
                        throw APIError.serverError(errorResponse.error.detailedMessage)
                    }
                    // Fallback for simple error responses
                    if let simpleError = try? JSONDecoder().decode([String: String].self, from: data),
                       let detail = simpleError["detail"] {
                        throw APIError.unauthorized
                    }
                    throw APIError.serverError("Login failed with status \(httpResponse.statusCode)")
                }

                return data
            }
            .decode(type: AuthResponse.self, decoder: JSONDecoder())
            .mapError { error -> APIError in
                if let apiError = error as? APIError {
                    return apiError
                }
                return APIError.networkError(error)
            }
            .eraseToAnyPublisher()
    }

    func getCurrentUser(token: String) -> AnyPublisher<User, APIError> {
        let url = URL(string: "\(baseURL)/auth/me")!

        return URLSession.shared.dataTaskPublisher(for: createAuthenticatedRequest(url: url, method: "GET", token: token))
            .map(\.data)
            .decode(type: APIResponse<UserData>.self, decoder: JSONDecoder())
            .tryMap { response in
                if response.success {
                    return response.data?.user ?? User(id: 0, email: "", username: "", role: "borrower", isActive: nil, isVerified: nil, profileCompletion: nil, createdAt: nil)
                } else {
                    throw APIError.serverError(response.error?.message ?? "Failed to get user")
                }
            }
            .catch { error in
                Fail(error: APIError.networkError(error))
                    .eraseToAnyPublisher()
            }
            .eraseToAnyPublisher()
    }

    // MARK: - Analytics

    func getMobileAnalytics(token: String) -> AnyPublisher<MobileAnalytics, APIError> {
        let url = URL(string: "\(baseURL)/analytics/mobile/summary")!

        return URLSession.shared.dataTaskPublisher(for: createAuthenticatedRequest(url: url, method: "GET", token: token))
            .map(\.data)
            .decode(type: MobileAPIResponse<MobileAnalytics>.self, decoder: JSONDecoder())
            .tryMap { response in
                if response.success {
                    return response.data ?? MobileAnalytics.empty
                } else {
                    throw APIError.serverError("Failed to load analytics")
                }
            }
            .catch { error in
                Fail(error: APIError.networkError(error))
                    .eraseToAnyPublisher()
            }
            .eraseToAnyPublisher()
    }

    // MARK: - Health Check

    func healthCheck() -> AnyPublisher<Bool, APIError> {
        let url = URL(string: "\(baseURL)/health")!

        return URLSession.shared.dataTaskPublisher(for: URLRequest(url: url))
            .map { data, response in
                guard let httpResponse = response as? HTTPURLResponse,
                      httpResponse.statusCode == 200 else {
                    return false
                }
                return true
            }
            .catch { error in
                Just(false)
                    .setFailureType(to: APIError.self)
                    .eraseToAnyPublisher()
            }
            .eraseToAnyPublisher()
    }

    // MARK: - Helper Methods

    private func createRequest<T: Codable>(url: URL, method: String, body: T? = nil) -> URLRequest {
        var request = URLRequest(url: url)
        request.httpMethod = method
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        if let body = body {
            do {
                request.httpBody = try JSONEncoder().encode(body)
            } catch {
                print("Failed to encode request body: \(error)")
            }
        }

        return request
    }

    private func createAuthenticatedRequest(url: URL, method: String, token: String, body: Data? = nil) -> URLRequest {
        var request = URLRequest(url: url)
        request.httpMethod = method
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        request.httpBody = body

        return request
    }
}

// MARK: - API Error

enum APIError: Error, LocalizedError {
    case networkError(Error)
    case serverError(String)
    case conflict(String)
    case decodingError
    case unauthorized
    case rateLimited(retryAfter: Int?)

    var errorDescription: String? {
        switch self {
        case .networkError(_):
            return "Network error. Please check your connection and try again."
        case .serverError(let message):
            // Improve rate limiting message
            if message.lowercased().contains("rate limit") {
                return "Too many attempts. Please wait a few minutes before trying again."
            }
            return message
        case .conflict(let message):
            return message
        case .decodingError:
            return "Something went wrong. Please try again."
        case .unauthorized:
            return "Incorrect email or password. Please try again."
        case .rateLimited(let retryAfter):
            if let seconds = retryAfter {
                let minutes = seconds / 60
                if minutes > 0 {
                    return "Too many attempts. Please wait \(minutes) minute\(minutes == 1 ? "" : "s") before trying again."
                }
                return "Too many attempts. Please wait \(seconds) seconds before trying again."
            }
            return "Too many attempts. Please wait a few minutes before trying again."
        }
    }

    var recoverySuggestion: String? {
        switch self {
        case .networkError(_):
            return "Check your internet connection and try again."
        case .serverError(let message):
            if message.lowercased().contains("password") {
                return "Password must contain at least 8 characters with uppercase, lowercase, and numbers."
            }
            if message.lowercased().contains("email") {
                return "Please use a valid email address."
            }
            return nil
        case .conflict(let message):
            if message.lowercased().contains("email") {
                return "Try using a different email address or login if you already have an account."
            }
            if message.lowercased().contains("username") {
                return "Try using a different username."
            }
            return nil
        case .unauthorized:
            return "Double-check your email and password and try again."
        case .rateLimited(_):
            return "For security, we limit registration attempts. Please wait before trying again."
        case .decodingError:
            return "Please try again. If the problem persists, contact support."
        }
    }
}

// MARK: - Backend Error Response (for structured error responses)

struct BackendErrorResponse: Codable {
    let error: ErrorDetail

    struct ErrorDetail: Codable {
        let code: String
        let message: String
        let statusCode: Int?
        let conflictingField: String?
        let conflictingValue: String?
        let fieldErrors: [FieldError]?

        enum CodingKeys: String, CodingKey {
            case code
            case message
            case statusCode = "status_code"
            case conflictingField = "conflicting_field"
            case conflictingValue = "conflicting_value"
            case fieldErrors = "field_errors"
        }

        // Get the most relevant error message
        var detailedMessage: String {
            if let fieldErrors = fieldErrors, let firstError = fieldErrors.first {
                return firstError.message
            }
            return message
        }
    }

    struct FieldError: Codable {
        let field: String
        let message: String
        let type: String?
        let input: String?
    }
}