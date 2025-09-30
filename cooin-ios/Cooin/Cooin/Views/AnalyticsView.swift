//
//  AnalyticsView.swift
//  Cooin
//
//  Analytics and insights view
//

import SwiftUI

struct AnalyticsView: View {
    @EnvironmentObject var authManager: AuthenticationManager
    @EnvironmentObject var apiClient: APIClient
    @State private var analytics: MobileAnalytics?
    @State private var isLoading = true

    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    if isLoading {
                        VStack {
                            ProgressView("Loading analytics...")
                                .progressViewStyle(CircularProgressViewStyle())
                        }
                        .frame(height: 200)
                    } else if let analytics = analytics {
                        // Platform Stats Section
                        VStack(spacing: 15) {
                            SectionHeader(title: "Platform Statistics", icon: "chart.bar.fill")

                            LazyVGrid(columns: [
                                GridItem(.flexible()),
                                GridItem(.flexible())
                            ], spacing: 15) {
                                AnalyticsCard(
                                    title: "Total Users",
                                    value: "\(analytics.platformStats.totalUsers)",
                                    change: "+\(String(format: "%.1f", analytics.growthTrends.userGrowth))%",
                                    isPositive: analytics.growthTrends.userGrowth > 0,
                                    icon: "person.3.fill",
                                    color: .blue
                                )

                                AnalyticsCard(
                                    title: "Active Users",
                                    value: "\(analytics.platformStats.activeUsers)",
                                    change: "+\(String(format: "%.1f", analytics.growthTrends.activityGrowth))%",
                                    isPositive: analytics.growthTrends.activityGrowth > 0,
                                    icon: "person.fill.checkmark",
                                    color: .green
                                )

                                AnalyticsCard(
                                    title: "Loan Requests",
                                    value: "\(analytics.platformStats.loanRequests)",
                                    change: "This month",
                                    isPositive: true,
                                    icon: "doc.text.fill",
                                    color: .orange
                                )

                                AnalyticsCard(
                                    title: "Lending Offers",
                                    value: "\(analytics.platformStats.lendingOffers)",
                                    change: "Available",
                                    isPositive: true,
                                    icon: "dollarsign.circle.fill",
                                    color: .purple
                                )
                            }
                        }

                        // Financial Overview Section
                        VStack(spacing: 15) {
                            SectionHeader(title: "Financial Overview", icon: "chart.line.uptrend.xyaxis")

                            HStack(spacing: 15) {
                                FinancialOverviewCard(
                                    title: "Average Loan Amount",
                                    value: analytics.financialOverview.avgLoanAmount,
                                    subtitle: "Typical loan size",
                                    color: .blue
                                )

                                FinancialOverviewCard(
                                    title: "Total Volume",
                                    value: analytics.financialOverview.totalVolume,
                                    subtitle: "Platform volume",
                                    color: .green
                                )
                            }
                        }

                        // Insights Section
                        VStack(spacing: 15) {
                            SectionHeader(title: "Insights", icon: "lightbulb.fill")

                            VStack(spacing: 10) {
                                InsightCard(
                                    title: "Growing Community",
                                    description: "User growth is up \(String(format: "%.1f", analytics.growthTrends.userGrowth))% this month",
                                    icon: "arrow.up.circle.fill",
                                    color: .green
                                )

                                InsightCard(
                                    title: "Active Marketplace",
                                    description: "High activity with \(analytics.platformStats.activeUsers) active users",
                                    icon: "chart.bar.fill",
                                    color: .blue
                                )

                                InsightCard(
                                    title: "Balanced Platform",
                                    description: "Good balance between borrowers and lenders",
                                    icon: "scale.3d",
                                    color: .purple
                                )
                            }
                        }
                    } else {
                        VStack(spacing: 20) {
                            Image(systemName: "chart.bar.xaxis")
                                .font(.system(size: 50))
                                .foregroundColor(.gray)

                            Text("Analytics Unavailable")
                                .font(.title2)
                                .fontWeight(.bold)

                            Text("Unable to load analytics data")
                                .font(.body)
                                .foregroundColor(.secondary)

                            Button("Retry") {
                                loadAnalytics()
                            }
                            .buttonStyle(.borderedProminent)
                        }
                    }

                    Spacer(minLength: 100)
                }
                .padding()
            }
            .navigationTitle("Analytics")
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

        isLoading = true
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

struct SectionHeader: View {
    let title: String
    let icon: String

    var body: some View {
        HStack {
            Image(systemName: icon)
                .foregroundColor(.blue)
            Text(title)
                .font(.headline)
                .fontWeight(.semibold)
            Spacer()
        }
    }
}

struct AnalyticsCard: View {
    let title: String
    let value: String
    let change: String
    let isPositive: Bool
    let icon: String
    let color: Color

    var body: some View {
        VStack(spacing: 8) {
            HStack {
                Image(systemName: icon)
                    .font(.title3)
                    .foregroundColor(color)
                Spacer()
                Image(systemName: isPositive ? "arrow.up" : "arrow.down")
                    .font(.caption)
                    .foregroundColor(isPositive ? .green : .red)
            }

            VStack(alignment: .leading, spacing: 4) {
                Text(value)
                    .font(.title2)
                    .fontWeight(.bold)
                    .foregroundColor(.primary)

                Text(title)
                    .font(.caption)
                    .foregroundColor(.secondary)

                Text(change)
                    .font(.caption2)
                    .foregroundColor(isPositive ? .green : .red)
            }
            .frame(maxWidth: .infinity, alignment: .leading)
        }
        .padding()
        .background(Color.gray.opacity(0.1))
        .cornerRadius(12)
    }
}

struct FinancialOverviewCard: View {
    let title: String
    let value: String
    let subtitle: String
    let color: Color

    var body: some View {
        VStack(spacing: 8) {
            Text(title)
                .font(.caption)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)

            Text(value)
                .font(.title2)
                .fontWeight(.bold)
                .foregroundColor(color)

            Text(subtitle)
                .font(.caption2)
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(color.opacity(0.1))
        .cornerRadius(12)
    }
}

struct InsightCard: View {
    let title: String
    let description: String
    let icon: String
    let color: Color

    var body: some View {
        HStack(spacing: 12) {
            Image(systemName: icon)
                .font(.title2)
                .foregroundColor(color)
                .frame(width: 30)

            VStack(alignment: .leading, spacing: 2) {
                Text(title)
                    .font(.subheadline)
                    .fontWeight(.semibold)
                    .foregroundColor(.primary)

                Text(description)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }

            Spacer()
        }
        .padding()
        .background(Color.white)
        .overlay(
            RoundedRectangle(cornerRadius: 12)
                .stroke(color.opacity(0.2), lineWidth: 1)
        )
        .cornerRadius(12)
    }
}

#Preview {
    AnalyticsView()
        .environmentObject(AuthenticationManager())
        .environmentObject(APIClient())
}