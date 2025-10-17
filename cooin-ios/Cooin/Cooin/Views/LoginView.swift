//
//  LoginView.swift
//  Cooin
//
//  User login screen
//

import SwiftUI

struct LoginView: View {
    @Environment(\.dismiss) private var dismiss
    @EnvironmentObject var authManager: AuthenticationManager

    @State private var email = ""
    @State private var password = ""
    @State private var showingPassword = false
    @State private var showSuccessAlert = false

    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 25) {
                    // Header
                    VStack(spacing: 10) {
                        Image(systemName: "person.circle.fill")
                            .font(.system(size: 50))
                            .foregroundColor(.blue)

                        Text("login.welcome_back".localized)
                            .font(.largeTitle)
                            .fontWeight(.bold)

                        Text("auth.sign_in".localized)
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

                            TextField("login.email_placeholder".localized, text: $email)
                                .textFieldStyle(RoundedBorderTextFieldStyle())
                                .keyboardType(.emailAddress)
                                .autocapitalization(.none)
                                .disableAutocorrection(true)
                        }

                        // Password field
                        VStack(alignment: .leading, spacing: 8) {
                            Text("common.password".localized)
                                .font(.headline)
                                .foregroundColor(.primary)

                            HStack {
                                if showingPassword {
                                    TextField("login.password_placeholder".localized, text: $password)
                                } else {
                                    SecureField("login.password_placeholder".localized, text: $password)
                                }

                                Button(action: {
                                    showingPassword.toggle()
                                }) {
                                    Image(systemName: showingPassword ? "eye.slash" : "eye")
                                        .foregroundColor(.gray)
                                }
                            }
                            .textFieldStyle(RoundedBorderTextFieldStyle())
                        }

                        // Error message
                        if let errorMessage = authManager.errorMessage {
                            Text(errorMessage)
                                .foregroundColor(.red)
                                .font(.caption)
                                .multilineTextAlignment(.center)
                        }

                        // Login button
                        Button(action: {
                            authManager.login(email: email, password: password)
                        }) {
                            HStack {
                                if authManager.isLoading {
                                    ProgressView()
                                        .progressViewStyle(CircularProgressViewStyle(tint: .white))
                                        .scaleEffect(0.8)
                                } else {
                                    Text("auth.login".localized)
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
            .navigationTitle("login.title".localized)
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
                // Dismiss after a short delay to allow user to see success message
                DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) {
                    dismiss()
                }
            }
        }
        .alert("login.success_title".localized, isPresented: $showSuccessAlert) {
            Button("common.ok".localized) {
                dismiss()
            }
        } message: {
            Text("login.success_message".localized)
        }
    }

    private var isFormValid: Bool {
        !email.isEmpty && !password.isEmpty && email.contains("@")
    }
}

#Preview {
    LoginView()
        .environmentObject(AuthenticationManager())
}