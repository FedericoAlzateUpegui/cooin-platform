//
//  LoanRequestFormView.swift
//  CooinNew
//
//  Loan request creation form
//

import SwiftUI

struct LoanRequestFormView: View {
    @Environment(\.dismiss) private var dismiss
    @ObservedObject var languageManager = LanguageManager.shared
    @State private var loanAmount = ""
    @State private var loanPurpose = ""
    @State private var repaymentPeriod = 12

    var body: some View {
        Text("").hidden().id(languageManager.refreshTrigger)
        NavigationView {
            Form {
                Section(header: Text("loan_form.details_header".localized)) {
                    TextField("loan_form.amount_placeholder".localized, text: $loanAmount)
                        .keyboardType(.decimalPad)

                    TextField("loan_form.purpose_placeholder".localized, text: $loanPurpose)

                    Stepper("loan_form.repayment_period".localized + ": \(repaymentPeriod) " + "loan_form.months".localized, value: $repaymentPeriod, in: 1...60)
                }

                Section {
                    Button(action: {
                        // TODO: Submit loan request
                        dismiss()
                    }) {
                        Text("loan_form.submit_request".localized)
                            .frame(maxWidth: .infinity)
                            .foregroundColor(.white)
                            .padding()
                            .background(Color.blue)
                            .cornerRadius(10)
                    }
                    .listRowBackground(Color.clear)
                }
            }
            .navigationTitle("loan_form.navigation_title".localized)
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
    LoanRequestFormView()
}
