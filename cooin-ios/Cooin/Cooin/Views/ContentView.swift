//
//  ContentView.swift
//  Cooin
//
//  Main content view that handles navigation
//

import SwiftUI

struct ContentView: View {
    @EnvironmentObject var authManager: AuthenticationManager
    @State private var showingSplash = true

    var body: some View {
        Group {
            if showingSplash {
                SplashView()
            } else if authManager.isAuthenticated {
                MainTabView()
            } else {
                WelcomeView()
            }
        }
        .onAppear {
            // Show splash for 2 seconds
            DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
                withAnimation(.easeInOut(duration: 0.5)) {
                    showingSplash = false
                }
            }
        }
    }
}

struct SplashView: View {
    var body: some View {
        ZStack {
            // Gradient background
            LinearGradient(
                gradient: Gradient(colors: [
                    Color(red: 0.2, green: 0.6, blue: 1.0),
                    Color(red: 0.1, green: 0.4, blue: 0.8)
                ]),
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()

            VStack(spacing: 20) {
                // Logo
                Image(systemName: "dollarsign.circle.fill")
                    .font(.system(size: 80))
                    .foregroundColor(.white)

                Text("Cooin")
                    .font(.largeTitle)
                    .fontWeight(.bold)
                    .foregroundColor(.white)

                Text("welcome.peer_to_peer_lending".localized)
                    .font(.title3)
                    .foregroundColor(.white.opacity(0.8))

                // Loading indicator
                ProgressView()
                    .progressViewStyle(CircularProgressViewStyle(tint: .white))
                    .scaleEffect(1.2)
                    .padding(.top, 20)
            }
        }
    }
}

struct WelcomeView: View {
    @State private var showingLogin = false
    @State private var showingRegister = false

    var body: some View {
        NavigationView {
            ZStack {
                // Background
                LinearGradient(
                    gradient: Gradient(colors: [
                        Color(red: 0.95, green: 0.97, blue: 1.0),
                        Color(red: 0.9, green: 0.95, blue: 1.0)
                    ]),
                    startPoint: .top,
                    endPoint: .bottom
                )
                .ignoresSafeArea()

                VStack(spacing: 30) {
                    Spacer()

                    // Logo and Title
                    VStack(spacing: 15) {
                        Image(systemName: "dollarsign.circle.fill")
                            .font(.system(size: 60))
                            .foregroundColor(.blue)

                        Text("welcome.title".localized)
                            .font(.largeTitle)
                            .fontWeight(.bold)
                            .foregroundColor(.primary)

                        Text("welcome.subtitle".localized)
                            .font(.body)
                            .multilineTextAlignment(.center)
                            .foregroundColor(.secondary)
                    }

                    Spacer()

                    // Action Buttons
                    VStack(spacing: 15) {
                        Button(action: {
                            showingLogin = true
                        }) {
                            Text("welcome.login_button".localized)
                                .font(.headline)
                                .foregroundColor(.white)
                                .frame(maxWidth: .infinity)
                                .frame(height: 50)
                                .background(Color.blue)
                                .cornerRadius(12)
                        }

                        Button(action: {
                            showingRegister = true
                        }) {
                            Text("welcome.register_button".localized)
                                .font(.headline)
                                .foregroundColor(.blue)
                                .frame(maxWidth: .infinity)
                                .frame(height: 50)
                                .background(Color.white)
                                .overlay(
                                    RoundedRectangle(cornerRadius: 12)
                                        .stroke(Color.blue, lineWidth: 2)
                                )
                                .cornerRadius(12)
                        }
                    }
                    .padding(.horizontal, 30)

                    Spacer()
                }
            }
        }
        .sheet(isPresented: $showingLogin) {
            LoginView()
        }
        .sheet(isPresented: $showingRegister) {
            RegisterView()
        }
    }
}

#Preview {
    ContentView()
        .environmentObject(AuthenticationManager())
        .environmentObject(APIClient())
}