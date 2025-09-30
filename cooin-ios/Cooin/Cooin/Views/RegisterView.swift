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

                        Text("Create Account")
                            .font(.largeTitle)
                            .fontWeight(.bold)

                        Text("Join the Cooin community")
                            .font(.body)
                            .foregroundColor(.secondary)
                    }
                    .padding(.top, 20)

                    // Form
                    VStack(spacing: 20) {
                        // Email field
                        VStack(alignment: .leading, spacing: 8) {
                            Text("Email")
                                .font(.headline)
                                .foregroundColor(.primary)

                            TextField("Enter your email", text: $email)
                                .textFieldStyle(RoundedBorderTextFieldStyle())
                                .keyboardType(.emailAddress)
                                .autocapitalization(.none)
                                .disableAutocorrection(true)
                        }

                        // Username field
                        VStack(alignment: .leading, spacing: 8) {
                            Text("Username")
                                .font(.headline)
                                .foregroundColor(.primary)

                            TextField("Choose a username", text: $username)
                                .textFieldStyle(RoundedBorderTextFieldStyle())
                                .autocapitalization(.none)
                                .disableAutocorrection(true)
                        }

                        // Role selection
                        VStack(alignment: .leading, spacing: 8) {
                            Text("I want to")
                                .font(.headline)
                                .foregroundColor(.primary)

                            Picker("Role", selection: $selectedRole) {
                                Text("Borrow money").tag("borrower")
                                Text("Lend money").tag("lender")
                            }
                            .pickerStyle(SegmentedPickerStyle())
                        }

                        // Password field
                        VStack(alignment: .leading, spacing: 8) {
                            Text("Password")
                                .font(.headline)
                                .foregroundColor(.primary)

                            HStack {
                                if showingPassword {
                                    TextField("Create a password", text: $password)
                                } else {
                                    SecureField("Create a password", text: $password)
                                }

                                Button(action: {
                                    showingPassword.toggle()
                                }) {
                                    Image(systemName: showingPassword ? "eye.slash" : "eye")
                                        .foregroundColor(.gray)
                                }
                            }
                            .textFieldStyle(RoundedBorderTextFieldStyle())

                            Text("Must be at least 8 characters with uppercase, lowercase, number, and special character")
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }

                        // Confirm password field
                        VStack(alignment: .leading, spacing: 8) {
                            Text("Confirm Password")
                                .font(.headline)
                                .foregroundColor(.primary)

                            HStack {
                                if showingConfirmPassword {
                                    TextField("Confirm your password", text: $confirmPassword)
                                } else {
                                    SecureField("Confirm your password", text: $confirmPassword)
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
                                Text("Passwords do not match")
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

                            Text("I agree to the Terms of Service and Privacy Policy")
                                .font(.caption)
                                .foregroundColor(.secondary)
                                .multilineTextAlignment(.leading)

                            Spacer()
                        }

                        // Error message
                        if let errorMessage = authManager.errorMessage {
                            Text(errorMessage)
                                .foregroundColor(.red)
                                .font(.caption)
                                .multilineTextAlignment(.center)
                        }

                        // Register button
                        Button(action: {
                            authManager.register(
                                email: email,
                                username: username,
                                password: password,
                                confirmPassword: confirmPassword,
                                role: selectedRole
                            )
                        }) {
                            HStack {
                                if authManager.isLoading {
                                    ProgressView()
                                        .progressViewStyle(CircularProgressViewStyle(tint: .white))
                                        .scaleEffect(0.8)
                                } else {
                                    Text("Create Account")
                                        .font(.headline)
                                        .fontWeight(.semibold)
                                }
                            }
                            .foregroundColor(.white)
                            .frame(maxWidth: .infinity)
                            .frame(height: 50)
                            .background(
                                isFormValid ? Color.blue : Color.gray
                            )
                            .cornerRadius(12)
                        }
                        .disabled(!isFormValid || authManager.isLoading)
                    }
                    .padding(.horizontal, 20)

                    Spacer()
                }
            }
            .navigationTitle("Register")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
            }
        }
        .onChange(of: authManager.isAuthenticated) { isAuthenticated in
            if isAuthenticated {
                dismiss()
            }
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

#Preview {
    RegisterView()
        .environmentObject(AuthenticationManager())
}