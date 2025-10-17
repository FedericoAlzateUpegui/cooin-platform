//
//  AuthenticationManager.swift
//  Cooin
//
//  Manages user authentication state
//

import Foundation
import Combine

class AuthenticationManager: ObservableObject {
    @Published var isAuthenticated = false
    @Published var currentUser: User?
    @Published var isLoading = false
    @Published var errorMessage: String?

    private var accessToken: String?
    private var refreshToken: String?
    private let apiClient = APIClient.shared
    private let keychainHelper = KeychainHelper.shared
    private var cancellables = Set<AnyCancellable>()

    init() {
        loadStoredTokens()
        checkAuthenticationStatus()
    }

    // MARK: - Public Methods

    func register(email: String, username: String, password: String, confirmPassword: String, role: String) {
        isLoading = true
        errorMessage = nil

        let userRegistration = UserRegistration(
            email: email,
            username: username,
            password: password,
            confirmPassword: confirmPassword,
            role: role,
            agreeToTerms: true
        )

        apiClient.register(user: userRegistration)
            .receive(on: DispatchQueue.main)
            .sink(
                receiveCompletion: { completion in
                    self.isLoading = false
                    if case .failure(let error) = completion {
                        self.errorMessage = error.localizedDescription
                    }
                },
                receiveValue: { authResponse in
                    self.handleAuthenticationSuccess(authResponse)
                }
            )
            .store(in: &cancellables)
    }

    func login(email: String, password: String) {
        isLoading = true
        errorMessage = nil

        apiClient.login(email: email, password: password)
            .receive(on: DispatchQueue.main)
            .sink(
                receiveCompletion: { completion in
                    self.isLoading = false
                    if case .failure(let error) = completion {
                        self.errorMessage = error.localizedDescription
                    }
                },
                receiveValue: { authResponse in
                    self.handleAuthenticationSuccess(authResponse)
                }
            )
            .store(in: &cancellables)
    }

    func logout() {
        isAuthenticated = false
        currentUser = nil
        accessToken = nil
        refreshToken = nil
        clearStoredTokens()
    }

    func refreshUserData() {
        guard let token = accessToken else { return }

        apiClient.getCurrentUser(token: token)
            .receive(on: DispatchQueue.main)
            .sink(
                receiveCompletion: { completion in
                    if case .failure = completion {
                        // Handle error silently or show notification
                    }
                },
                receiveValue: { user in
                    self.currentUser = user
                }
            )
            .store(in: &cancellables)
    }

    // MARK: - Private Methods

    private func handleAuthenticationSuccess(_ authResponse: AuthResponse) {
        currentUser = authResponse.user
        accessToken = authResponse.tokens.accessToken
        refreshToken = authResponse.tokens.refreshToken
        isAuthenticated = true

        storeTokens()
    }

    private func checkAuthenticationStatus() {
        guard let token = accessToken else { return }

        apiClient.getCurrentUser(token: token)
            .receive(on: DispatchQueue.main)
            .sink(
                receiveCompletion: { completion in
                    if case .failure = completion {
                        self.logout()
                    }
                },
                receiveValue: { user in
                    self.currentUser = user
                    self.isAuthenticated = true
                }
            )
            .store(in: &cancellables)
    }

    private func storeTokens() {
        // Store in Keychain for better security
        if let accessToken = accessToken {
            _ = keychainHelper.save(key: KeychainHelper.accessTokenKey, value: accessToken)
        }
        if let refreshToken = refreshToken {
            _ = keychainHelper.save(key: KeychainHelper.refreshTokenKey, value: refreshToken)
        }
    }

    private func loadStoredTokens() {
        // Load from Keychain
        accessToken = keychainHelper.load(key: KeychainHelper.accessTokenKey)
        refreshToken = keychainHelper.load(key: KeychainHelper.refreshTokenKey)
    }

    private func clearStoredTokens() {
        // Clear from Keychain
        _ = keychainHelper.delete(key: KeychainHelper.accessTokenKey)
        _ = keychainHelper.delete(key: KeychainHelper.refreshTokenKey)
    }

    // MARK: - Public Properties

    var hasValidToken: Bool {
        return accessToken != nil
    }

    func getAccessToken() -> String? {
        return accessToken
    }
}