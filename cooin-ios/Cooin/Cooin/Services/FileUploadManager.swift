//
//  FileUploadManager.swift
//  Cooin
//
//  File upload and document management service
//

import SwiftUI
import PhotosUI
import Combine

class FileUploadManager: ObservableObject {
    @Published var uploadProgress: Double = 0.0
    @Published var isUploading = false
    @Published var uploadedDocuments: [UploadedDocument] = []
    @Published var errorMessage: String?

    private let apiClient: APIClient
    private var cancellables = Set<AnyCancellable>()

    init(apiClient: APIClient) {
        self.apiClient = apiClient
    }

    func uploadImage(_ image: UIImage, documentType: DocumentType, authToken: String) {
        guard let imageData = image.jpegData(compressionQuality: 0.8) else {
            errorMessage = "Failed to process image"
            return
        }

        uploadFile(data: imageData, fileName: "\(documentType.rawValue)_\(Date().timeIntervalSince1970).jpg",
                  mimeType: "image/jpeg", documentType: documentType, authToken: authToken)
    }

    func uploadDocument(data: Data, fileName: String, mimeType: String, documentType: DocumentType, authToken: String) {
        uploadFile(data: data, fileName: fileName, mimeType: mimeType, documentType: documentType, authToken: authToken)
    }

    private func uploadFile(data: Data, fileName: String, mimeType: String, documentType: DocumentType, authToken: String) {
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
        guard let url = URL(string: "http://192.168.40.34:8000/api/v1/documents/upload") else {
            errorMessage = "Invalid URL"
            isUploading = false
            return
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(authToken)", forHTTPHeaderField: "Authorization")
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        request.httpBody = body

        // Simulate upload progress
        URLSession.shared.dataTaskPublisher(for: request)
            .map { data, response in
                // Parse response
                return data
            }
            .receive(on: DispatchQueue.main)
            .sink(
                receiveCompletion: { [weak self] completion in
                    self?.isUploading = false
                    if case .failure(let error) = completion {
                        self?.errorMessage = error.localizedDescription
                    }
                },
                receiveValue: { [weak self] data in
                    // Simulate successful upload
                    let document = UploadedDocument(
                        id: UUID().uuidString,
                        fileName: fileName,
                        documentType: documentType,
                        uploadDate: Date(),
                        status: .verified
                    )
                    self?.uploadedDocuments.append(document)
                    self?.uploadProgress = 1.0
                }
            )
            .store(in: &cancellables)

        // Simulate progress
        Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { timer in
            DispatchQueue.main.async {
                if self.uploadProgress < 0.9 && self.isUploading {
                    self.uploadProgress += 0.1
                } else {
                    timer.invalidate()
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

// MARK: - Photo Picker Integration

struct PhotoPickerView: UIViewControllerRepresentable {
    @Binding var selectedImage: UIImage?
    @Environment(\.dismiss) private var dismiss

    func makeUIViewController(context: Context) -> PHPickerViewController {
        var config = PHPickerConfiguration()
        config.filter = .images
        config.selectionLimit = 1

        let picker = PHPickerViewController(configuration: config)
        picker.delegate = context.coordinator
        return picker
    }

    func updateUIViewController(_ uiViewController: PHPickerViewController, context: Context) {}

    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    class Coordinator: NSObject, PHPickerViewControllerDelegate {
        let parent: PhotoPickerView

        init(_ parent: PhotoPickerView) {
            self.parent = parent
        }

        func picker(_ picker: PHPickerViewController, didFinishPicking results: [PHPickerResult]) {
            picker.dismiss(animated: true)

            guard let provider = results.first?.itemProvider,
                  provider.canLoadObject(ofClass: UIImage.self) else {
                return
            }

            provider.loadObject(ofClass: UIImage.self) { image, error in
                DispatchQueue.main.async {
                    self.parent.selectedImage = image as? UIImage
                }
            }
        }
    }
}

// MARK: - Camera Integration

struct CameraView: UIViewControllerRepresentable {
    @Binding var selectedImage: UIImage?
    @Environment(\.dismiss) private var dismiss

    func makeUIViewController(context: Context) -> UIImagePickerController {
        let picker = UIImagePickerController()
        picker.sourceType = .camera
        picker.delegate = context.coordinator
        return picker
    }

    func updateUIViewController(_ uiViewController: UIImagePickerController, context: Context) {}

    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    class Coordinator: NSObject, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
        let parent: CameraView

        init(_ parent: CameraView) {
            self.parent = parent
        }

        func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
            if let image = info[.originalImage] as? UIImage {
                parent.selectedImage = image
            }
            picker.dismiss(animated: true)
        }

        func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
            picker.dismiss(animated: true)
        }
    }
}