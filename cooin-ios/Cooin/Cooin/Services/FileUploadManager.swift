//
//  FileUploadManager.swift
//  Cooin
//
//  File upload and document management service
//

import SwiftUI
import Combine

class FileUploadManager: ObservableObject {
    @Published var uploadProgress: Double = 0.0
    @Published var isUploading = false
    @Published var uploadedDocuments: [UploadedDocument] = []
    @Published var errorMessage: String?

    private let apiClient: APIClient
    private var cancellables = Set<AnyCancellable>()
    private var progressTimer: Timer?

    init(apiClient: APIClient) {
        self.apiClient = apiClient
    }

    func uploadImage(_ image: UIImage, documentType: DocumentType, authToken: String) {
        guard let imageData = image.jpegData(compressionQuality: 0.8) else {
            errorMessage = NSLocalizedString("upload.error.failed_to_process", comment: "")
            return
        }

        uploadFile(data: imageData, fileName: "\(documentType.rawValue)_\(Date().timeIntervalSince1970).jpg",
                  mimeType: "image/jpeg", documentType: documentType, authToken: authToken, image: image)
    }

    func uploadDocument(data: Data, fileName: String, mimeType: String, documentType: DocumentType, authToken: String) {
        uploadFile(data: data, fileName: fileName, mimeType: mimeType, documentType: documentType, authToken: authToken, image: nil)
    }

    private func uploadFile(data: Data, fileName: String, mimeType: String, documentType: DocumentType, authToken: String, image: UIImage? = nil) {
        isUploading = true
        uploadProgress = 0.0
        errorMessage = nil

        // Create multipart form data
        let boundary = UUID().uuidString
        var body = Data()

        // Add document type field
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"document_type\"\r\n\r\n".data(using: .utf8)!)
        body.append("\(documentType.rawValue)\r\n".data(using: .utf8)!)

        // Add file data
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"file\"; filename=\"\(fileName)\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: \(mimeType)\r\n\r\n".data(using: .utf8)!)
        body.append(data)
        body.append("\r\n".data(using: .utf8)!)
        body.append("--\(boundary)--\r\n".data(using: .utf8)!)

        // Create request
        #if targetEnvironment(simulator)
        let baseURL = "http://127.0.0.1:8000"
        #else
        let baseURL = "http://192.168.1.9:8000"
        #endif

        guard let url = URL(string: "\(baseURL)/api/v1/mobile/uploads/document") else {
            errorMessage = NSLocalizedString("upload.error.invalid_url", comment: "")
            isUploading = false
            return
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(authToken)", forHTTPHeaderField: "Authorization")
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        request.httpBody = body

        // Upload with proper response handling
        URLSession.shared.dataTaskPublisher(for: request)
            .tryMap { data, response -> Data in
                // Check HTTP status code
                guard let httpResponse = response as? HTTPURLResponse else {
                    throw URLError(.badServerResponse)
                }

                // Log response for debugging
                print("📤 Upload response status: \(httpResponse.statusCode)")
                if let responseString = String(data: data, encoding: .utf8) {
                    print("📤 Upload response: \(responseString)")
                }

                // Check for success
                guard (200...299).contains(httpResponse.statusCode) else {
                    throw URLError(.badServerResponse)
                }

                return data
            }
            .receive(on: DispatchQueue.main)
            .sink(
                receiveCompletion: { [weak self] completion in
                    self?.progressTimer?.invalidate()
                    self?.progressTimer = nil
                    self?.isUploading = false
                    if case .failure(let error) = completion {
                        print("❌ Upload failed: \(error)")
                        if (error as? URLError)?.code == .timedOut {
                            self?.errorMessage = NSLocalizedString("upload.error.timeout", comment: "")
                        } else {
                            self?.errorMessage = error.localizedDescription
                        }
                    }
                },
                receiveValue: { [weak self] data in
                    print("✅ Upload successful")
                    // Create document from successful upload
                    let document = UploadedDocument(
                        id: UUID().uuidString,
                        fileName: fileName,
                        documentType: documentType,
                        uploadDate: Date(),
                        status: .pending,
                        image: image
                    )
                    self?.uploadedDocuments.append(document)
                    self?.uploadProgress = 1.0
                }
            )
            .store(in: &cancellables)

        // Simulate progress with proper cleanup
        progressTimer?.invalidate()
        progressTimer = Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { [weak self] timer in
            guard let self = self else {
                timer.invalidate()
                return
            }
            DispatchQueue.main.async {
                if self.uploadProgress < 0.9 && self.isUploading {
                    self.uploadProgress += 0.1
                } else {
                    timer.invalidate()
                    self.progressTimer = nil
                }
            }
        }
    }

    func deleteDocument(_ document: UploadedDocument, authToken: String) {
        uploadedDocuments.removeAll { $0.id == document.id }
    }
}

// MARK: - Data Models

struct UploadedDocument: Identifiable {
    let id: String
    let fileName: String
    let documentType: DocumentType
    let uploadDate: Date
    let status: DocumentStatus
    let image: UIImage?
}

enum DocumentType: String, CaseIterable {
    case idCard = "id_card"
    case driversLicense = "drivers_license"
    case passport = "passport"
    case incomeProof = "income_proof"
    case bankStatement = "bank_statement"
    case profilePhoto = "profile_photo"
    case creditReport = "credit_report"
    case employmentLetter = "employment_letter"

    var displayName: String {
        switch self {
        case .idCard: return "ID Card"
        case .driversLicense: return "Driver's License"
        case .passport: return "Passport"
        case .incomeProof: return "Income Proof"
        case .bankStatement: return "Bank Statement"
        case .profilePhoto: return "Profile Photo"
        case .creditReport: return "Credit Report"
        case .employmentLetter: return "Employment Letter"
        }
    }

    var icon: String {
        switch self {
        case .idCard, .driversLicense, .passport: return "person.text.rectangle"
        case .incomeProof, .employmentLetter: return "doc.text"
        case .bankStatement: return "building.columns"
        case .profilePhoto: return "person.crop.circle"
        case .creditReport: return "chart.line.uptrend.xyaxis"
        }
    }
}

enum DocumentStatus {
    case pending
    case verified
    case rejected

    var color: Color {
        switch self {
        case .pending: return .orange
        case .verified: return .green
        case .rejected: return .red
        }
    }

    var displayName: String {
        switch self {
        case .pending: return "Pending"
        case .verified: return "Verified"
        case .rejected: return "Rejected"
        }
    }
}