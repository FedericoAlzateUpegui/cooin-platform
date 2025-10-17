//
//  LendingOfferFormView.swift
//  CooinNew
//
//  Lending offer creation form
//

import SwiftUI

struct LendingOfferFormView: View {
    @Environment(\.dismiss) private var dismiss
    @ObservedObject var languageManager = LanguageManager.shared
    @State private var availableAmount = ""
    @State private var minLoanAmount = ""
    @State private var maxLoanAmount = ""
    @State private var interestRate = ""
    @State private var preferredTermMonths = 36

    var body: some View {
        Text("").hidden().id(languageManager.refreshTrigger)
        NavigationView {
            Form {
                Section(header: Text("lending_offer.details_header".localized)) {
                    TextField("lending_offer.available_amount_placeholder".localized, text: $availableAmount)
                        .keyboardType(.decimalPad)

                    TextField("lending_offer.min_amount_placeholder".localized, text: $minLoanAmount)
                        .keyboardType(.decimalPad)

                    TextField("lending_offer.max_amount_placeholder".localized, text: $maxLoanAmount)
                        .keyboardType(.decimalPad)

                    TextField("lending_offer.interest_rate_placeholder".localized, text: $interestRate)
                        .keyboardType(.decimalPad)

                    Stepper("lending_offer.preferred_term".localized + ": \(preferredTermMonths) " + "lending_offer.months".localized, value: $preferredTermMonths, in: 1...60)
                }

                Section {
                    Button(action: {
                        // TODO: Submit lending offer
                        dismiss()
                    }) {
                        Text("lending_offer.submit_offer".localized)
                            .frame(maxWidth: .infinity)
                            .foregroundColor(.white)
                            .padding()
                            .background(Color.green)
                            .cornerRadius(10)
                    }
                    .listRowBackground(Color.clear)
                }
            }
            .navigationTitle("lending_offer.navigation_title".localized)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("common.cancel".localized) {
                        dismiss()
                    }
                }
            }
        }
    }
}

#Preview {
    LendingOfferFormView()
}
