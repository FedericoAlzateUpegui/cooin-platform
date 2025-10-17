//
//  DocumentVerificationView.swift
//  Cooin
//
//  Document verification and upload interface
//

import SwiftUI
import Combine

struct DocumentVerificationView: View {
    @Environment(\.dismiss) private var dismiss
    @EnvironmentObject var authManager: AuthenticationManager
    @EnvironmentObject var apiClient: APIClient
    @StateObject private var fileUploadManager: FileUploadManager
    @ObservedObject var languageManager = LanguageManager.shared

    @State private var selectedDocumentType: DocumentType = .idCard
    @State private var showingImagePicker = false
    @State private var showingCamera = false
    @State private var showingDocumentPicker = false
    @State private var selectedImage: UIImage?
    @State private var uploadSource: UploadSource = .camera
    @State private var showingCameraUnavailable = false
    @State private var showingDocumentPickerUnavailable = false

    enum UploadSource {
        case camera, photoLibrary, documents
    }

    init() {
        // Initialize with a temporary APIClient - will be replaced by environment object
        self._fileUploadManager = StateObject(wrappedValue: FileUploadManager(apiClient: APIClient()))
    }

    var body: some View {
        Text("").hidden().id(languageManager.refreshTrigger)
        NavigationView {
            ScrollView {
                VStack(spacing: 25) {
                    // Header
                    VStack(spacing: 10) {
                        Image(systemName: "checkmark.shield.fill")
                            .font(.system(size: 50))
                            .foregroundColor(.green)

                        Text("verification.title".localized)
                            .font(.title2)
                            .fontWeight(.bold)

                        Text("verification.description".localized)
                            .font(.body)
                            .foregroundColor(.secondary)
                            .multilineTextAlignment(.center)
                    }
                    .padding(.horizontal)

                    // Document Type Selection
                    VStack(spacing: 15) {
                        Text("verification.select_document_type".localized)
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
                        Text("verification.upload_method".localized)
                            .font(.headline)
                            .frame(maxWidth: .infinity, alignment: .leading)

                        VStack(spacing: 12) {
                            UploadOptionCard(
                                title: "verification.take_photo".localized,
                                subtitle: "verification.take_photo_subtitle".localized,
                                icon: "camera.fill",
                                color: .blue
                            ) {
                                uploadSource = .camera
                                #if targetEnvironment(simulator)
                                showingCameraUnavailable = true
                                #else
                                if UIImagePickerController.isSourceTypeAvailable(.camera) {
                                    showingCamera = true
                                } else {
                                    showingCameraUnavailable = true
                                }
                                #endif
                            }

                            UploadOptionCard(
                                title: "verification.choose_photos".localized,
                                subtitle: "verification.choose_photos_subtitle".localized,
                                icon: "photo.fill",
                                color: .green
                            ) {
                                uploadSource = .photoLibrary
                                showingImagePicker = true
                            }

                            UploadOptionCard(
                                title: "verification.browse_files".localized,
                                subtitle: "verification.browse_files_subtitle".localized,
                                icon: "doc.fill",
                                color: .orange
                            ) {
                                uploadSource = .photoLibrary
                                showingImagePicker = true
                            }
                        }
                    }
                    .padding(.horizontal)

                    // Upload Progress
                    if fileUploadManager.isUploading {
                        VStack(spacing: 10) {
                            Text("verification.uploading".localized)
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
                            Text("verification.uploaded_documents".localized)
                                .font(.headline)
                                .frame(maxWidth: .infinity, alignment: .leading)

                            LazyVStack(spacing: 10) {
                                ForEach(fileUploadManager.uploadedDocuments) { document in
                                    DocumentRowWithPreview(document: document) {
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
                        Text("verification.requirements_title".localized)
                            .font(.headline)
                            .frame(maxWidth: .infinity, alignment: .leading)

                        VStack(spacing: 8) {
                            RequirementRow(text: "verification.requirement_clear".localized, isCompleted: true)
                            RequirementRow(text: "verification.requirement_corners".localized, isCompleted: true)
                            RequirementRow(text: "verification.requirement_no_glare".localized, isCompleted: false)
                            RequirementRow(text: "verification.requirement_file_size".localized, isCompleted: true)
                        }
                    }
                    .padding(.horizontal)

                    Spacer(minLength: 100)
                }
                .padding(.top)
            }
            .navigationTitle("verification.navigation_title".localized)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("common.done".localized) {
                        dismiss()
                    }
                }
            }
        }
        .sheet(isPresented: $showingCamera) {
            DocumentCameraView(selectedImage: $selectedImage)
        }
        .sheet(isPresented: $showingImagePicker) {
            DocumentPhotoPickerView(selectedImage: $selectedImage)
        }
        .onChange(of: selectedImage) { image in
            if let image = image, let token = authManager.getAccessToken() {
                fileUploadManager.uploadImage(image, documentType: selectedDocumentType, authToken: token)
                selectedImage = nil
            }
        }
        .alert("verification.camera_unavailable".localized, isPresented: $showingCameraUnavailable) {
            Button("common.ok".localized) { }
        } message: {
            #if targetEnvironment(simulator)
            Text("verification.camera_unavailable_simulator".localized)
            #else
            Text("verification.camera_unavailable_device".localized)
            #endif
        }
        .alert("verification.document_picker".localized, isPresented: $showingDocumentPickerUnavailable) {
            Button("common.ok".localized) { }
        } message: {
            Text("verification.document_picker_coming_soon".localized)
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
    @ObservedObject var languageManager = LanguageManager.shared

    var body: some View {
        Text("").hidden().id(languageManager.refreshTrigger)
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
    @ObservedObject var languageManager = LanguageManager.shared

    var body: some View {
        Text("").hidden().id(languageManager.refreshTrigger)
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

struct DocumentRowWithPreview: View {
    let document: UploadedDocument
    let onDelete: () -> Void
    @ObservedObject var languageManager = LanguageManager.shared
    @State private var showingImagePreview = false

    private var dateFormatter: DateFormatter {
        let formatter = DateFormatter()
        formatter.dateStyle = .short
        formatter.timeStyle = .short
        return formatter
    }

    var body: some View {
        Text("").hidden().id(languageManager.refreshTrigger)
        Button(action: {
            if document.image != nil {
                showingImagePreview = true
            }
        }) {
            HStack(spacing: 15) {
                // Thumbnail or icon
                if let image = document.image {
                    Image(uiImage: image)
                        .resizable()
                        .aspectRatio(contentMode: .fill)
                        .frame(width: 60, height: 60)
                        .clipped()
                        .cornerRadius(8)
                } else {
                    Image(systemName: document.documentType.icon)
                        .font(.title2)
                        .foregroundColor(.blue)
                        .frame(width: 60, height: 60)
                }

                VStack(alignment: .leading, spacing: 4) {
                    Text(document.documentType.displayName)
                        .font(.headline)
                        .fontWeight(.semibold)
                        .foregroundColor(.primary)

                    Text(dateFormatter.string(from: document.uploadDate))
                        .font(.caption)
                        .foregroundColor(.secondary)

                    if document.image != nil {
                        Text("verification.tap_to_view".localized)
                            .font(.caption2)
                            .foregroundColor(.blue)
                    }
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
        .buttonStyle(PlainButtonStyle())
        .sheet(isPresented: $showingImagePreview) {
            if let image = document.image {
                DocumentImagePreview(image: image, documentType: document.documentType)
            }
        }
    }
}

struct DocumentImagePreview: View {
    let image: UIImage
    let documentType: DocumentType
    @Environment(\.dismiss) private var dismiss
    @ObservedObject var languageManager = LanguageManager.shared

    var body: some View {
        Text("").hidden().id(languageManager.refreshTrigger)
        NavigationView {
            ZStack {
                Color.black.edgesIgnoringSafeArea(.all)

                Image(uiImage: image)
                    .resizable()
                    .aspectRatio(contentMode: .fit)
                    .padding()
            }
            .navigationTitle(documentType.displayName)
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("common.done".localized) {
                        dismiss()
                    }
                    .foregroundColor(.white)
                }
            }
        }
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

// MARK: - Camera Pickers

struct DocumentCameraView: UIViewControllerRepresentable {
    @Binding var selectedImage: UIImage?
    @Environment(\.dismiss) private var dismiss

    func makeUIViewController(context: Context) -> UIImagePickerController {
        let picker = UIImagePickerController()
        picker.delegate = context.coordinator
        picker.sourceType = .camera
        picker.cameraCaptureMode = .photo
        picker.cameraDevice = .rear
        picker.allowsEditing = false
        return picker
    }

    func updateUIViewController(_ uiViewController: UIImagePickerController, context: Context) {}

    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    class Coordinator: NSObject, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
        let parent: DocumentCameraView

        init(_ parent: DocumentCameraView) {
            self.parent = parent
        }

        func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
            if let image = info[.originalImage] as? UIImage {
                parent.selectedImage = image
            }
            parent.dismiss()
        }

        func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
            parent.dismiss()
        }
    }
}

struct DocumentPhotoPickerView: UIViewControllerRepresentable {
    @Binding var selectedImage: UIImage?
    @Environment(\.dismiss) private var dismiss

    func makeUIViewController(context: Context) -> UIImagePickerController {
        let picker = UIImagePickerController()
        picker.delegate = context.coordinator
        picker.sourceType = .photoLibrary
        picker.allowsEditing = false
        return picker
    }

    func updateUIViewController(_ uiViewController: UIImagePickerController, context: Context) {}

    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    class Coordinator: NSObject, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
        let parent: DocumentPhotoPickerView

        init(_ parent: DocumentPhotoPickerView) {
            self.parent = parent
        }

        func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
            if let image = info[.originalImage] as? UIImage {
                parent.selectedImage = image
            }
            parent.dismiss()
        }

        func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
            parent.dismiss()
        }
    }
}

#Preview {
    DocumentVerificationView()
        .environmentObject(AuthenticationManager())
        .environmentObject(APIClient())
}