//
//  MainTabView.swift
//  Cooin
//
//  Main tab navigation for authenticated users
//

import SwiftUI
import Combine

struct MainTabView: View {
    @EnvironmentObject var authManager: AuthenticationManager
    @ObservedObject var languageManager = LanguageManager.shared

    var body: some View {
        TabView {
            DashboardView()
                .tabItem {
                    Image(systemName: "house.fill")
                    Text("dashboard.title".localized)
                }
                .id(languageManager.refreshTrigger)

            MatchingView()
                .tabItem {
                    Image(systemName: "heart.fill")
                    Text("dashboard.matching".localized)
                }
                .id(languageManager.refreshTrigger)

            AnalyticsView()
                .tabItem {
                    Image(systemName: "chart.bar.fill")
                    Text("dashboard.analytics".localized)
                }
                .id(languageManager.refreshTrigger)

            ProfileView()
                .tabItem {
                    Image(systemName: "person.fill")
                    Text("dashboard.profile".localized)
                }
                .id(languageManager.refreshTrigger)
        }
        .accentColor(.blue)
    }
}

struct DashboardView: View {
    @EnvironmentObject var authManager: AuthenticationManager
    @EnvironmentObject var apiClient: APIClient
    @ObservedObject var languageManager = LanguageManager.shared
    @State private var analytics: MobileAnalytics?
    @State private var isLoading = true
    @State private var showingBrowseBorrowers = false
    @State private var showingFindLenders = false
    @State private var showingCreateLoanRequest = false
    @State private var showingCreateLendingOffer = false

    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // Hidden view to trigger refresh on language change
                    Text("").hidden().id(languageManager.refreshTrigger)

                    // Welcome section
                    if let user = authManager.currentUser {
                        VStack(alignment: .leading, spacing: 10) {
                            Text("dashboard.welcome".localized)
                                .font(.title2)
                                .foregroundColor(.secondary)

                            Text(user.username)
                                .font(.title)
                                .fontWeight(.bold)
                                .foregroundColor(.primary)
                        }
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .padding(.horizontal)
                    }

                    // Quick stats
                    if isLoading {
                        VStack {
                            ProgressView("loading.please_wait".localized)
                                .progressViewStyle(CircularProgressViewStyle())
                        }
                        .frame(height: 200)
                    } else if let analytics = analytics {
                        VStack(spacing: 15) {
                            Text("dashboard.platform_overview".localized)
                                .font(.headline)
                                .frame(maxWidth: .infinity, alignment: .leading)

                            LazyVGrid(columns: [
                                GridItem(.flexible()),
                                GridItem(.flexible())
                            ], spacing: 15) {
                                StatCard(
                                    title: "dashboard.total_users".localized,
                                    value: "\(analytics.platformStats.totalUsers)",
                                    icon: "person.3.fill",
                                    color: .blue
                                )

                                StatCard(
                                    title: "dashboard.active_users".localized,
                                    value: "\(analytics.platformStats.activeUsers)",
                                    icon: "person.fill.checkmark",
                                    color: .green
                                )

                                StatCard(
                                    title: "dashboard.loan_requests".localized,
                                    value: "\(analytics.platformStats.loanRequests)",
                                    icon: "doc.text.fill",
                                    color: .orange
                                )

                                StatCard(
                                    title: "dashboard.lending_offers".localized,
                                    value: "\(analytics.platformStats.lendingOffers)",
                                    icon: "dollarsign.circle.fill",
                                    color: .purple
                                )
                            }

                            // Financial overview
                            VStack(spacing: 10) {
                                Text("dashboard.financial_overview".localized)
                                    .font(.headline)
                                    .frame(maxWidth: .infinity, alignment: .leading)

                                HStack {
                                    FinancialCard(
                                        title: "dashboard.avg_loan".localized,
                                        value: analytics.financialOverview.avgLoanAmount
                                    )

                                    FinancialCard(
                                        title: "dashboard.total_volume".localized,
                                        value: analytics.financialOverview.totalVolume
                                    )
                                }
                            }
                        }
                        .padding(.horizontal)
                    }

                    // Quick actions
                    VStack(spacing: 15) {
                        Text("dashboard.quick_actions".localized)
                            .font(.headline)
                            .frame(maxWidth: .infinity, alignment: .leading)

                        if let user = authManager.currentUser {
                            if user.role == "borrower" {
                                ActionButton(
                                    title: "dashboard.find_lenders".localized,
                                    subtitle: "dashboard.find_lenders_subtitle".localized,
                                    icon: "magnifyingglass",
                                    color: .blue
                                ) {
                                    showingFindLenders = true
                                }

                                ActionButton(
                                    title: "dashboard.create_loan_request".localized,
                                    subtitle: "dashboard.create_loan_request_subtitle".localized,
                                    icon: "plus.circle.fill",
                                    color: .green
                                ) {
                                    showingCreateLoanRequest = true
                                }
                            } else {
                                ActionButton(
                                    title: "dashboard.browse_borrowers".localized,
                                    subtitle: "dashboard.browse_borrowers_subtitle".localized,
                                    icon: "person.2.fill",
                                    color: .blue
                                ) {
                                    showingBrowseBorrowers = true
                                }

                                ActionButton(
                                    title: "dashboard.create_lending_offer".localized,
                                    subtitle: "dashboard.create_lending_offer_subtitle".localized,
                                    icon: "dollarsign.circle.fill",
                                    color: .green
                                ) {
                                    showingCreateLendingOffer = true
                                }
                            }
                        }
                    }
                    .padding(.horizontal)

                    Spacer(minLength: 100)
                }
                .padding(.top)
            }
            .navigationTitle("dashboard.title".localized)
            .refreshable {
                loadAnalytics()
            }
            .alert("Browse Borrowers", isPresented: $showingBrowseBorrowers) {
                Button("OK") { }
            } message: {
                Text("This feature is coming soon! You'll be able to browse and connect with borrowers looking for loans.")
            }
            .alert("Find Lenders", isPresented: $showingFindLenders) {
                Button("OK") { }
            } message: {
                Text("This feature is coming soon! You'll be able to search and connect with lenders offering loans.")
            }
            .alert("Create Loan Request", isPresented: $showingCreateLoanRequest) {
                Button("OK") { }
            } message: {
                Text("This feature is coming soon! You'll be able to create and submit loan requests.")
            }
            .alert("Create Lending Offer", isPresented: $showingCreateLendingOffer) {
                Button("OK") { }
            } message: {
                Text("This feature is coming soon! You'll be able to create and publish lending offers.")
            }
        }
        .onAppear {
            loadAnalytics()
        }
    }

    private func loadAnalytics() {
        guard let token = authManager.getAccessToken() else { return }

        apiClient.getMobileAnalytics(token: token)
            .receive(on: DispatchQueue.main)
            .sink(
                receiveCompletion: { completion in
                    self.isLoading = false
                    if case .failure(let error) = completion {
                        print("Failed to load analytics: \(error)")
                    }
                },
                receiveValue: { analytics in
                    self.analytics = analytics
                    self.isLoading = false
                }
            )
            .store(in: &apiClient.cancellables)
    }
}

struct StatCard: View {
    let title: String
    let value: String
    let icon: String
    let color: Color

    var body: some View {
        VStack(spacing: 8) {
            Image(systemName: icon)
                .font(.title2)
                .foregroundColor(color)

            Text(value)
                .font(.title2)
                .fontWeight(.bold)
                .foregroundColor(.primary)

            Text(title)
                .font(.caption)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)
        }
        .frame(height: 80)
        .frame(maxWidth: .infinity)
        .background(Color.gray.opacity(0.1))
        .cornerRadius(12)
    }
}

struct FinancialCard: View {
    let title: String
    let value: String

    var body: some View {
        VStack(spacing: 5) {
            Text(title)
                .font(.caption)
                .foregroundColor(.secondary)

            Text(value)
                .font(.title3)
                .fontWeight(.semibold)
                .foregroundColor(.primary)
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(Color.blue.opacity(0.1))
        .cornerRadius(12)
    }
}

struct ActionButton: View {
    let title: String
    let subtitle: String
    let icon: String
    let color: Color
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            HStack(spacing: 15) {
                Image(systemName: icon)
                    .font(.title2)
                    .foregroundColor(color)
                    .frame(width: 30)

                VStack(alignment: .leading, spacing: 2) {
                    Text(title)
                        .font(.headline)
                        .foregroundColor(.primary)

                    Text(subtitle)
                        .font(.caption)
                        .foregroundColor(.secondary)
                }

                Spacer()

                Image(systemName: "chevron.right")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            .padding()
            .background(Color.white)
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(Color.gray.opacity(0.2), lineWidth: 1)
            )
            .cornerRadius(12)
        }
        .buttonStyle(PlainButtonStyle())
    }
}

#Preview {
    MainTabView()
        .environmentObject(AuthenticationManager())
        .environmentObject(APIClient())
}