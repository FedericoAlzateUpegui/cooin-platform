//
//  BrowseLendersView.swift
//  CooinNew
//
//  Browse available lenders
//

import SwiftUI

struct BrowseLendersView: View {
    @Environment(\.dismiss) private var dismiss
    @ObservedObject var languageManager = LanguageManager.shared

    var body: some View {
        Text("").hidden().id(languageManager.refreshTrigger)
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // Placeholder content
                    VStack(spacing: 15) {
                        Image(systemName: "person.2.fill")
                            .font(.system(size: 60))
                            .foregroundColor(.green)

                        Text("browse_lenders.title".localized)
                            .font(.title2)
                            .fontWeight(.bold)

                        Text("browse_lenders.description".localized)
                            .font(.body)
                            .foregroundColor(.secondary)
                            .multilineTextAlignment(.center)
                    }
                    .padding()

                    // TODO: Add lender list here
                    Text("browse_lenders.no_lenders".localized)
                        .foregroundColor(.secondary)
                        .padding()

                    Spacer()
                }
                .padding()
            }
            .navigationTitle("browse_lenders.navigation_title".localized)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("common.done".localized) {
                        dismiss()
                    }
                }
            }
        }
    }
}

#Preview {
    BrowseLendersView()
}
