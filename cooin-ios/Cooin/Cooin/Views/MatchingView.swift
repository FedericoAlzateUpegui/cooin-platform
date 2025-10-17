//
//  MatchingView.swift
//  Cooin
//
//  Loan matching and browsing view
//

import SwiftUI

struct MatchingView: View {
    @EnvironmentObject var authManager: AuthenticationManager
    @ObservedObject var languageManager = LanguageManager.shared

    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // Hidden view to trigger refresh on language change
                    Text("").hidden().id(languageManager.refreshTrigger)

                    if let user = authManager.currentUser {
                        if user.role == "borrower" {
                            BorrowerMatchingView()
                        } else {
                            LenderMatchingView()
                        }
                    }
                }
                .padding()
            }
            .navigationTitle("matching.title".localized)
        }
    }
}

struct BorrowerMatchingView: View {
    @EnvironmentObject var authManager: AuthenticationManager
    @EnvironmentObject var apiClient: APIClient
    @ObservedObject var languageManager = LanguageManager.shared
    @State private var showingLoanRequestForm = false
    @State private var showingBrowseLenders = false
    @State private var showingMatches = false

    var body: some View {
        VStack(spacing: 20) {
            // Hidden view to trigger refresh on language change
            Text("").hidden().id(languageManager.refreshTrigger)

            // Header
            VStack(spacing: 10) {
                Image(systemName: "heart.circle.fill")
                    .font(.system(size: 50))
                    .foregroundColor(.pink)

                Text("matching.find_perfect_lender".localized)
                    .font(.title2)
                    .fontWeight(.bold)
                    .multilineTextAlignment(.center)

                Text("matching.connect_lenders".localized)
                    .font(.body)
                    .foregroundColor(.secondary)
                    .multilineTextAlignment(.center)
            }

            // Action card
            VStack(spacing: 15) {
                Text("matching.get_started".localized)
                    .font(.headline)

                VStack(spacing: 10) {
                    MatchingActionCard(
                        title: "matching.create_loan_request".localized,
                        subtitle: "matching.create_loan_request_subtitle".localized,
                        icon: "doc.text.badge.plus",
                        color: .blue
                    ) {
                        showingLoanRequestForm = true
                    }

                    MatchingActionCard(
                        title: "matching.browse_lenders".localized,
                        subtitle: "matching.browse_lenders_subtitle".localized,
                        icon: "person.2.fill",
                        color: .green
                    ) {
                        showingBrowseLenders = true
                    }

                    MatchingActionCard(
                        title: "matching.view_matches".localized,
                        subtitle: "matching.view_matches_lenders_subtitle".localized,
                        icon: "heart.fill",
                        color: .pink
                    ) {
                        showingMatches = true
                    }
                }
            }

            Spacer()
        }
        .sheet(isPresented: $showingLoanRequestForm) {
            LoanRequestFormView()
        }
        .sheet(isPresented: $showingBrowseLenders) {
            BrowseLendersView()
        }
        .sheet(isPresented: $showingMatches) {
            MatchesView(userRole: "borrower")
        }
    }
}

struct LenderMatchingView: View {
    @EnvironmentObject var authManager: AuthenticationManager
    @EnvironmentObject var apiClient: APIClient
    @ObservedObject var languageManager = LanguageManager.shared
    @State private var showingLendingOfferForm = false
    @State private var showingBrowseBorrowers = false
    @State private var showingMatches = false

    var body: some View {
        VStack(spacing: 20) {
            // Hidden view to trigger refresh on language change
            Text("").hidden().id(languageManager.refreshTrigger)

            // Header
            VStack(spacing: 10) {
                Image(systemName: "dollarsign.circle.fill")
                    .font(.system(size: 50))
                    .foregroundColor(.green)

                Text("matching.find_investment_opportunities".localized)
                    .font(.title2)
                    .fontWeight(.bold)
                    .multilineTextAlignment(.center)

                Text("matching.connect_borrowers".localized)
                    .font(.body)
                    .foregroundColor(.secondary)
                    .multilineTextAlignment(.center)
            }

            // Action card
            VStack(spacing: 15) {
                Text("matching.get_started".localized)
                    .font(.headline)

                VStack(spacing: 10) {
                    MatchingActionCard(
                        title: "matching.create_lending_offer".localized,
                        subtitle: "matching.create_lending_offer_subtitle".localized,
                        icon: "plus.circle.fill",
                        color: .blue
                    ) {
                        showingLendingOfferForm = true
                    }

                    MatchingActionCard(
                        title: "matching.browse_borrowers".localized,
                        subtitle: "matching.browse_borrowers_subtitle".localized,
                        icon: "person.2.fill",
                        color: .green
                    ) {
                        showingBrowseBorrowers = true
                    }

                    MatchingActionCard(
                        title: "matching.view_matches".localized,
                        subtitle: "matching.view_matches_borrowers_subtitle".localized,
                        icon: "heart.fill",
                        color: .pink
                    ) {
                        showingMatches = true
                    }
                }
            }

            Spacer()
        }
        .sheet(isPresented: $showingLendingOfferForm) {
            LendingOfferFormView()
        }
        .sheet(isPresented: $showingBrowseBorrowers) {
            BrowseBorrowersView()
        }
        .sheet(isPresented: $showingMatches) {
            MatchesView(userRole: "lender")
        }
    }
}

struct MatchingActionCard: View {
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
                    .stroke(color.opacity(0.3), lineWidth: 2)
            )
            .cornerRadius(12)
        }
        .buttonStyle(PlainButtonStyle())
    }
}

// Note: LoanRequestFormView and BrowseLendersView are defined in separate files

struct BrowseBorrowersView: View {
    @Environment(\.dismiss) private var dismiss
    @EnvironmentObject var authManager: AuthenticationManager
    @EnvironmentObject var apiClient: APIClient
    @ObservedObject var languageManager = LanguageManager.shared
    @State private var borrowers: [BorrowerRequest] = []
    @State private var isLoading = true

    var body: some View {
        NavigationView {
            ScrollView {
                LazyVStack(spacing: 15) {
                    // Hidden view to trigger refresh on language change
                    Text("").hidden().id(languageManager.refreshTrigger)

                    if isLoading {
                        ProgressView("matching.loading_loan_requests".localized)
                            .frame(height: 200)
                    } else if borrowers.isEmpty {
                        VStack(spacing: 20) {
                            Image(systemName: "doc.text.slash")
                                .font(.system(size: 50))
                                .foregroundColor(.gray)

                            Text("matching.no_loan_requests".localized)
                                .font(.title2)
                                .fontWeight(.bold)

                            Text("matching.check_back_later_borrowers".localized)
                                .font(.body)
                                .foregroundColor(.secondary)
                                .multilineTextAlignment(.center)
                        }
                        .frame(height: 200)
                    } else {
                        ForEach(borrowers, id: \.id) { borrower in
                            BorrowerCard(borrower: borrower)
                        }
                    }
                }
                .padding()
            }
            .navigationTitle("matching.browse_borrowers".localized)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("common.done".localized) {
                        dismiss()
                    }
                }
            }
        }
        .onAppear {
            loadBorrowers()
        }
    }

    private func loadBorrowers() {
        // Simulate loading borrowers
        DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
            self.borrowers = [
                BorrowerRequest(id: 1, username: "home_buyer", amount: "$35,000", purpose: "Home Improvement", maxRate: "7.5%", term: "36 months"),
                BorrowerRequest(id: 2, username: "student_grad", amount: "$15,000", purpose: "Education", maxRate: "6.0%", term: "24 months"),
                BorrowerRequest(id: 3, username: "small_biz", amount: "$50,000", purpose: "Business", maxRate: "8.5%", term: "48 months")
            ]
            self.isLoading = false
        }
    }
}

struct MatchesView: View {
    @Environment(\.dismiss) private var dismiss
    @ObservedObject var languageManager = LanguageManager.shared
    let userRole: String
    @State private var matches: [MatchProfile] = []
    @State private var isLoading = true

    var body: some View {
        NavigationView {
            ScrollView {
                LazyVStack(spacing: 15) {
                    // Hidden view to trigger refresh on language change
                    Text("").hidden().id(languageManager.refreshTrigger)

                    if isLoading {
                        ProgressView("matching.loading_matches".localized)
                            .frame(height: 200)
                    } else if matches.isEmpty {
                        VStack(spacing: 20) {
                            Image(systemName: "heart.slash")
                                .font(.system(size: 50))
                                .foregroundColor(.gray)

                            Text("matching.no_matches_yet".localized)
                                .font(.title2)
                                .fontWeight(.bold)

                            Text("matching.complete_profile".localized)
                                .font(.body)
                                .foregroundColor(.secondary)
                                .multilineTextAlignment(.center)
                        }
                        .frame(height: 200)
                    } else {
                        ForEach(matches, id: \.id) { match in
                            MatchCard(match: match, userRole: userRole)
                        }
                    }
                }
                .padding()
            }
            .navigationTitle("matching.my_matches".localized)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("common.done".localized) {
                        dismiss()
                    }
                }
            }
        }
        .onAppear {
            loadMatches()
        }
    }

    private func loadMatches() {
        // Simulate loading matches
        DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
            if userRole == "borrower" {
                self.matches = [
                    MatchProfile(id: 1, username: "investor_match", detail: "Offering $30K at 6.8%", matchPercentage: 95),
                    MatchProfile(id: 2, username: "capital_friend", detail: "Offering $25K at 7.1%", matchPercentage: 87)
                ]
            } else {
                self.matches = [
                    MatchProfile(id: 1, username: "borrower_match", detail: "Seeking $20K for education", matchPercentage: 92),
                    MatchProfile(id: 2, username: "home_seeker", detail: "Seeking $40K for home improvement", matchPercentage: 78)
                ]
            }
            self.isLoading = false
        }
    }
}

// MARK: - Supporting Data Models

struct LenderProfile {
    let id: Int
    let username: String
    let availableAmount: String
    let interestRate: String
    let minLoan: String
    let maxLoan: String
}

struct BorrowerRequest {
    let id: Int
    let username: String
    let amount: String
    let purpose: String
    let maxRate: String
    let term: String
}

struct MatchProfile {
    let id: Int
    let username: String
    let detail: String
    let matchPercentage: Int
}

// MARK: - Supporting Card Views

struct LenderCard: View {
    let lender: LenderProfile
    @ObservedObject var languageManager = LanguageManager.shared

    var body: some View {
        VStack(spacing: 12) {
            // Hidden view to trigger refresh on language change
            Text("").hidden().id(languageManager.refreshTrigger)

            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    Text("@\(lender.username)")
                        .font(.headline)
                        .fontWeight(.semibold)

                    Text("matching.available".localized + ": \(lender.availableAmount)")
                        .font(.subheadline)
                        .foregroundColor(.green)
                }

                Spacer()

                VStack(alignment: .trailing, spacing: 4) {
                    Text("\(lender.interestRate)")
                        .font(.title2)
                        .fontWeight(.bold)
                        .foregroundColor(.blue)

                    Text("matching.interest_rate".localized)
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }

            HStack {
                Text("matching.range".localized + ": \(lender.minLoan) - \(lender.maxLoan)")
                    .font(.caption)
                    .foregroundColor(.secondary)

                Spacer()

                Button("matching.contact".localized) {
                    // Contact action
                }
                .buttonStyle(.borderedProminent)
                .controlSize(.small)
            }
        }
        .padding()
        .background(Color.white)
        .overlay(
            RoundedRectangle(cornerRadius: 12)
                .stroke(Color.blue.opacity(0.2), lineWidth: 1)
        )
        .cornerRadius(12)
    }
}

struct BorrowerCard: View {
    let borrower: BorrowerRequest
    @ObservedObject var languageManager = LanguageManager.shared

    var body: some View {
        VStack(spacing: 12) {
            // Hidden view to trigger refresh on language change
            Text("").hidden().id(languageManager.refreshTrigger)

            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    Text("@\(borrower.username)")
                        .font(.headline)
                        .fontWeight(.semibold)

                    Text("matching.seeking".localized + ": \(borrower.amount)")
                        .font(.subheadline)
                        .foregroundColor(.orange)
                }

                Spacer()

                VStack(alignment: .trailing, spacing: 4) {
                    Text("≤\(borrower.maxRate)")
                        .font(.title2)
                        .fontWeight(.bold)
                        .foregroundColor(.green)

                    Text("matching.max_rate".localized)
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }

            HStack {
                Text("\(borrower.purpose) • \(borrower.term)")
                    .font(.caption)
                    .foregroundColor(.secondary)

                Spacer()

                Button("matching.make_offer".localized) {
                    // Make offer action
                }
                .buttonStyle(.borderedProminent)
                .controlSize(.small)
            }
        }
        .padding()
        .background(Color.white)
        .overlay(
            RoundedRectangle(cornerRadius: 12)
                .stroke(Color.green.opacity(0.2), lineWidth: 1)
        )
        .cornerRadius(12)
    }
}

struct MatchCard: View {
    let match: MatchProfile
    let userRole: String
    @ObservedObject var languageManager = LanguageManager.shared

    var body: some View {
        VStack(spacing: 12) {
            // Hidden view to trigger refresh on language change
            Text("").hidden().id(languageManager.refreshTrigger)

            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    Text("@\(match.username)")
                        .font(.headline)
                        .fontWeight(.semibold)

                    Text(match.detail)
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }

                Spacer()

                VStack(alignment: .trailing, spacing: 4) {
                    Text("\(match.matchPercentage)%")
                        .font(.title2)
                        .fontWeight(.bold)
                        .foregroundColor(.pink)

                    Text("matching.match".localized)
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }

            HStack {
                ProgressView(value: Double(match.matchPercentage), total: 100)
                    .progressViewStyle(LinearProgressViewStyle(tint: .pink))

                Spacer()

                Button("matching.connect".localized) {
                    // Connect action
                }
                .buttonStyle(.borderedProminent)
                .controlSize(.small)
            }
        }
        .padding()
        .background(Color.white)
        .overlay(
            RoundedRectangle(cornerRadius: 12)
                .stroke(Color.pink.opacity(0.2), lineWidth: 1)
        )
        .cornerRadius(12)
    }
}

#Preview {
    MatchingView()
        .environmentObject(AuthenticationManager())
        .environmentObject(APIClient())
}