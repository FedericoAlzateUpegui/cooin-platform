//
//  AppInfoView.swift
//  Cooin
//
//  App information and settings view
//

import SwiftUI

struct AppInfoView: View {
    @Environment(\.dismiss) private var dismiss
    @ObservedObject var languageManager = LanguageManager.shared

    var body: some View {
        Text("").hidden().id(languageManager.refreshTrigger)
        NavigationView {
            ScrollView {
                VStack(spacing: 30) {
                    // App Logo and Info
                    VStack(spacing: 15) {
                        Image(systemName: "dollarsign.circle.fill")
                            .font(.system(size: 80))
                            .foregroundColor(.blue)

                        Text("app_info.app_name".localized)
                            .font(.largeTitle)
                            .fontWeight(.bold)

                        Text("app_info.tagline".localized)
                            .font(.subheadline)
                            .foregroundColor(.secondary)

                        Text("app_info.version".localized)
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }

                    // About Section
                    VStack(spacing: 15) {
                        Text("app_info.about_title".localized)
                            .font(.headline)
                            .frame(maxWidth: .infinity, alignment: .leading)

                        VStack(alignment: .leading, spacing: 12) {
                            Text("app_info.about_description1".localized)
                            Text("app_info.about_description2".localized)
                            Text("app_info.about_description3".localized)
                        }
                        .font(.body)
                        .foregroundColor(.secondary)
                    }

                    // Features Section
                    VStack(spacing: 15) {
                        Text("app_info.features_title".localized)
                            .font(.headline)
                            .frame(maxWidth: .infinity, alignment: .leading)

                        LazyVGrid(columns: [
                            GridItem(.flexible()),
                            GridItem(.flexible())
                        ], spacing: 15) {
                            FeatureCard(
                                icon: "shield.checkered",
                                title: "app_info.feature_secure_title".localized,
                                description: "app_info.feature_secure_desc".localized
                            )

                            FeatureCard(
                                icon: "person.2.fill",
                                title: "app_info.feature_p2p_title".localized,
                                description: "app_info.feature_p2p_desc".localized
                            )

                            FeatureCard(
                                icon: "chart.line.uptrend.xyaxis",
                                title: "app_info.feature_analytics_title".localized,
                                description: "app_info.feature_analytics_desc".localized
                            )

                            FeatureCard(
                                icon: "doc.text.magnifyingglass",
                                title: "app_info.feature_verification_title".localized,
                                description: "app_info.feature_verification_desc".localized
                            )
                        }
                    }

                    // Support Section
                    VStack(spacing: 15) {
                        Text("app_info.support_title".localized)
                            .font(.headline)
                            .frame(maxWidth: .infinity, alignment: .leading)

                        VStack(spacing: 12) {
                            SupportRow(title: "app_info.terms_of_service".localized, icon: "doc.text")
                            SupportRow(title: "app_info.privacy_policy".localized, icon: "hand.raised")
                            SupportRow(title: "app_info.help_center".localized, icon: "questionmark.circle")
                            SupportRow(title: "app_info.contact_support".localized, icon: "envelope")
                            SupportRow(title: "app_info.rate_app".localized, icon: "star")
                        }
                    }

                    // Technical Info
                    VStack(spacing: 10) {
                        Text("app_info.technical_info_title".localized)
                            .font(.headline)
                            .frame(maxWidth: .infinity, alignment: .leading)

                        VStack(alignment: .leading, spacing: 8) {
                            HStack {
                                Text("app_info.backend_api".localized)
                                Spacer()
                                Text("http://192.168.40.34:8000")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }

                            HStack {
                                Text("app_info.framework".localized)
                                Spacer()
                                Text("SwiftUI")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }

                            HStack {
                                Text("app_info.platform".localized)
                                Spacer()
                                Text("iOS 14.0+")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }
                        }
                        .font(.caption)
                    }

                    Spacer(minLength: 50)
                }
                .padding()
            }
            .navigationTitle("app_info.navigation_title".localized)
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

struct FeatureCard: View {
    let icon: String
    let title: String
    let description: String
    @ObservedObject var languageManager = LanguageManager.shared

    var body: some View {
        Text("").hidden().id(languageManager.refreshTrigger)
        VStack(spacing: 8) {
            Image(systemName: icon)
                .font(.title2)
                .foregroundColor(.blue)

            Text(title)
                .font(.headline)
                .fontWeight(.semibold)

            Text(description)
                .font(.caption)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)
        }
        .frame(height: 100)
        .frame(maxWidth: .infinity)
        .padding()
        .background(Color.blue.opacity(0.1))
        .cornerRadius(12)
    }
}

struct SupportRow: View {
    let title: String
    let icon: String
    @ObservedObject var languageManager = LanguageManager.shared

    var body: some View {
        Text("").hidden().id(languageManager.refreshTrigger)
        HStack(spacing: 15) {
            Image(systemName: icon)
                .font(.title3)
                .foregroundColor(.blue)
                .frame(width: 25)

            Text(title)
                .font(.body)

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
}

#Preview {
    AppInfoView()
}