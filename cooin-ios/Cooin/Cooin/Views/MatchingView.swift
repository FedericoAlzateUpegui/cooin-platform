//
//  MatchingView.swift
//  Cooin
//
//  Loan matching and browsing view
//

import SwiftUI

struct MatchingView: View {
    @EnvironmentObject var authManager: AuthenticationManager

    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
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
            .navigationTitle("Matches")
        }
    }
}

struct BorrowerMatchingView: View {
    @EnvironmentObject var authManager: AuthenticationManager
    @EnvironmentObject var apiClient: APIClient
    @State private var showingLoanRequestForm = false
    @State private var showingBrowseLenders = false
    @State private var showingMatches = false

    var body: some View {
        VStack(spacing: 20) {
            // Header
            VStack(spacing: 10) {
                Image(systemName: "heart.circle.fill")
                    .font(.system(size: 50))
                    .foregroundColor(.pink)

                Text("Find Your Perfect Lender")
                    .font(.title2)
                    .fontWeight(.bold)
                    .multilineTextAlignment(.center)

                Text("Connect with lenders who match your needs")
                    .font(.body)
                    .foregroundColor(.secondary)
                    .multilineTextAlignment(.center)
            }

            // Action card
            VStack(spacing: 15) {
                Text("Get Started")
                    .font(.headline)

                VStack(spacing: 10) {
                    MatchingActionCard(
                        title: "Create Loan Request",
                        subtitle: "Tell us what you need to borrow",
                        icon: "doc.text.badge.plus",
                        color: .blue
                    ) {
                        showingLoanRequestForm = true
                    }

                    MatchingActionCard(
                        title: "Browse Lenders",
                        subtitle: "Explore available lending offers",
                        icon: "person.2.fill",
                        color: .green
                    ) {
                        showingBrowseLenders = true
                    }

                    MatchingActionCard(
                        title: "View My Matches",
                        subtitle: "See lenders interested in you",
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
    @State private var showingLendingOfferForm = false
    @State private var showingBrowseBorrowers = false
    @State private var showingMatches = false

    var body: some View {
        VStack(spacing: 20) {
            // Header
            VStack(spacing: 10) {
                Image(systemName: "dollarsign.circle.fill")
                    .font(.system(size: 50))
                    .foregroundColor(.green)

                Text("Find Investment Opportunities")
                    .font(.title2)
                    .fontWeight(.bold)
                    .multilineTextAlignment(.center)

                Text("Connect with borrowers who need your support")
                    .font(.body)
                    .foregroundColor(.secondary)
                    .multilineTextAlignment(.center)
            }

            // Action card
            VStack(spacing: 15) {
                Text("Get Started")
                    .font(.headline)

                VStack(spacing: 10) {
                    MatchingActionCard(
                        title: "Create Lending Offer",
                        subtitle: "Set your lending preferences",
                        icon: "plus.circle.fill",
                        color: .blue
                    ) {
                        showingLendingOfferForm = true
                    }

                    MatchingActionCard(
                        title: "Browse Borrowers",
                        subtitle: "Explore loan requests",
                        icon: "person.2.fill",
                        color: .green
                    ) {
                        showingBrowseBorrowers = true
                    }

                    MatchingActionCard(
                        title: "View My Matches",
                        subtitle: "See borrowers matched to you",
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

struct LoanRequestFormView: View {
    @Environment(\.dismiss) private var dismiss
    @EnvironmentObject var authManager: AuthenticationManager
    @EnvironmentObject var apiClient: APIClient
    @State private var loanAmount = ""
    @State private var purpose = "home_improvement"
    @State private var termMonths = "36"
    @State private var maxRate = ""
    @State private var description = ""
    @State private var isLoading = false
    @State private var errorMessage: String?

    let purposes = [
        ("home_improvement", "Home Improvement"),
        ("debt_consolidation", "Debt Consolidation"),
        ("education", "Education"),
        ("business", "Business"),
        ("medical", "Medical"),
        ("other", "Other")
    ]

    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Loan Details")) {
                    HStack {
                        Text("Amount")
                        Spacer()
                        TextField("25000", text: $loanAmount)
                            .keyboardType(.numberPad)
                            .multilineTextAlignment(.trailing)
                    }

                    Picker("Purpose", selection: $purpose) {
                        ForEach(purposes, id: \.0) { value, label in
                            Text(label).tag(value)
                        }
                    }

                    HStack {
                        Text("Term (months)")
                        Spacer()
                        TextField("36", text: $termMonths)
                            .keyboardType(.numberPad)
                            .multilineTextAlignment(.trailing)
                    }

                    HStack {
                        Text("Max Interest Rate (%)")
                        Spacer()
                        TextField("8.5", text: $maxRate)
                            .keyboardType(.decimalPad)
                            .multilineTextAlignment(.trailing)
                    }
                }

                Section(header: Text("Description")) {
                    TextEditor(text: $description)
                        .frame(height: 100)
                }
            }
            .navigationTitle("Loan Request")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Create") {
                        createLoanRequest()
                    }
                    .disabled(loanAmount.isEmpty || maxRate.isEmpty || isLoading)
                }
            }
        }
    }

    private func createLoanRequest() {
        guard let token = authManager.getAccessToken(),
              let amount = Double(loanAmount),
              let termMonthsInt = Int(termMonths),
              let maxRateDouble = Double(maxRate) else { return }

        isLoading = true
        errorMessage = nil

        // In a real implementation, this would call apiClient.createLoanRequest
        // For now, we'll simulate success
        DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
            self.isLoading = false
            self.dismiss()
        }
    }
}

struct LendingOfferFormView: View {
    @Environment(\.dismiss) private var dismiss
    @EnvironmentObject var authManager: AuthenticationManager
    @EnvironmentObject var apiClient: APIClient
    @State private var availableAmount = ""
    @State private var minAmount = ""
    @State private var maxAmount = ""
    @State private var interestRate = ""
    @State private var preferredTerms = "36"
    @State private var isLoading = false
    @State private var errorMessage: String?

    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Lending Terms")) {
                    HStack {
                        Text("Available Amount")
                        Spacer()
                        TextField("100000", text: $availableAmount)
                            .keyboardType(.numberPad)
                            .multilineTextAlignment(.trailing)
                    }

                    HStack {
                        Text("Min Loan Amount")
                        Spacer()
                        TextField("10000", text: $minAmount)
                            .keyboardType(.numberPad)
                            .multilineTextAlignment(.trailing)
                    }

                    HStack {
                        Text("Max Loan Amount")
                        Spacer()
                        TextField("50000", text: $maxAmount)
                            .keyboardType(.numberPad)
                            .multilineTextAlignment(.trailing)
                    }

                    HStack {
                        Text("Interest Rate (%)")
                        Spacer()
                        TextField("7.5", text: $interestRate)
                            .keyboardType(.decimalPad)
                            .multilineTextAlignment(.trailing)
                    }

                    HStack {
                        Text("Preferred Term (months)")
                        Spacer()
                        TextField("36", text: $preferredTerms)
                            .keyboardType(.numberPad)
                            .multilineTextAlignment(.trailing)
                    }
                }
            }
            .navigationTitle("Lending Offer")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Create") {
                        createLendingOffer()
                    }
                    .disabled(availableAmount.isEmpty || interestRate.isEmpty || isLoading)
                }
            }
        }
    }

    private func createLendingOffer() {
        guard let token = authManager.getAccessToken(),
              let availableAmountDouble = Double(availableAmount),
              let minAmountDouble = Double(minAmount),
              let maxAmountDouble = Double(maxAmount),
              let interestRateDouble = Double(interestRate),
              let preferredTermsInt = Int(preferredTerms) else { return }

        isLoading = true
        errorMessage = nil

        // In a real implementation, this would call apiClient.createLendingOffer
        // For now, we'll simulate success
        DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
            self.isLoading = false
            self.dismiss()
        }
    }
}

struct BrowseLendersView: View {
    @Environment(\.dismiss) private var dismiss
    @EnvironmentObject var authManager: AuthenticationManager
    @EnvironmentObject var apiClient: APIClient
    @State private var lenders: [LenderProfile] = []
    @State private var isLoading = true

    var body: some View {
        NavigationView {
            ScrollView {
                LazyVStack(spacing: 15) {
                    if isLoading {
                        ProgressView("Loading lenders...")
                            .frame(height: 200)
                    } else if lenders.isEmpty {
                        VStack(spacing: 20) {
                            Image(systemName: "person.2.slash")
                                .font(.system(size: 50))
                                .foregroundColor(.gray)

                            Text("No Lenders Available")
                                .font(.title2)
                                .fontWeight(.bold)

                            Text("Check back later for new lending opportunities")
                                .font(.body)
                                .foregroundColor(.secondary)
                                .multilineTextAlignment(.center)
                        }
                        .frame(height: 200)
                    } else {
                        ForEach(lenders, id: \.id) { lender in
                            LenderCard(lender: lender)
                        }
                    }
                }
                .padding()
            }
            .navigationTitle("Browse Lenders")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
                        dismiss()
                    }
                }
            }
        }
        .onAppear {
            loadLenders()
        }
    }

    private func loadLenders() {
        // Simulate loading lenders
        DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
            self.lenders = [
                LenderProfile(id: 1, username: "investor_pro", availableAmount: "$50,000", interestRate: "6.5%", minLoan: "$5,000", maxLoan: "$25,000"),
                LenderProfile(id: 2, username: "capital_builder", availableAmount: "$100,000", interestRate: "7.2%", minLoan: "$10,000", maxLoan: "$50,000"),
                LenderProfile(id: 3, username: "loan_helper", availableAmount: "$25,000", interestRate: "8.0%", minLoan: "$2,500", maxLoan: "$15,000")
            ]
            self.isLoading = false
        }
    }
}

struct BrowseBorrowersView: View {
    @Environment(\.dismiss) private var dismiss
    @EnvironmentObject var authManager: AuthenticationManager
    @EnvironmentObject var apiClient: APIClient
    @State private var borrowers: [BorrowerRequest] = []
    @State private var isLoading = true

    var body: some View {
        NavigationView {
            ScrollView {
                LazyVStack(spacing: 15) {
                    if isLoading {
                        ProgressView("Loading loan requests...")
                            .frame(height: 200)
                    } else if borrowers.isEmpty {
                        VStack(spacing: 20) {
                            Image(systemName: "doc.text.slash")
                                .font(.system(size: 50))
                                .foregroundColor(.gray)

                            Text("No Loan Requests")
                                .font(.title2)
                                .fontWeight(.bold)

                            Text("Check back later for new borrower requests")
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
            .navigationTitle("Browse Borrowers")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
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
    let userRole: String
    @State private var matches: [MatchProfile] = []
    @State private var isLoading = true

    var body: some View {
        NavigationView {
            ScrollView {
                LazyVStack(spacing: 15) {
                    if isLoading {
                        ProgressView("Loading matches...")
                            .frame(height: 200)
                    } else if matches.isEmpty {
                        VStack(spacing: 20) {
                            Image(systemName: "heart.slash")
                                .font(.system(size: 50))
                                .foregroundColor(.gray)

                            Text("No Matches Yet")
                                .font(.title2)
                                .fontWeight(.bold)

                            Text("Complete your profile to get better matches")
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
            .navigationTitle("My Matches")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
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

    var body: some View {
        VStack(spacing: 12) {
            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    Text("@\(lender.username)")
                        .font(.headline)
                        .fontWeight(.semibold)

                    Text("Available: \(lender.availableAmount)")
                        .font(.subheadline)
                        .foregroundColor(.green)
                }

                Spacer()

                VStack(alignment: .trailing, spacing: 4) {
                    Text("\(lender.interestRate)")
                        .font(.title2)
                        .fontWeight(.bold)
                        .foregroundColor(.blue)

                    Text("Interest Rate")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }

            HStack {
                Text("Range: \(lender.minLoan) - \(lender.maxLoan)")
                    .font(.caption)
                    .foregroundColor(.secondary)

                Spacer()

                Button("Contact") {
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

    var body: some View {
        VStack(spacing: 12) {
            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    Text("@\(borrower.username)")
                        .font(.headline)
                        .fontWeight(.semibold)

                    Text("Seeking: \(borrower.amount)")
                        .font(.subheadline)
                        .foregroundColor(.orange)
                }

                Spacer()

                VStack(alignment: .trailing, spacing: 4) {
                    Text("≤\(borrower.maxRate)")
                        .font(.title2)
                        .fontWeight(.bold)
                        .foregroundColor(.green)

                    Text("Max Rate")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }

            HStack {
                Text("\(borrower.purpose) • \(borrower.term)")
                    .font(.caption)
                    .foregroundColor(.secondary)

                Spacer()

                Button("Make Offer") {
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

    var body: some View {
        VStack(spacing: 12) {
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

                    Text("Match")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }

            HStack {
                ProgressView(value: Double(match.matchPercentage), total: 100)
                    .progressViewStyle(LinearProgressViewStyle(tint: .pink))

                Spacer()

                Button("Connect") {
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