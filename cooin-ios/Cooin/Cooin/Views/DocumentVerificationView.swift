//
//  DocumentVerificationView.swift
//  Cooin
//
//  Document verification and upload interface
//

import SwiftUI

struct DocumentVerificationView: View {
    @Environment(\.dismiss) private var dismiss
    @EnvironmentObject var authManager: AuthenticationManager
    @EnvironmentObject var apiClient: APIClient
    @StateObject private var fileUploadManager: FileUploadManager

    @State private var selectedDocumentType: DocumentType = .idCard
    @State private var showingImagePicker = false
    @State private var showingCamera = false
    @State private var showingDocumentPicker = false
    @State private var selectedImage: UIImage?
    @State private var uploadSource: UploadSource = .camera

    enum UploadSource {
        case camera, photoLibrary, documents
    }

    init() {
        // Initialize with a temporary APIClient - will be replaced by environment object
        self._fileUploadManager = StateObject(wrappedValue: FileUploadManager(apiClient: APIClient()))
    }

    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 25) {
                    // Header
                    VStack(spacing: 10) {
                        Image(systemName: "checkmark.shield.fill")
                            .font(.system(size: 50))
                            .foregroundColor(.green)

                        Text("Document Verification")
                            .font(.title2)
                            .fontWeight(.bold)

                        Text("Upload documents to verify your identity and financial status")
                            .font(.body)
                            .foregroundColor(.secondary)
                            .multilineTextAlignment(.center)
                    }
                    .padding(.horizontal)

                    // Document Type Selection
                    VStack(spacing: 15) {
                        Text("Select Document Type")
                            .font(.headline)
                            .frame(maxWidth: .infinity, alignment: .leading)

                        ScrollView(.horizontal, showsIndicators: false) {
                            HStack(spacing: 12) {
                                ForEach(DocumentType.allCases, id: \.self) { docType in
                                    DocumentTypeCard(
                                        documentType: docType,
                                        isSelected: selectedDocumentType == docType
                                    ) {
                                        selectedDocumentType = docType
                                    }
                                }
                            }
                            .padding(.horizontal)
                        }
                    }

                    // Upload Options
                    VStack(spacing: 15) {
                        Text("Upload Method")
                            .font(.headline)
                            .frame(maxWidth: .infinity, alignment: .leading)

                        VStack(spacing: 12) {
                            UploadOptionCard(
                                title: "Take Photo",
                                subtitle: "Use camera to capture document",
                                icon: "camera.fill",
                                color: .blue
                            ) {
                                uploadSource = .camera
                                showingCamera = true
                            }

                            UploadOptionCard(
                                title: "Choose from Photos",
                                subtitle: "Select from photo library",
                                icon: "photo.fill",
                                color: .green
                            ) {
                                uploadSource = .photoLibrary
                                showingImagePicker = true
                            }

                            UploadOptionCard(
                                title: "Browse Files",
                                subtitle: "Upload PDF or other documents",
                                icon: "doc.fill",
                                color: .orange
                            ) {
                                uploadSource = .documents
                                showingDocumentPicker = true
                            }
                        }
                    }
                    .padding(.horizontal)

                    // Upload Progress
                    if fileUploadManager.isUploading {
                        VStack(spacing: 10) {
                            Text("Uploading...")
                                .font(.headline)

                            ProgressView(value: fileUploadManager.uploadProgress)
                                .progressViewStyle(LinearProgressViewStyle(tint: .blue))

                            Text("\(Int(fileUploadManager.uploadProgress * 100))%")
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                        .padding()
                        .background(Color.blue.opacity(0.1))
                        .cornerRadius(12)
                        .padding(.horizontal)
                    }

                    // Error Message
                    if let errorMessage = fileUploadManager.errorMessage {
                        Text(errorMessage)
                            .foregroundColor(.red)
                            .font(.caption)
                            .padding()
                            .background(Color.red.opacity(0.1))
                            .cornerRadius(8)
                            .padding(.horizontal)
                    }

                    // Uploaded Documents
                    if !fileUploadManager.uploadedDocuments.isEmpty {
                        VStack(spacing: 15) {
                            Text("Uploaded Documents")
                                .font(.headline)
                                .frame(maxWidth: .infinity, alignment: .leading)

                            LazyVStack(spacing: 10) {
                                ForEach(fileUploadManager.uploadedDocuments) { document in
                                    DocumentRow(document: document) {
                                        // Delete document
                                        if let token = authManager.getAccessToken() {
                                            fileUploadManager.deleteDocument(document, authToken: token)
                                        }
                                    }
                                }
                            }
                        }
                        .padding(.horizontal)
                    }

                    // Requirements Section
                    VStack(spacing: 15) {
                        Text("Document Requirements")
                            .font(.headline)
                            .frame(maxWidth: .infinity, alignment: .leading)

                        VStack(spacing: 8) {
                            RequirementRow(text: "Documents must be clear and legible", isCompleted: true)
                            RequirementRow(text: "All four corners must be visible", isCompleted: true)
                            RequirementRow(text: "No glare or shadows", isCompleted: false)
                            RequirementRow(text: "File size under 10MB", isCompleted: true)
                        }
                    }
                    .padding(.horizontal)

                    Spacer(minLength: 100)
                }
                .padding(.top)
            }
            .navigationTitle("Verification")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
                        dismiss()
                    }
                }
            }
        }
        .sheet(isPresented: $showingImagePicker) {
            PhotoPickerView(selectedImage: $selectedImage)
        }
        .sheet(isPresented: $showingCamera) {
            CameraView(selectedImage: $selectedImage)
        }
        .onChange(of: selectedImage) { image in
            if let image = image, let token = authManager.getAccessToken() {
                fileUploadManager.uploadImage(image, documentType: selectedDocumentType, authToken: token)
                selectedImage = nil
            }
        }
        .onAppear {
            // Update the file upload manager with the correct API client
            fileUploadManager.objectWillChange.send()
        }
    }
}

struct DocumentTypeCard: View {
    let documentType: DocumentType
    let isSelected: Bool
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            VStack(spacing: 8) {
                Image(systemName: documentType.icon)
                    .font(.title2)
                    .foregroundColor(isSelected ? .white : .blue)

                Text(documentType.displayName)
                    .font(.caption)
                    .foregroundColor(isSelected ? .white : .primary)
                    .multilineTextAlignment(.center)
            }
            .frame(width: 80, height: 80)
            .background(isSelected ? Color.blue : Color.blue.opacity(0.1))
            .cornerRadius(12)
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(isSelected ? Color.blue : Color.clear, lineWidth: 2)
            )
        }
        .buttonStyle(PlainButtonStyle())
    }
}

struct UploadOptionCard: View {
    let title: String
    let subtitle: String
    let icon: String
    let color: Color
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            HStack(spacing: 15) {
                Image(systemName: icon)
                    .font(.title2)
                    .foregroundColor(color)
                    .frame(width: 30)

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
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(color.opacity(0.3), lineWidth: 2)
            )
            .cornerRadius(12)
        }
        .buttonStyle(PlainButtonStyle())
    }
}

struct DocumentRow: View {
    let document: UploadedDocument
    let onDelete: () -> Void

    private var dateFormatter: DateFormatter {
        let formatter = DateFormatter()
        formatter.dateStyle = .short
        formatter.timeStyle = .short
        return formatter
    }

    var body: some View {
        HStack(spacing: 15) {
            Image(systemName: document.documentType.icon)
                .font(.title2)
                .foregroundColor(.blue)

            VStack(alignment: .leading, spacing: 4) {
                Text(document.documentType.displayName)
                    .font(.headline)
                    .fontWeight(.semibold)

                Text(dateFormatter.string(from: document.uploadDate))
                    .font(.caption)
                    .foregroundColor(.secondary)
            }

            Spacer()

            VStack(alignment: .trailing, spacing: 4) {
                Text(document.status.displayName)
                    .font(.caption)
                    .fontWeight(.semibold)
                    .foregroundColor(document.status.color)

                Button(action: onDelete) {
                    Image(systemName: "trash")
                        .font(.caption)
                        .foregroundColor(.red)
                }
            }
        }
        .padding()
        .background(Color.white)
        .overlay(
            RoundedRectangle(cornerRadius: 12)
                .stroke(document.status.color.opacity(0.3), lineWidth: 1)
        )
        .cornerRadius(12)
    }
}

struct RequirementRow: View {
    let text: String
    let isCompleted: Bool

    var body: some View {
        HStack(spacing: 12) {
            Image(systemName: isCompleted ? "checkmark.circle.fill" : "circle")
                .foregroundColor(isCompleted ? .green : .gray)

            Text(text)
                .font(.caption)
                .foregroundColor(.secondary)

            Spacer()
        }
    }
}

#Preview {
    DocumentVerificationView()
        .environmentObject(AuthenticationManager())
        .environmentObject(APIClient())
}