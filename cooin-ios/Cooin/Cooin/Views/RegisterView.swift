//
//  RegisterView.swift
//  Cooin
//
//  User registration screen
//

import SwiftUI

struct RegisterView: View {
    @Environment(\.dismiss) private var dismiss
    @EnvironmentObject var authManager: AuthenticationManager

    @State private var email = ""
    @State private var username = ""
    @State private var password = ""
    @State private var confirmPassword = ""
    @State private var selectedRole = "borrower"
    @State private var agreeToTerms = false
    @State private var showingPassword = false
    @State private var showingConfirmPassword = false
    @State private var showSuccessAlert = false

    let roles = ["borrower", "lender"]

    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 25) {
                    // Header
                    VStack(spacing: 10) {
                        Image(systemName: "person.badge.plus")
                            .font(.system(size: 50))
                            .foregroundColor(.blue)

                        Text("register.title".localized)
                            .font(.largeTitle)
                            .fontWeight(.bold)

                        Text("auth.join_community".localized)
                            .font(.body)
                            .foregroundColor(.secondary)
                    }
                    .padding(.top, 20)

                    // Form
                    VStack(spacing: 20) {
                        // Email field
                        VStack(alignment: .leading, spacing: 8) {
                            Text("common.email".localized)
                                .font(.headline)
                                .foregroundColor(.primary)

                            TextField("register.email_placeholder".localized, text: $email)
                                .textFieldStyle(RoundedBorderTextFieldStyle())
                                .keyboardType(.emailAddress)
                                .autocapitalization(.none)
                                .disableAutocorrection(true)
                        }

                        // Username field
                        VStack(alignment: .leading, spacing: 8) {
                            Text("common.username".localized)
                                .font(.headline)
                                .foregroundColor(.primary)

                            TextField("register.username_placeholder".localized, text: $username)
                                .textFieldStyle(RoundedBorderTextFieldStyle())
                                .autocapitalization(.none)
                                .disableAutocorrection(true)
                        }

                        // Role selection
                        VStack(alignment: .leading, spacing: 8) {
                            Text("register.role_label".localized)
                                .font(.headline)
                                .foregroundColor(.primary)

                            Picker("Role", selection: $selectedRole) {
                                Text("register.role_borrower".localized).tag("borrower")
                                Text("register.role_lender".localized).tag("lender")
                            }
                            .pickerStyle(SegmentedPickerStyle())
                        }

                        // Password field
                        VStack(alignment: .leading, spacing: 8) {
                            Text("common.password".localized)
                                .font(.headline)
                                .foregroundColor(.primary)

                            HStack {
                                if showingPassword {
                                    TextField("register.password_placeholder".localized, text: $password)
                                        .textContentType(.none)
                                        .autocapitalization(.none)
                                        .disableAutocorrection(true)
                                } else {
                                    SecureField("register.password_placeholder".localized, text: $password)
                                        .textContentType(.none)
                                        .autocapitalization(.none)
                                        .disableAutocorrection(true)
                                }

                                Button(action: {
                                    showingPassword.toggle()
                                }) {
                                    Image(systemName: showingPassword ? "eye.slash" : "eye")
                                        .foregroundColor(.gray)
                                }
                            }
                            .textFieldStyle(RoundedBorderTextFieldStyle())

                            // Password requirements with validation indicators
                            if !password.isEmpty {
                                VStack(alignment: .leading, spacing: 4) {
                                    PasswordRequirementRow(text: "register.password_requirement_length".localized, isMet: password.count >= 8)
                                    PasswordRequirementRow(text: "register.password_requirement_uppercase".localized, isMet: password.contains(where: { $0.isUppercase }))
                                    PasswordRequirementRow(text: "register.password_requirement_lowercase".localized, isMet: password.contains(where: { $0.isLowercase }))
                                    PasswordRequirementRow(text: "register.password_requirement_number".localized, isMet: password.contains(where: { $0.isNumber }))
                                }
                                .padding(.vertical, 4)
                            } else {
                                Text("register.password_requirements_text".localized)
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }

                            // Password strength indicator
                            if !password.isEmpty {
                                PasswordStrengthIndicator(password: password)
                            }
                        }

                        // Confirm password field
                        VStack(alignment: .leading, spacing: 8) {
                            Text("register.confirm_password".localized)
                                .font(.headline)
                                .foregroundColor(.primary)

                            HStack {
                                if showingConfirmPassword {
                                    TextField("register.confirm_password_placeholder".localized, text: $confirmPassword)
                                        .textContentType(.none)
                                        .autocapitalization(.none)
                                        .disableAutocorrection(true)
                                } else {
                                    SecureField("register.confirm_password_placeholder".localized, text: $confirmPassword)
                                        .textContentType(.none)
                                        .autocapitalization(.none)
                                        .disableAutocorrection(true)
                                }

                                Button(action: {
                                    showingConfirmPassword.toggle()
                                }) {
                                    Image(systemName: showingConfirmPassword ? "eye.slash" : "eye")
                                        .foregroundColor(.gray)
                                }
                            }
                            .textFieldStyle(RoundedBorderTextFieldStyle())

                            if !confirmPassword.isEmpty && password != confirmPassword {
                                Text("register.passwords_not_match".localized)
                                    .font(.caption)
                                    .foregroundColor(.red)
                            }
                        }

                        // Terms agreement
                        HStack(alignment: .top, spacing: 10) {
                            Button(action: {
                                agreeToTerms.toggle()
                            }) {
                                Image(systemName: agreeToTerms ? "checkmark.square.fill" : "square")
                                    .foregroundColor(agreeToTerms ? .blue : .gray)
                                    .font(.title3)
                            }

                            Text("register.agree_terms".localized)
                                .font(.caption)
                                .foregroundColor(.secondary)
                                .multilineTextAlignment(.leading)

                            Spacer()
                        }

                        // Error message with recovery suggestion
                        if let errorMessage = authManager.errorMessage {
                            VStack(spacing: 4) {
                                Text(errorMessage)
                                    .foregroundColor(.red)
                                    .font(.callout)
                                    .fontWeight(.semibold)
                                    .multilineTextAlignment(.center)

                                // Show helpful recovery suggestion if available
                                if errorMessage.lowercased().contains("password") {
                                    Text("register.error_recovery_password".localized)
                                        .foregroundColor(.orange)
                                        .font(.caption)
                                        .multilineTextAlignment(.center)
                                } else if errorMessage.lowercased().contains("email") && errorMessage.lowercased().contains("exists") {
                                    Text("register.error_recovery_email".localized)
                                        .foregroundColor(.orange)
                                        .font(.caption)
                                        .multilineTextAlignment(.center)
                                } else if errorMessage.lowercased().contains("rate limit") || errorMessage.lowercased().contains("too many") {
                                    Text("register.error_recovery_rate_limit".localized)
                                        .foregroundColor(.orange)
                                        .font(.caption)
                                        .multilineTextAlignment(.center)
                                }
                            }
                            .padding(.vertical, 8)
                            .padding(.horizontal, 12)
                            .background(Color.red.opacity(0.1))
                            .cornerRadius(8)
                        }

                        // Register button with improved loading state
                        Button(action: {
                            // Clear any previous errors
                            authManager.errorMessage = nil
                            authManager.register(
                                email: email,
                                username: username,
                                password: password,
                                confirmPassword: confirmPassword,
                                role: selectedRole
                            )
                        }) {
                            HStack(spacing: 12) {
                                if authManager.isLoading {
                                    ProgressView()
                                        .progressViewStyle(CircularProgressViewStyle(tint: .white))
                                        .scaleEffect(0.9)
                                    Text("register.creating_account_loading".localized)
                                        .font(.headline)
                                        .fontWeight(.semibold)
                                } else {
                                    Image(systemName: "person.badge.plus")
                                        .font(.title3)
                                    Text("auth.create_account".localized)
                                        .font(.headline)
                                        .fontWeight(.semibold)
                                }
                            }
                            .foregroundColor(.white)
                            .frame(maxWidth: .infinity)
                            .frame(height: 52)
                            .background(
                                Group {
                                    if authManager.isLoading {
                                        Color.blue.opacity(0.7)
                                    } else if isFormValid {
                                        Color.blue
                                    } else {
                                        Color.gray
                                    }
                                }
                            )
                            .cornerRadius(12)
                            .shadow(color: isFormValid && !authManager.isLoading ? Color.blue.opacity(0.3) : Color.clear, radius: 8, x: 0, y: 4)
                        }
                        .disabled(!isFormValid || authManager.isLoading)
                        .animation(.easeInOut(duration: 0.2), value: authManager.isLoading)
                    }
                    .padding(.horizontal, 20)

                    Spacer()
                }
            }
            .navigationTitle("auth.register".localized)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("common.cancel".localized) {
                        dismiss()
                    }
                }
            }
        }
        .onChange(of: authManager.isAuthenticated) { isAuthenticated in
            if isAuthenticated {
                showSuccessAlert = true
                // Don't auto-dismiss - let user tap OK when ready
            }
        }
        .alert("register.success_title".localized, isPresented: $showSuccessAlert) {
            Button("common.ok".localized) {
                dismiss()
            }
        } message: {
            Text("register.success_message".localized)
        }
    }

    private var isFormValid: Bool {
        !email.isEmpty &&
        !username.isEmpty &&
        !password.isEmpty &&
        !confirmPassword.isEmpty &&
        email.contains("@") &&
        password == confirmPassword &&
        password.count >= 8 &&
        agreeToTerms
    }
}

// MARK: - Password Requirement Row Component
struct PasswordRequirementRow: View {
    let text: String
    let isMet: Bool

    var body: some View {
        HStack(spacing: 6) {
            Image(systemName: isMet ? "checkmark.circle.fill" : "circle")
                .foregroundColor(isMet ? .green : .gray)
                .font(.caption)
            Text(text)
                .font(.caption)
                .foregroundColor(isMet ? .green : .secondary)
        }
    }
}

// MARK: - Password Strength Indicator Component
struct PasswordStrengthIndicator: View {
    let password: String

    private var strength: PasswordStrength {
        let hasMinLength = password.count >= 8
        let hasUppercase = password.contains(where: { $0.isUppercase })
        let hasLowercase = password.contains(where: { $0.isLowercase })
        let hasNumber = password.contains(where: { $0.isNumber })
        let hasSpecialChar = password.contains(where: { "!@#$%^&*(),.?\":{}|<>".contains($0) })

        let metRequirements = [hasMinLength, hasUppercase, hasLowercase, hasNumber].filter { $0 }.count

        if metRequirements == 4 && hasSpecialChar {
            return .strong
        } else if metRequirements >= 3 {
            return .medium
        } else {
            return .weak
        }
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text("register.password_strength_label".localized + " \(strength.text)")
                .font(.caption)
                .fontWeight(.semibold)
                .foregroundColor(strength.color)

            GeometryReader { geometry in
                ZStack(alignment: .leading) {
                    Rectangle()
                        .fill(Color.gray.opacity(0.2))
                        .frame(height: 4)
                        .cornerRadius(2)

                    Rectangle()
                        .fill(strength.color)
                        .frame(width: geometry.size.width * strength.percentage, height: 4)
                        .cornerRadius(2)
                        .animation(.easeInOut(duration: 0.3), value: strength)
                }
            }
            .frame(height: 4)
        }
    }

    enum PasswordStrength {
        case weak, medium, strong

        var text: String {
            switch self {
            case .weak: return "register.password_strength_weak".localized
            case .medium: return "register.password_strength_good".localized
            case .strong: return "register.password_strength_strong".localized
            }
        }

        var color: Color {
            switch self {
            case .weak: return .red
            case .medium: return .orange
            case .strong: return .green
            }
        }

        var percentage: CGFloat {
            switch self {
            case .weak: return 0.33
            case .medium: return 0.66
            case .strong: return 1.0
            }
        }
    }
}

#Preview {
    RegisterView()
        .environmentObject(AuthenticationManager())
}