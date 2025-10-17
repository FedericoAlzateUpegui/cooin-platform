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
    @ObservedObject var languageManager = LanguageManager.shared
    @State private var showingImagePicker = false
    @State private var showingEditProfile = false
    @State private var showingSettings = false
    @State private var showingDocumentVerification = false
    @State private var showingAppInfo = false
    @State private var showingLanguagePicker = false

    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // Hidden view to trigger refresh on language change
                    Text("").hidden().id(languageManager.refreshTrigger)

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
                            ProfileSection(title: "profile.account".localized) {
                                ProfileMenuItem(
                                    title: "profile.edit".localized,
                                    subtitle: "profile.update_information".localized,
                                    icon: "person.crop.circle",
                                    color: .blue
                                ) {
                                    showingEditProfile = true
                                }

                                ProfileMenuItem(
                                    title: "profile.verification_status".localized,
                                    subtitle: "profile.complete_verification".localized,
                                    icon: "checkmark.shield",
                                    color: .green
                                ) {
                                    showingDocumentVerification = true
                                }

                                ProfileMenuItem(
                                    title: "profile.security".localized,
                                    subtitle: "profile.security_settings".localized,
                                    icon: "lock.shield",
                                    color: .orange
                                ) {
                                    // Navigate to security settings
                                }
                            }

                            // Activity section
                            ProfileSection(title: user.role == "borrower" ? "profile.my_borrowing".localized : "profile.my_lending".localized) {
                                if user.role == "borrower" {
                                    ProfileMenuItem(
                                        title: "profile.loan_requests".localized,
                                        subtitle: "profile.view_loan_applications".localized,
                                        icon: "doc.text",
                                        color: .blue
                                    ) {
                                        // Navigate to loan requests
                                    }

                                    ProfileMenuItem(
                                        title: "profile.active_loans".localized,
                                        subtitle: "profile.manage_current_loans".localized,
                                        icon: "dollarsign.circle",
                                        color: .green
                                    ) {
                                        // Navigate to active loans
                                    }
                                } else {
                                    ProfileMenuItem(
                                        title: "profile.lending_offers".localized,
                                        subtitle: "profile.manage_offers".localized,
                                        icon: "plus.circle",
                                        color: .blue
                                    ) {
                                        // Navigate to lending offers
                                    }

                                    ProfileMenuItem(
                                        title: "profile.active_investments".localized,
                                        subtitle: "profile.track_investments".localized,
                                        icon: "chart.line.uptrend.xyaxis",
                                        color: .green
                                    ) {
                                        // Navigate to investments
                                    }
                                }

                                ProfileMenuItem(
                                    title: "profile.transaction_history".localized,
                                    subtitle: "profile.view_transactions".localized,
                                    icon: "list.bullet.rectangle",
                                    color: .purple
                                ) {
                                    // Navigate to transaction history
                                }
                            }

                            // Settings section
                            ProfileSection(title: "settings.title".localized) {
                                ProfileMenuItem(
                                    title: "profile.language".localized,
                                    subtitle: languageManager.currentLanguage.displayName,
                                    icon: "globe",
                                    color: .blue
                                ) {
                                    showingLanguagePicker = true
                                }

                                ProfileMenuItem(
                                    title: "profile.notifications".localized,
                                    subtitle: "settings.notifications".localized,
                                    icon: "bell",
                                    color: .orange
                                ) {
                                    // Navigate to notifications
                                }

                                ProfileMenuItem(
                                    title: "profile.privacy".localized,
                                    subtitle: "profile.privacy".localized,
                                    icon: "hand.raised",
                                    color: .purple
                                ) {
                                    // Navigate to privacy settings
                                }

                                ProfileMenuItem(
                                    title: "profile.help_support".localized,
                                    subtitle: "profile.help_support_subtitle".localized,
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

                                        Text("auth.logout".localized)
                                            .font(.headline)
                                            .foregroundColor(.red)

                                        Spacer()
                                    }
                                    .padding()
                                    .background(Color.red.opacity(0.1))
                                    .cornerRadius(12)
                                }

                                Text("profile.version".localized + " 1.0.0")
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
            .navigationTitle("profile.title".localized)
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
        .sheet(isPresented: $showingLanguagePicker) {
            LanguagePickerView()
        }
        .sheet(isPresented: $showingAppInfo) {
            AppInfoView()
        }
    }
}

struct RoleBadge: View {
    let role: String
    @ObservedObject var languageManager = LanguageManager.shared

    var roleColor: Color {
        role == "borrower" ? .blue : .green
    }

    var roleText: String {
        role == "borrower" ? "profile.role_borrower".localized : "profile.role_lender".localized
    }

    var body: some View {
        // Hidden view to trigger refresh on language change
        Text("").hidden().id(languageManager.refreshTrigger)

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
    @ObservedObject var languageManager = LanguageManager.shared
    @State private var showingCameraUnavailable = false
    @State private var showingLibraryUnavailable = false

    var body: some View {
        NavigationView {
            VStack(spacing: 30) {
                // Hidden view to trigger refresh on language change
                Text("").hidden().id(languageManager.refreshTrigger)

                Text("profile.update_profile_picture".localized)
                    .font(.title2)
                    .fontWeight(.bold)

                VStack(spacing: 20) {
                    Button(action: {
                        #if targetEnvironment(simulator)
                        showingCameraUnavailable = true
                        #else
                        showingCameraUnavailable = true
                        #endif
                    }) {
                        HStack(spacing: 15) {
                            Image(systemName: "camera")
                                .font(.title2)
                                .foregroundColor(.blue)

                            Text("profile.take_photo".localized)
                                .font(.headline)
                        }
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.blue.opacity(0.1))
                        .cornerRadius(12)
                    }

                    Button(action: {
                        showingLibraryUnavailable = true
                    }) {
                        HStack(spacing: 15) {
                            Image(systemName: "photo.on.rectangle")
                                .font(.title2)
                                .foregroundColor(.green)

                            Text("profile.choose_from_library".localized)
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
            .navigationTitle("profile.profile_picture".localized)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("common.cancel".localized) {
                        dismiss()
                    }
                }
            }
            .alert("profile.camera_unavailable".localized, isPresented: $showingCameraUnavailable) {
                Button("common.ok".localized) { }
            } message: {
                #if targetEnvironment(simulator)
                Text("profile.camera_unavailable_simulator".localized)
                #else
                Text("profile.camera_coming_soon".localized)
                #endif
            }
            .alert("profile.photo_library".localized, isPresented: $showingLibraryUnavailable) {
                Button("common.ok".localized) { }
            } message: {
                Text("profile.photo_library_coming_soon".localized)
            }
        }
    }
}

struct EditProfileView: View {
    @Environment(\.dismiss) private var dismiss
    @EnvironmentObject var authManager: AuthenticationManager
    @ObservedObject var languageManager = LanguageManager.shared
    @State private var username = ""
    @State private var email = ""
    @State private var phone = ""
    @State private var bio = ""

    var body: some View {
        NavigationView {
            Form {
                // Hidden view to trigger refresh on language change
                Text("").hidden().id(languageManager.refreshTrigger)

                Section(header: Text("profile.basic_information".localized)) {
                    HStack {
                        Text("common.username".localized)
                        Spacer()
                        TextField("common.username".localized, text: $username)
                            .multilineTextAlignment(.trailing)
                    }

                    HStack {
                        Text("common.email".localized)
                        Spacer()
                        TextField("common.email".localized, text: $email)
                            .multilineTextAlignment(.trailing)
                            .keyboardType(.emailAddress)
                    }

                    HStack {
                        Text("profile.phone".localized)
                        Spacer()
                        TextField("profile.phone_number".localized, text: $phone)
                            .multilineTextAlignment(.trailing)
                            .keyboardType(.phonePad)
                    }
                }

                Section(header: Text("profile.about".localized)) {
                    VStack(alignment: .leading) {
                        Text("profile.bio".localized)
                            .font(.caption)
                            .foregroundColor(.secondary)

                        TextEditor(text: $bio)
                            .frame(height: 80)
                    }
                }
            }
            .navigationTitle("profile.edit".localized)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("common.cancel".localized) {
                        dismiss()
                    }
                }
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("common.save".localized) {
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

struct LanguagePickerView: View {
    @Environment(\.dismiss) private var dismiss
    @ObservedObject var languageManager = LanguageManager.shared

    var body: some View {
        NavigationView {
            List {
                // Hidden view to trigger refresh on language change
                Text("").hidden().id(languageManager.refreshTrigger)

                ForEach(LanguageManager.Language.allCases, id: \.self) { language in
                    Button(action: {
                        languageManager.setLanguage(language)
                        dismiss()
                    }) {
                        HStack {
                            Text(language.displayName)
                                .font(.headline)
                                .foregroundColor(.primary)

                            Spacer()

                            if languageManager.currentLanguage == language {
                                Image(systemName: "checkmark")
                                    .foregroundColor(.blue)
                                    .font(.headline)
                            }
                        }
                    }
                }
            }
            .navigationTitle("profile.select_language".localized)
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
    ProfileView()
        .environmentObject(AuthenticationManager())
        .environmentObject(APIClient())
}