//
//  LanguageManager.swift
//  CooinNew
//
//  Manages app language/localization
//

import Foundation
import SwiftUI
import Combine

class LanguageManager: ObservableObject {
    static let shared = LanguageManager()

    @Published var currentLanguage: Language {
        didSet {
            UserDefaults.standard.set(currentLanguage.rawValue, forKey: "app_language")
            Bundle.setLanguage(currentLanguage.code)
            refreshTrigger += 1
        }
    }

    @Published var refreshTrigger: Int = 0

    enum Language: String, CaseIterable {
        case english = "en"
        case spanish = "es"

        var code: String {
            return self.rawValue
        }

        var displayName: String {
            switch self {
            case .english:
                return "English"
            case .spanish:
                return "Español"
            }
        }

        var localizedName: String {
            switch self {
            case .english:
                return NSLocalizedString("settings.english", comment: "")
            case .spanish:
                return NSLocalizedString("settings.spanish", comment: "")
            }
        }
    }

    private init() {
        // Load saved language or use device language
        if let savedLanguage = UserDefaults.standard.string(forKey: "app_language"),
           let language = Language(rawValue: savedLanguage) {
            self.currentLanguage = language
        } else {
            // Default to device language if available, otherwise English
            let deviceLanguage = Locale.current.languageCode ?? "en"
            self.currentLanguage = Language(rawValue: deviceLanguage) ?? .english
        }

        Bundle.setLanguage(currentLanguage.code)
    }

    func setLanguage(_ language: Language) {
        currentLanguage = language
        // Notify the app to reload
        NotificationCenter.default.post(name: .languageChanged, object: nil)
    }
}

// MARK: - Bundle Extension for Language Switching

private var bundleKey: UInt8 = 0

class BundleEx: Bundle, @unchecked Sendable {
    override func localizedString(forKey key: String, value: String?, table tableName: String?) -> String {
        if let bundle = objc_getAssociatedObject(self, &bundleKey) as? Bundle {
            return bundle.localizedString(forKey: key, value: value, table: tableName)
        }
        return super.localizedString(forKey: key, value: value, table: tableName)
    }
}

extension Bundle {
    static func setLanguage(_ language: String) {
        defer {
            object_setClass(Bundle.main, BundleEx.self)
        }

        guard let path = Bundle.main.path(forResource: language, ofType: "lproj"),
              let bundle = Bundle(path: path) else {
            return
        }

        objc_setAssociatedObject(Bundle.main, &bundleKey, bundle, .OBJC_ASSOCIATION_RETAIN_NONATOMIC)
    }
}

// MARK: - Notification Names

extension Notification.Name {
    static let languageChanged = Notification.Name("languageChanged")
}

// MARK: - String Extension for Easy Localization

extension String {
    var localized: String {
        return NSLocalizedString(self, comment: "")
    }

    func localized(with arguments: CVarArg...) -> String {
        return String(format: self.localized, arguments: arguments)
    }
}
