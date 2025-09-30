//
//  CooinApp.swift
//  Cooin
//
//  Created by Claude on 2024-01-15.
//  Cooin - Peer-to-Peer Lending Platform
//

import SwiftUI

@main
struct CooinApp: App {
    @StateObject private var authManager = AuthenticationManager()
    @StateObject private var apiClient = APIClient()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(authManager)
                .environmentObject(apiClient)
                .preferredColorScheme(.light)
        }
    }
}