//
//  AnalyticsView.swift
//  Cooin
//
//  Analytics and insights view
//

import SwiftUI
import Combine

struct AnalyticsView: View {
    @EnvironmentObject var authManager: AuthenticationManager
    @EnvironmentObject var apiClient: APIClient
    @ObservedObject var languageManager = LanguageManager.shared
    @State private var analytics: MobileAnalytics?
    @State private var isLoading = true

    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // Hidden view to trigger refresh on language change
                    Text("").hidden().id(languageManager.refreshTrigger)

                    if isLoading {
                        VStack {
                            ProgressView("analytics.loading".localized)
                                .progressViewStyle(CircularProgressViewStyle())
                        }
                        .frame(height: 200)
                    } else if let analytics = analytics {
                        // Platform Stats Section
                        VStack(spacing: 15) {
                            SectionHeader(title: "analytics.platform_statistics".localized, icon: "chart.bar.fill")

                            LazyVGrid(columns: [
                                GridItem(.flexible()),
                                GridItem(.flexible())
                            ], spacing: 15) {
                                AnalyticsCard(
                                    title: "analytics.total_users".localized,
                                    value: "\(analytics.platformStats.totalUsers)",
                                    change: "+\(String(format: "%.1f", analytics.growthTrends.userGrowth))%",
                                    isPositive: analytics.growthTrends.userGrowth > 0,
                                    icon: "person.3.fill",
                                    color: .blue
                                )

                                AnalyticsCard(
                                    title: "analytics.active_users".localized,
                                    value: "\(analytics.platformStats.activeUsers)",
                                    change: "+\(String(format: "%.1f", analytics.growthTrends.activityGrowth))%",
                                    isPositive: analytics.growthTrends.activityGrowth > 0,
                                    icon: "person.fill.checkmark",
                                    color: .green
                                )

                                AnalyticsCard(
                                    title: "analytics.loan_requests".localized,
                                    value: "\(analytics.platformStats.loanRequests)",
                                    change: "analytics.this_month".localized,
                                    isPositive: true,
                                    icon: "doc.text.fill",
                                    color: .orange
                                )

                                AnalyticsCard(
                                    title: "analytics.lending_offers".localized,
                                    value: "\(analytics.platformStats.lendingOffers)",
                                    change: "analytics.available".localized,
                                    isPositive: true,
                                    icon: "dollarsign.circle.fill",
                                    color: .purple
                                )
                            }
                        }

                        // Financial Overview Section
                        VStack(spacing: 15) {
                            SectionHeader(title: "analytics.financial_overview".localized, icon: "chart.line.uptrend.xyaxis")

                            HStack(spacing: 15) {
                                FinancialOverviewCard(
                                    title: "analytics.avg_loan_amount".localized,
                                    value: analytics.financialOverview.avgLoanAmount,
                                    subtitle: "analytics.typical_loan_size".localized,
                                    color: .blue
                                )

                                FinancialOverviewCard(
                                    title: "analytics.total_volume".localized,
                                    value: analytics.financialOverview.totalVolume,
                                    subtitle: "analytics.platform_volume".localized,
                                    color: .green
                                )
                            }
                        }

                        // Insights Section
                        VStack(spacing: 15) {
                            SectionHeader(title: "analytics.insights".localized, icon: "lightbulb.fill")

                            VStack(spacing: 10) {
                                InsightCard(
                                    title: "analytics.growing_community".localized,
                                    description: String(format: "analytics.user_growth_description".localized, String(format: "%.1f", analytics.growthTrends.userGrowth)),
                                    icon: "arrow.up.circle.fill",
                                    color: .green
                                )

                                InsightCard(
                                    title: "analytics.active_marketplace".localized,
                                    description: String(format: "analytics.active_marketplace_description".localized, "\(analytics.platformStats.activeUsers)"),
                                    icon: "chart.bar.fill",
                                    color: .blue
                                )

                                InsightCard(
                                    title: "analytics.balanced_platform".localized,
                                    description: "analytics.balanced_platform_description".localized,
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

                            Text("analytics.unavailable".localized)
                                .font(.title2)
                                .fontWeight(.bold)

                            Text("analytics.unable_to_load".localized)
                                .font(.body)
                                .foregroundColor(.secondary)

                            Button("analytics.retry".localized) {
                                loadAnalytics()
                            }
                            .buttonStyle(.borderedProminent)
                        }
                    }

                    Spacer(minLength: 100)
                }
                .padding()
            }
            .navigationTitle("analytics.title".localized)
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