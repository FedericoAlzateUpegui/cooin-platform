//
//  MainTabView.swift
//  Cooin
//
//  Main tab navigation for authenticated users
//

import SwiftUI

struct MainTabView: View {
    @EnvironmentObject var authManager: AuthenticationManager

    var body: some View {
        TabView {
            DashboardView()
                .tabItem {
                    Image(systemName: "house.fill")
                    Text("Dashboard")
                }

            MatchingView()
                .tabItem {
                    Image(systemName: "heart.fill")
                    Text("Matches")
                }

            AnalyticsView()
                .tabItem {
                    Image(systemName: "chart.bar.fill")
                    Text("Analytics")
                }

            ProfileView()
                .tabItem {
                    Image(systemName: "person.fill")
                    Text("Profile")
                }
        }
        .accentColor(.blue)
    }
}

struct DashboardView: View {
    @EnvironmentObject var authManager: AuthenticationManager
    @EnvironmentObject var apiClient: APIClient
    @State private var analytics: MobileAnalytics?
    @State private var isLoading = true

    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // Welcome section
                    if let user = authManager.currentUser {
                        VStack(alignment: .leading, spacing: 10) {
                            Text("Welcome back,")
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
                            ProgressView("Loading dashboard...")
                                .progressViewStyle(CircularProgressViewStyle())
                        }
                        .frame(height: 200)
                    } else if let analytics = analytics {
                        VStack(spacing: 15) {
                            Text("Platform Overview")
                                .font(.headline)
                                .frame(maxWidth: .infinity, alignment: .leading)

                            LazyVGrid(columns: [
                                GridItem(.flexible()),
                                GridItem(.flexible())
                            ], spacing: 15) {
                                StatCard(
                                    title: "Total Users",
                                    value: "\(analytics.platformStats.totalUsers)",
                                    icon: "person.3.fill",
                                    color: .blue
                                )

                                StatCard(
                                    title: "Active Users",
                                    value: "\(analytics.platformStats.activeUsers)",
                                    icon: "person.fill.checkmark",
                                    color: .green
                                )

                                StatCard(
                                    title: "Loan Requests",
                                    value: "\(analytics.platformStats.loanRequests)",
                                    icon: "doc.text.fill",
                                    color: .orange
                                )

                                StatCard(
                                    title: "Lending Offers",
                                    value: "\(analytics.platformStats.lendingOffers)",
                                    icon: "dollarsign.circle.fill",
                                    color: .purple
                                )
                            }

                            // Financial overview
                            VStack(spacing: 10) {
                                Text("Financial Overview")
                                    .font(.headline)
                                    .frame(maxWidth: .infinity, alignment: .leading)

                                HStack {
                                    FinancialCard(
                                        title: "Avg Loan",
                                        value: analytics.financialOverview.avgLoanAmount
                                    )

                                    FinancialCard(
                                        title: "Total Volume",
                                        value: analytics.financialOverview.totalVolume
                                    )
                                }
                            }
                        }
                        .padding(.horizontal)
                    }

                    // Quick actions
                    VStack(spacing: 15) {
                        Text("Quick Actions")
                            .font(.headline)
                            .frame(maxWidth: .infinity, alignment: .leading)

                        if let user = authManager.currentUser {
                            if user.role == "borrower" {
                                ActionButton(
                                    title: "Find Lenders",
                                    subtitle: "Discover lending opportunities",
                                    icon: "magnifyingglass",
                                    color: .blue
                                ) {
                                    // Action
                                }

                                ActionButton(
                                    title: "Create Loan Request",
                                    subtitle: "Tell us what you need",
                                    icon: "plus.circle.fill",
                                    color: .green
                                ) {
                                    // Action
                                }
                            } else {
                                ActionButton(
                                    title: "Browse Borrowers",
                                    subtitle: "Find investment opportunities",
                                    icon: "person.2.fill",
                                    color: .blue
                                ) {
                                    // Action
                                }

                                ActionButton(
                                    title: "Create Lending Offer",
                                    subtitle: "Set your lending terms",
                                    icon: "dollarsign.circle.fill",
                                    color: .green
                                ) {
                                    // Action
                                }
                            }
                        }
                    }
                    .padding(.horizontal)

                    Spacer(minLength: 100)
                }
                .padding(.top)
            }
            .navigationTitle("Dashboard")
            .refreshable {
                loadAnalytics()
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