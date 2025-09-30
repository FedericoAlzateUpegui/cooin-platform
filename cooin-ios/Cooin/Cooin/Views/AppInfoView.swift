//
//  AppInfoView.swift
//  Cooin
//
//  App information and settings view
//

import SwiftUI

struct AppInfoView: View {
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 30) {
                    // App Logo and Info
                    VStack(spacing: 15) {
                        Image(systemName: "dollarsign.circle.fill")
                            .font(.system(size: 80))
                            .foregroundColor(.blue)

                        Text("Cooin")
                            .font(.largeTitle)
                            .fontWeight(.bold)

                        Text("Peer-to-Peer Lending Platform")
                            .font(.subheadline)
                            .foregroundColor(.secondary)

                        Text("Version 1.0.0 (Build 1)")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }

                    // About Section
                    VStack(spacing: 15) {
                        Text("About Cooin")
                            .font(.headline)
                            .frame(maxWidth: .infinity, alignment: .leading)

                        VStack(alignment: .leading, spacing: 12) {
                            Text("Cooin connects borrowers and lenders in a secure, transparent peer-to-peer lending environment.")
                            Text("Our platform facilitates direct lending relationships while ensuring proper verification and security for all users.")
                            Text("Whether you're looking to borrow money for personal needs or lend money for investment returns, Cooin provides the tools and community to make it happen safely.")
                        }
                        .font(.body)
                        .foregroundColor(.secondary)
                    }

                    // Features Section
                    VStack(spacing: 15) {
                        Text("Features")
                            .font(.headline)
                            .frame(maxWidth: .infinity, alignment: .leading)

                        LazyVGrid(columns: [
                            GridItem(.flexible()),
                            GridItem(.flexible())
                        ], spacing: 15) {
                            FeatureCard(
                                icon: "shield.checkered",
                                title: "Secure",
                                description: "Bank-level security"
                            )

                            FeatureCard(
                                icon: "person.2.fill",
                                title: "Peer-to-Peer",
                                description: "Direct connections"
                            )

                            FeatureCard(
                                icon: "chart.line.uptrend.xyaxis",
                                title: "Analytics",
                                description: "Real-time insights"
                            )

                            FeatureCard(
                                icon: "doc.text.magnifyingglass",
                                title: "Verification",
                                description: "Identity & document checks"
                            )
                        }
                    }

                    // Support Section
                    VStack(spacing: 15) {
                        Text("Support & Legal")
                            .font(.headline)
                            .frame(maxWidth: .infinity, alignment: .leading)

                        VStack(spacing: 12) {
                            SupportRow(title: "Terms of Service", icon: "doc.text")
                            SupportRow(title: "Privacy Policy", icon: "hand.raised")
                            SupportRow(title: "Help Center", icon: "questionmark.circle")
                            SupportRow(title: "Contact Support", icon: "envelope")
                            SupportRow(title: "Rate App", icon: "star")
                        }
                    }

                    // Technical Info
                    VStack(spacing: 10) {
                        Text("Technical Information")
                            .font(.headline)
                            .frame(maxWidth: .infinity, alignment: .leading)

                        VStack(alignment: .leading, spacing: 8) {
                            HStack {
                                Text("Backend API:")
                                Spacer()
                                Text("http://192.168.40.34:8000")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }

                            HStack {
                                Text("Framework:")
                                Spacer()
                                Text("SwiftUI")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }

                            HStack {
                                Text("Platform:")
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
            .navigationTitle("About")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
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

    var body: some View {
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

    var body: some View {
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