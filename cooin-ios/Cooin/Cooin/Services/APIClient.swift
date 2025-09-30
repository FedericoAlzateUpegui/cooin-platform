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

    // Your computer's IP address - update this if needed
    private let baseURL = "http://192.168.40.34:8000/api/v1"

    private var cancellables = Set<AnyCancellable>()

    // MARK: - Authentication

    func register(user: UserRegistration) -> AnyPublisher<AuthResponse, APIError> {
        let url = URL(string: "\(baseURL)/auth/register")!

        return URLSession.shared.dataTaskPublisher(for: createRequest(url: url, method: "POST", body: user))
            .map(\.data)
            .decode(type: APIResponse<AuthResponseData>.self, decoder: JSONDecoder())
            .map { response in
                if response.success {
                    return AuthResponse(
                        user: response.data?.user ?? User(id: 0, email: "", username: "", role: "borrower"),
                        tokens: response.data?.tokens ?? Tokens(accessToken: "", refreshToken: "", tokenType: "bearer", expiresIn: 0)
                    )
                } else {
                    throw APIError.serverError(response.error?.message ?? "Registration failed")
                }
            }
            .catch { error in
                Just(AuthResponse(user: User(id: 0, email: "", username: "", role: ""), tokens: Tokens(accessToken: "", refreshToken: "", tokenType: "", expiresIn: 0)))
                    .setFailureType(to: APIError.self)
                    .eraseToAnyPublisher()
            }
            .eraseToAnyPublisher()
    }

    func login(email: String, password: String) -> AnyPublisher<AuthResponse, APIError> {
        let url = URL(string: "\(baseURL)/auth/login")!
        let loginRequest = LoginRequest(email: email, password: password, rememberMe: false)

        return URLSession.shared.dataTaskPublisher(for: createRequest(url: url, method: "POST", body: loginRequest))
            .map(\.data)
            .decode(type: APIResponse<AuthResponseData>.self, decoder: JSONDecoder())
            .map { response in
                if response.success {
                    return AuthResponse(
                        user: response.data?.user ?? User(id: 0, email: "", username: "", role: "borrower"),
                        tokens: response.data?.tokens ?? Tokens(accessToken: "", refreshToken: "", tokenType: "bearer", expiresIn: 0)
                    )
                } else {
                    throw APIError.serverError(response.error?.message ?? "Login failed")
                }
            }
            .catch { error in
                Fail(error: APIError.networkError(error))
                    .eraseToAnyPublisher()
            }
            .eraseToAnyPublisher()
    }

    func getCurrentUser(token: String) -> AnyPublisher<User, APIError> {
        let url = URL(string: "\(baseURL)/auth/me")!

        return URLSession.shared.dataTaskPublisher(for: createAuthenticatedRequest(url: url, method: "GET", token: token))
            .map(\.data)
            .decode(type: APIResponse<UserData>.self, decoder: JSONDecoder())
            .map { response in
                if response.success {
                    return response.data?.user ?? User(id: 0, email: "", username: "", role: "borrower")
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
            .map { response in
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
    case decodingError
    case unauthorized

    var errorDescription: String? {
        switch self {
        case .networkError(let error):
            return "Network error: \(error.localizedDescription)"
        case .serverError(let message):
            return message
        case .decodingError:
            return "Failed to decode response"
        case .unauthorized:
            return "Unauthorized access"
        }
    }
}