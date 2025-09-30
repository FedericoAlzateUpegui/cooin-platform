//
//  ProfileView.swift
//  Cooin
//
//  User profile and settings view
//

import SwiftUI

struct ProfileView: View {
    @EnvironmentObject var authManager: AuthenticationManager
    @EnvironmentObject var apiClient: APIClient
    @State private var showingImagePicker = false
    @State private var showingEditProfile = false
    @State private var showingSettings = false
    @State private var showingDocumentVerification = false
    @State private var showingAppInfo = false

    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    if let user = authManager.currentUser {
                        // Profile header
                        VStack(spacing: 15) {
                            Button(action: {
                                showingImagePicker = true
                            }) {
                                ZStack {
                                    Circle()
                                        .fill(Color.blue.opacity(0.1))
                                        .frame(width: 100, height: 100)

                                    Image(systemName: "person.fill")
                                        .font(.system(size: 40))
                                        .foregroundColor(.blue)

                                    Circle()
                                        .stroke(Color.blue, lineWidth: 2)
                                        .frame(width: 100, height: 100)

                                    // Camera icon overlay
                                    VStack {
                                        Spacer()
                                        HStack {
                                            Spacer()
                                            Image(systemName: "camera.circle.fill")
                                                .font(.title3)
                                                .foregroundColor(.blue)
                                                .background(Color.white)
                                                .clipShape(Circle())
                                        }
                                    }
                                    .frame(width: 100, height: 100)
                                }
                            }

                            VStack(spacing: 5) {
                                Text(user.username)
                                    .font(.title2)
                                    .fontWeight(.bold)

                                Text(user.email)
                                    .font(.caption)
                                    .foregroundColor(.secondary)

                                RoleBadge(role: user.role)
                            }
                        }

                        // Profile sections
                        VStack(spacing: 15) {
                            // Account section
                            ProfileSection(title: "Account") {
                                ProfileMenuItem(
                                    title: "Edit Profile",
                                    subtitle: "Update your information",
                                    icon: "person.crop.circle",
                                    color: .blue
                                ) {
                                    showingEditProfile = true
                                }

                                ProfileMenuItem(
                                    title: "Verification Status",
                                    subtitle: "Complete your verification",
                                    icon: "checkmark.shield",
                                    color: .green
                                ) {
                                    showingDocumentVerification = true
                                }

                                ProfileMenuItem(
                                    title: "Security",
                                    subtitle: "Password and security settings",
                                    icon: "lock.shield",
                                    color: .orange
                                ) {
                                    // Navigate to security settings
                                }
                            }

                            // Activity section
                            ProfileSection(title: user.role == "borrower" ? "My Borrowing" : "My Lending") {
                                if user.role == "borrower" {
                                    ProfileMenuItem(
                                        title: "Loan Requests",
                                        subtitle: "View your loan applications",
                                        icon: "doc.text",
                                        color: .blue
                                    ) {
                                        // Navigate to loan requests
                                    }

                                    ProfileMenuItem(
                                        title: "Active Loans",
                                        subtitle: "Manage current loans",
                                        icon: "dollarsign.circle",
                                        color: .green
                                    ) {
                                        // Navigate to active loans
                                    }
                                } else {
                                    ProfileMenuItem(
                                        title: "Lending Offers",
                                        subtitle: "Manage your offers",
                                        icon: "plus.circle",
                                        color: .blue
                                    ) {
                                        // Navigate to lending offers
                                    }

                                    ProfileMenuItem(
                                        title: "Active Investments",
                                        subtitle: "Track your investments",
                                        icon: "chart.line.uptrend.xyaxis",
                                        color: .green
                                    ) {
                                        // Navigate to investments
                                    }
                                }

                                ProfileMenuItem(
                                    title: "Transaction History",
                                    subtitle: "View all transactions",
                                    icon: "list.bullet.rectangle",
                                    color: .purple
                                ) {
                                    // Navigate to transaction history
                                }
                            }

                            // Settings section
                            ProfileSection(title: "Settings") {
                                ProfileMenuItem(
                                    title: "Notifications",
                                    subtitle: "Manage notifications",
                                    icon: "bell",
                                    color: .orange
                                ) {
                                    // Navigate to notifications
                                }

                                ProfileMenuItem(
                                    title: "Privacy",
                                    subtitle: "Privacy preferences",
                                    icon: "hand.raised",
                                    color: .blue
                                ) {
                                    // Navigate to privacy settings
                                }

                                ProfileMenuItem(
                                    title: "Help & Support",
                                    subtitle: "Get help and contact us",
                                    icon: "questionmark.circle",
                                    color: .green
                                ) {
                                    showingAppInfo = true
                                }
                            }

                            // Logout section
                            VStack(spacing: 10) {
                                Button(action: {
                                    authManager.logout()
                                }) {
                                    HStack {
                                        Image(systemName: "arrow.right.square")
                                            .font(.title3)
                                            .foregroundColor(.red)

                                        Text("Logout")
                                            .font(.headline)
                                            .foregroundColor(.red)

                                        Spacer()
                                    }
                                    .padding()
                                    .background(Color.red.opacity(0.1))
                                    .cornerRadius(12)
                                }

                                Text("Version 1.0.0")
                                    .font(.caption2)
                                    .foregroundColor(.secondary)
                            }
                        }
                        .padding(.horizontal)
                    }

                    Spacer(minLength: 100)
                }
                .padding(.top)
            }
            .navigationTitle("Profile")
        }
        .sheet(isPresented: $showingImagePicker) {
            ImagePickerView()
        }
        .sheet(isPresented: $showingEditProfile) {
            EditProfileView()
        }
        .sheet(isPresented: $showingDocumentVerification) {
            DocumentVerificationView()
        }
        .sheet(isPresented: $showingAppInfo) {
            AppInfoView()
        }
    }
}

struct RoleBadge: View {
    let role: String

    var roleColor: Color {
        role == "borrower" ? .blue : .green
    }

    var roleText: String {
        role == "borrower" ? "Borrower" : "Lender"
    }

    var body: some View {
        Text(roleText)
            .font(.caption)
            .fontWeight(.semibold)
            .foregroundColor(roleColor)
            .padding(.horizontal, 12)
            .padding(.vertical, 4)
            .background(roleColor.opacity(0.1))
            .cornerRadius(12)
    }
}

struct ProfileSection<Content: View>: View {
    let title: String
    let content: Content

    init(title: String, @ViewBuilder content: () -> Content) {
        self.title = title
        self.content = content()
    }

    var body: some View {
        VStack(spacing: 12) {
            HStack {
                Text(title)
                    .font(.headline)
                    .fontWeight(.semibold)
                Spacer()
            }

            VStack(spacing: 1) {
                content
            }
            .background(Color.white)
            .cornerRadius(12)
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(Color.gray.opacity(0.2), lineWidth: 1)
            )
        }
    }
}

struct ProfileMenuItem: View {
    let title: String
    let subtitle: String
    let icon: String
    let color: Color
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            HStack(spacing: 15) {
                Image(systemName: icon)
                    .font(.title3)
                    .foregroundColor(color)
                    .frame(width: 25)

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
        }
        .buttonStyle(PlainButtonStyle())
    }
}

struct ImagePickerView: View {
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationView {
            VStack(spacing: 30) {
                Text("Update Profile Picture")
                    .font(.title2)
                    .fontWeight(.bold)

                VStack(spacing: 20) {
                    Button(action: {
                        // Take photo with camera
                        dismiss()
                    }) {
                        HStack(spacing: 15) {
                            Image(systemName: "camera")
                                .font(.title2)
                                .foregroundColor(.blue)

                            Text("Take Photo")
                                .font(.headline)
                        }
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.blue.opacity(0.1))
                        .cornerRadius(12)
                    }

                    Button(action: {
                        // Choose from photo library
                        dismiss()
                    }) {
                        HStack(spacing: 15) {
                            Image(systemName: "photo.on.rectangle")
                                .font(.title2)
                                .foregroundColor(.green)

                            Text("Choose from Library")
                                .font(.headline)
                        }
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.green.opacity(0.1))
                        .cornerRadius(12)
                    }
                }
                .padding(.horizontal)

                Spacer()
            }
            .padding()
            .navigationTitle("Profile Picture")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
            }
        }
    }
}

struct EditProfileView: View {
    @Environment(\.dismiss) private var dismiss
    @EnvironmentObject var authManager: AuthenticationManager
    @State private var username = ""
    @State private var email = ""
    @State private var phone = ""
    @State private var bio = ""

    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Basic Information")) {
                    HStack {
                        Text("Username")
                        Spacer()
                        TextField("Username", text: $username)
                            .multilineTextAlignment(.trailing)
                    }

                    HStack {
                        Text("Email")
                        Spacer()
                        TextField("Email", text: $email)
                            .multilineTextAlignment(.trailing)
                            .keyboardType(.emailAddress)
                    }

                    HStack {
                        Text("Phone")
                        Spacer()
                        TextField("Phone number", text: $phone)
                            .multilineTextAlignment(.trailing)
                            .keyboardType(.phonePad)
                    }
                }

                Section(header: Text("About")) {
                    VStack(alignment: .leading) {
                        Text("Bio")
                            .font(.caption)
                            .foregroundColor(.secondary)

                        TextEditor(text: $bio)
                            .frame(height: 80)
                    }
                }
            }
            .navigationTitle("Edit Profile")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Save") {
                        // Save profile changes
                        dismiss()
                    }
                }
            }
        }
        .onAppear {
            if let user = authManager.currentUser {
                username = user.username
                email = user.email
            }
        }
    }
}

#Preview {
    ProfileView()
        .environmentObject(AuthenticationManager())
        .environmentObject(APIClient())
}